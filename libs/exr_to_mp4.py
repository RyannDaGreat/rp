# https://gist.github.com/SqrtRyan/719c46b275db344ec4bd9f1bcc82945c
#
# GPU-resident proof-of-concept rewrite. All per-frame compute lives on `device`
# (cuda / mps / cpu — selectable via the `device` kwarg). The only data crossing
# the CPU/GPU boundary per frame is one upload (OIIO decode -> tensor) and one
# download (uint16 tensor -> ffmpeg stdin bytes). No ping-pong.
#
# OCIO is called exactly once, at startup, to bake a log2-shaper + 65^3 3D LUT.
# Per frame the color transform is a torch grid_sample trilinear interpolation —
# OCIO is never on the hot path.

import functools
import glob
import json
import os
import shlex
import subprocess
import tempfile
import threading
import time
from functools import partial

import rp


OCIO_CONFIG = "studio-config-v4.0.0_aces-v2.0_ocio-v2.5"
DST_DISPLAY = "Rec.1886 Rec.709 - Display"          # output is locked to Rec.709 SDR
DST_VIEW = "ACES 2.0 - SDR 100 nits (Rec.709)"
PRINT_STYLE = "bold orange"

# log2 input domain covered by the 3D LUT. 2^-10 .. 2^+10 in scene-linear
# brackets ACES-style HDR comfortably (~1e-3 to ~1e3).
LUT3D_SIZE = 65
SHAPER_LOG2_MIN = -10.0
SHAPER_LOG2_MAX = +10.0

# Serializes GPU work across decode worker threads. Decode (OIIO, GIL-released)
# runs in parallel; the GPU stage is a serial funnel — that's fine because the
# GPU work per frame is tiny compared to OIIO decode + ffmpeg encode, and we
# avoid concurrent stream chaos for the PoC.
_gpu_lock = threading.Lock()


def console_print(text):
    rp.fansi_print(text, text_color=PRINT_STYLE)


def _read_header(path):
    """Query. Read framesPerSecond and PixelAspectRatio from an EXR header (defaults: 24.0, 1.0)."""
    import OpenImageIO as oiio
    inp = oiio.ImageInput.open(path)
    if inp is None:
        raise RuntimeError("Could not open " + path)
    try:
        spec = inp.spec()
        fps = spec.get_float_attribute("framesPerSecond") or 24.0
        par = (spec.get_float_attribute("PixelAspectRatio")
               or spec.get_float_attribute("pixelAspectRatio")
               or 1.0)
        return float(fps), float(par)
    finally:
        inp.close()


def _read_image(path, want_metadata=False):
    """
    Query. Reads an EXR as (H, W, C) float32 numpy.

    With want_metadata=True, returns (image, metadata) instead — metadata is
    the JSON-safe header dict from `_spec_metadata`, captured from the same
    open file handle as the pixels. Zero extra opens/reads: this matters when
    the EXR sits behind a slow remote mount (e.g. rclone with a VFS cache) —
    the header is grabbed while the file is already downloaded and hot.
    """
    import OpenImageIO as oiio
    inp = oiio.ImageInput.open(path)
    if inp is None:
        # oiio.geterror() both explains WHY (e.g. "not an OpenEXR file") and
        # clears OIIO's pending-error state (which otherwise warns at exit).
        raise RuntimeError("Could not open " + path + ": " + oiio.geterror())
    try:
        metadata = _spec_metadata(inp.spec()) if want_metadata else None
        image = inp.read_image(format=oiio.FLOAT)
        if image is None:
            raise RuntimeError("Could not read " + path + ": " + inp.geterror())
    finally:
        inp.close()
    return (image, metadata) if want_metadata else image


def _json_safe(value):
    """
    Pure function. Recursively convert a value into something json.dumps
    accepts. OIIO attribute values are already str/int/float/tuple, so this
    is normally a pass-through (tuples become lists); anything exotic
    degrades to str(value) — visibly, in the output, rather than crashing
    the encode over one odd header attribute.

    Examples:
        >>> _json_safe((1.0, 2.0))
        [1.0, 2.0]
        >>> _json_safe("zip")
        'zip'
        >>> _json_safe(b"raw")
        "b'raw'"
    """
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, (tuple, list)):
        return [_json_safe(v) for v in value]
    return str(value)


def _spec_metadata(spec):
    """
    Pure function. OIIO ImageSpec -> JSON-safe metadata dict: core geometry
    fields plus every header attribute (compression, smpte:TimeCode,
    worldToCamera, framesPerSecond, arbitrary show-specific attribs, ...).

    Args:
        spec (OpenImageIO.ImageSpec): as returned by ImageInput.spec()

    Returns:
        dict: {'width': int, 'height': int, 'x': int, 'y': int,
               'nchannels': int, 'channelnames': list of str, 'format': str,
               plus one key per header attribute}

    Examples:
        >>> # spec of a 64x48 RGB half EXR with a timecode:
        >>> # _spec_metadata(spec) -> {'width': 64, 'height': 48, 'x': 0,
        >>> #     'y': 0, 'nchannels': 3, 'channelnames': ['R', 'G', 'B'],
        >>> #     'format': 'half', 'compression': 'zip',
        >>> #     'smpte:TimeCode': [16909060, 0], 'framesPerSecond': 24.0}
    """
    metadata = dict(
        width=spec.width, height=spec.height, x=spec.x, y=spec.y,
        nchannels=spec.nchannels, channelnames=list(spec.channelnames),
        format=str(spec.format)
    )
    for attrib in spec.extra_attribs:
        metadata[attrib.name] = _json_safe(attrib.value)
    return metadata


def _metadata_tee_stream(stream, jsonl_file):
    """
    Generator command (writes jsonl_file as a side effect). Unzips a stream
    of (frame_bytes, metadata) pairs from _process_frame(collect_metadata=
    True): writes one JSON line per input EXR — in input order, including
    {'path':..., 'error':...} lines for unreadable frames — and yields the
    bytes (or None) onward, so the bad-frame policy wrappers downstream see
    the exact same stream they'd see with metadata off.
    """
    for frame_bytes, metadata in stream:
        jsonl_file.write(json.dumps(metadata) + "\n")
        yield frame_bytes


# ---- Bad-frame policies -------------------------------------------------
# Three self-contained generator wrappers, one per `strict` mode. Each one
# takes a stream of (bytes | None) — `None` signals "this frame failed to
# read" — and yields one bytes object per *input* item (skip yields fewer)
# according to its policy. The active policy is selected once in the main
# loop based on the user's `strict=` kwarg; the read site (`_process_frame`)
# only has to decide between raising and returning None.

def _strict_bad_frame_stream(stream):
    """
    Pure (generator). Pass-through stream wrapper for `strict='strict'`. The
    upstream `_process_frame` is supposed to raise on bad reads in this mode,
    so any None reaching here is an internal bug — assert loudly.
    """
    for x in stream:
        assert x is not None, "strict mode received None from _process_frame; that's a bug"
        yield x


def _skip_bad_frame_stream(stream):
    """
    Pure (generator). For `strict='skip'`. Drops None entries entirely — the
    output video has fewer frames than the input list. Timing of surviving
    frames advances by their original index, so a bad frame in the middle
    just disappears (slight one-frame "jump cut" at the gap).
    """
    for x in stream:
        if x is not None:
            yield x


def _pad_bad_frame_stream(stream, *, out_w, out_h):
    """
    Pure-ish (generator; allocates a black-frame buffer lazily). For
    `strict='pad'`. Substitutes a bad frame with:
        - the previous good frame's bytes, if any have been seen, else
        - the next good frame's bytes (held in a count of pending leading
          bad frames; emitted retroactively when the first good frame
          arrives), else
        - a black rgb48le frame (only reached when *every* input was bad).

    rgb48le = 16-bit RGB interleaved = 6 bytes per pixel.
    """
    pending = 0      # leading bad frames buffered until we see a good one
    last_good = None # most recent good frame's bytes
    for x in stream:
        if x is None:
            if last_good is not None:
                yield last_good
            else:
                pending += 1
        else:
            if pending and last_good is None:
                for _ in range(pending):
                    yield x
                pending = 0
            yield x
            last_good = x
    if last_good is None and pending:
        # All frames were bad — emit black for each.
        black = bytes(out_w * out_h * 6)
        for _ in range(pending):
            yield black


def _normalize_device_str(d):
    """
    Pure. Coerce one device value to a torch device string.

    int -> 'cuda:N' (the obvious shorthand)
    str -> as-is
    Anything else raises TypeError.

    Examples:
        >>> _normalize_device_str(0)
        'cuda:0'
        >>> _normalize_device_str('cuda:1')
        'cuda:1'
        >>> _normalize_device_str('mps')
        'mps'
    """
    if isinstance(d, bool):                                            # bool is a subclass of int — reject
        raise TypeError("device cannot be a bool; got " + repr(d))
    if isinstance(d, int):
        return "cuda:" + str(d)
    if isinstance(d, str):
        return d
    raise TypeError("device entries must be int, str, or list of those; got " + repr(type(d).__name__))


def _normalize_device_list(device):
    """
    Query (touches torch for auto-detect). Coerce `device` to a list of fully
    *indexed* torch device strings, so worker subprocesses never have to do
    any resolution themselves.

    None / 'auto' / 'cuda' -> all visible CUDA devices, else ['mps'], else ['cpu'].
        Bare 'cuda' (no index) is ambiguous — treat it as auto-detect rather
        than shipping an indexless string to workers.
    int                        -> ['cuda:N']
    str ('cuda:N' / 'mps' / 'cpu') -> [str]
    list/tuple                 -> [_normalize_device_str(x) for x in list]

    Examples:
        >>> _normalize_device_list('cuda:2')
        ['cuda:2']
        >>> _normalize_device_list(3)
        ['cuda:3']
        >>> _normalize_device_list([0, 1, 2])
        ['cuda:0', 'cuda:1', 'cuda:2']
    """
    if device is None or device == "auto" or device == "cuda":
        import torch
        if torch.cuda.is_available():
            return ["cuda:" + str(i) for i in range(torch.cuda.device_count())]
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return ["mps"]
        return ["cpu"]
    if isinstance(device, (list, tuple)):
        if not device:
            raise ValueError("device list is empty")
        return [_normalize_device_str(d) for d in device]
    return [_normalize_device_str(device)]


def _pick_device(device):
    """
    Query. Resolve a single device value (str/int/None) to a torch.device.
    None picks cuda > mps > cpu. CUDA devices are always returned with an
    explicit index (e.g. cuda:0 not bare cuda) because torch.cuda.set_device,
    which our worker threads call, rejects an indexless 'cuda' device.
    """
    import torch
    if device is None or device == "auto":
        if torch.cuda.is_available():
            return torch.device("cuda", torch.cuda.current_device())
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return torch.device("mps")
        return torch.device("cpu")
    d = torch.device(_normalize_device_str(device))
    if d.type == "cuda" and d.index is None:
        d = torch.device("cuda", torch.cuda.current_device())
    return d


@functools.lru_cache(maxsize=128)
def _bake_lut_3d(src_colorspace, device, lut_size):
    """
    Command on first call per (src_colorspace, device, lut_size), then memoized
    forever in this Python process. Build a 3D LUT tensor that maps
    scene-linear `src_colorspace` -> Rec.709 SDR, with a log2 shaper on the
    input axis covering 2^SHAPER_LOG2_MIN .. 2^SHAPER_LOG2_MAX scene-linear.

    Why a LUT rather than evaluating the transform directly: the ACES output
    transform is closed-form — OCIO's GPU path uses no 3D LUT for any of the 105
    transforms in the ACES 2.0 config — so the equations can be run per pixel
    instead. Per-pixel cost of each:

        equations   : 414 scalar ops, 37 transcendental (pow/sqrt/atan2/...)
        LUT lookup  :  24 scalar ops,  3 transcendental (the log2 shaper)

    The equations are ~366 separate elementwise steps, which in torch means one
    full-frame intermediate tensor per step: 13.6 GB of traffic per 4K frame,
    137x the 99.5 MB frame itself. Measured at 3840x2160:

        exact OCIO on CPU, 1 thread        1970.0 ms/frame
        equations in torch, eager           184.9 ms/frame
        equations in torch, torch.compile    97.6 ms/frame
        this LUT (65^3, grid_sample)          5.7 ms/frame

    The LUT's cost is interpolation error — see `exr_to_mp4`'s `lut_size`.

    The LRU cache is keyed by `(src_colorspace, device, lut_size)`. Each entry
    is lut_size^3 * 12 bytes and rarely changes within a run — a long-lived
    `exrs_to_mp4s` worker that processes many sequences in the same
    colorspace bakes the LUT exactly once, paying the bake on its first job
    and ~zero on every subsequent job.

    Returns:
        lut_3d: (1, 3, N, N, N) float32 on `device`, where N=lut_size. Laid out
        for torch.nn.functional.grid_sample as (N, C, D, H, W) with the LUT's
        R-axis at W (last), G-axis at H, B-axis at D, so a grid coord of
        (R, G, B) in [-1, 1] addresses the right cell.
    """
    import numpy as np
    import PyOpenColorIO as ocio
    import torch

    n = lut_size
    axis = np.linspace(0.0, 1.0, n, dtype=np.float32)
    # Shaper-space lattice: shaper_rgb[i,j,k] = (axis[i], axis[j], axis[k]) = (R, G, B) in [0, 1]
    r, g, b = np.meshgrid(axis, axis, axis, indexing="ij")
    shaper_rgb = np.stack([r, g, b], axis=-1)                          # (n, n, n, 3)
    # Inverse log2 shaper: shaper [0,1] -> scene-linear
    linear_rgb = np.power(
        2.0, SHAPER_LOG2_MIN + shaper_rgb * (SHAPER_LOG2_MAX - SHAPER_LOG2_MIN)
    ).astype(np.float32)
    flat = np.ascontiguousarray(linear_rgb.reshape(-1, 3))
    config = ocio.Config.CreateFromBuiltinConfig(OCIO_CONFIG)
    transform = ocio.DisplayViewTransform(src=src_colorspace, display=DST_DISPLAY, view=DST_VIEW)
    proc = config.getProcessor(transform).getDefaultCPUProcessor()
    proc.applyRGB(flat)                                                # in-place, ~10ms for 65^3
    out = flat.reshape(n, n, n, 3)                                     # (n_r, n_g, n_b, 3)
    # Lay out for grid_sample: (n_r, n_g, n_b, 3) -> (1, 3, n_b, n_g, n_r) = (N, C, D, H, W)
    from einops import rearrange
    out_t = rearrange(torch.from_numpy(out), "n_r n_g n_b c -> 1 c n_b n_g n_r").contiguous()
    return out_t.to(device)


def _unsquash_gpu(t, pixel_aspect):
    """
    Pure (on device). Stretch (H, W, C) tensor width by `pixel_aspect` via bicubic.
    No-op for pixel_aspect == 1.0.
    """
    if pixel_aspect == 1.0:
        return t
    import torch.nn.functional as F
    from einops import rearrange
    h, w = t.shape[:2]
    new_w = int(round(w * pixel_aspect))
    nchw = rearrange(t, "h w c -> 1 c h w")                            # F.interpolate wants NCHW
    nchw = F.interpolate(nchw, size=(h, new_w), mode="bicubic", align_corners=False)
    return rearrange(nchw, "1 c h w -> h w c").contiguous()


def _color_transform_gpu(t, lut_3d):
    """
    Pure (on device). Apply log2 shaper + 3D LUT to (H, W, 3) scene-linear -> Rec.709 SDR.

    Args:
        t: (H, W, 3) float32 on device, scene-linear values
        lut_3d: (1, 3, N, N, N) float32 on device, baked by `_bake_lut_3d`

    Returns:
        (H, W, 3) float32 on device, Rec.709 SDR (typically in [0, 1])
    """
    import torch
    import torch.nn.functional as F
    from einops import rearrange
    eps = 2.0 ** SHAPER_LOG2_MIN
    span = SHAPER_LOG2_MAX - SHAPER_LOG2_MIN
    # log2 shaper: scene-linear -> [0, 1], still HWC
    s = ((torch.log2(t.clamp_min(eps)) - SHAPER_LOG2_MIN) / span).clamp_(0.0, 1.0)
    # grid_sample wants grid (N, D_out, H_out, W_out, 3) with last dim = (x, y, z) = (W, H, D) = (R, G, B)
    grid = rearrange(s * 2.0 - 1.0, "h w c -> 1 1 h w c")
    sampled = F.grid_sample(
        lut_3d, grid, mode="bilinear", padding_mode="border", align_corners=True
    )                                                                  # (1, 3, 1, H, W)
    return rearrange(sampled, "1 c 1 h w -> h w c").contiguous()


def _process_frame(path, *, frame_transform, pre_unsquash_frame_transform,
                   pixel_aspect, out_h, out_w, clip, lut_3d, device, strict,
                   collect_metadata=False):
    """
    Command. EXR file -> rgb48le bytes for ffmpeg stdin. All compute on `device`.

    Pipeline (one upload, one download):
        OIIO decode -> upload -> pre_unsquash_frame_transform -> unsquash (bicubic)
        -> frame_transform -> crop -> log2 shaper -> 3D LUT -> clip -> quantize uint16
        -> download -> tobytes

    If `strict='strict'`, a failed OIIO read re-raises (kills the run). If
    `strict` is 'skip' or 'pad', a failed read returns None and the
    downstream policy wrapper decides what bytes (if any) make it to ffmpeg.

    With `collect_metadata=True`, returns (frame_bytes, metadata) pairs
    instead — metadata is the JSON-safe header dict (plus 'path'), read from
    the same file handle as the pixels; failed reads pair None with
    {'path':..., 'error':...}. `_metadata_tee_stream` unzips these before the
    bad-frame policy wrappers, which only ever see plain bytes|None.
    """
    import torch

    metadata = None
    try:
        if collect_metadata:
            np_image, metadata = _read_image(path, want_metadata=True)  # (H, W, C) float32
            metadata = dict(path=path, **metadata)
        else:
            np_image = _read_image(path)                               # (H, W, C) float32
    except RuntimeError as e:
        if strict == "strict":
            raise
        return (None, dict(path=path, error=str(e))) if collect_metadata else None
    t_cpu = torch.from_numpy(np_image)
    if device.type == "cuda":
        # PyTorch's "current CUDA device" is per-thread and defaults to cuda:0
        # for every new worker thread that rp.load_files spawns. Even though
        # .to(device) targets the right GPU, the thread's CUDA context (and
        # any op that allocates without an explicit device) lands on cuda:0
        # — which is why nvidia-smi showed work on 0 when device='cuda:2'.
        # Pinning the current device for this thread fixes it.
        torch.cuda.set_device(device)
        t_cpu = t_cpu.pin_memory()

    from einops import rearrange

    with _gpu_lock:
        t = t_cpu.to(device, non_blocking=True)                        # HWC, pipeline-internal layout

        # User transforms receive CHW (rp convention for torch images); we
        # rearrange in and out around each call so the pipeline's HWC internals
        # don't leak to user code, and rp helpers like resize_image_to_fit
        # drop in as a frame_transform with no wrapper.
        if pre_unsquash_frame_transform is not None:
            t = rearrange(pre_unsquash_frame_transform(rearrange(t, "h w c -> c h w")), "c h w -> h w c")

        t = _unsquash_gpu(t, pixel_aspect)

        if frame_transform is not None:
            t = rearrange(frame_transform(rearrange(t, "h w c -> c h w")), "c h w -> h w c")

        t = t[:out_h, :out_w]
        if t.shape[-1] > 3:                                            # drop alpha if present
            t = t[..., :3]
        t = t.contiguous().float()

        t = _color_transform_gpu(t, lut_3d)

        if clip:
            t.clamp_(0.0, 1.0)

        t.mul_(65535.0).add_(0.5).clamp_(0.0, 65535.0)
        quantized = t.to(torch.uint16)
        result = quantized.cpu().numpy()

    # Force little-endian for ffmpeg rgb48le. No-op view on LE hosts.
    frame_bytes = result.astype("<u2", copy=False).tobytes()
    return (frame_bytes, metadata) if collect_metadata else frame_bytes


_FANOUT_FORWARDED_KWARGS = (
    "src_colorspace", "num_threads", "buffer_limit", "codec", "crf", "preset",
    "pix_fmt", "unsquash", "atomic", "clip", "fps", "overwrite", "show_progress",
    "strict", "lut_size",
)


def _fanout_exr_to_mp4(exr_paths, out_path, *, devices, num_shards, meta_path, kwargs):
    """
    Command. Shard `exr_paths` into `num_shards` contiguous chunks, launch each
    chunk as a subprocess pinned to one device via CUDA_VISIBLE_DEVICES, wait
    for all to finish, then losslessly concat the shard videos into `out_path`
    via `rp.concat_video_files`. If `meta_path` is set, each shard
    writes its own metadata JSONL and they're merged (concatenated in shard
    order — same ordering guarantee as the video). The bash command for each
    shard is printed before launch so the user can audit what's about to run.

    Each shard's EXR list is written to a temp .txt file; the subprocess loads
    it via `rp.load_file_lines(...)` — so non-globbable lists work fine.

    Forwarded kwargs: see `_FANOUT_FORWARDED_KWARGS`. Not supported in fanout
    mode: `frame_transform`, `pre_unsquash_frame_transform` (can't serialize
    Python callables across processes), `ffmpeg_extra_args` (use single-shard).
    """
    if num_shards is None or num_shards < 1:
        raise ValueError("num_shards must be >= 1")
    if not devices:
        devices = ["cuda"]
    if kwargs.get("ffmpeg_extra_args"):
        raise ValueError("ffmpeg_extra_args not supported in fanout mode (run single-shard for codec-specific tuning)")

    # Resolve exr_paths into a concrete list (mirrors the single-shard branch).
    if isinstance(exr_paths, str):
        if rp.is_a_folder(exr_paths):
            exr_paths = rp.get_all_paths(exr_paths, file_extension_filter="exr", sort_by="number")
        else:
            exr_paths = rp.sorted_by_number(glob.glob(exr_paths))
    exr_paths = list(exr_paths)
    if not exr_paths:
        raise ValueError("exr_paths is empty")
    num_shards = min(num_shards, len(exr_paths))

    rp.make_parent_directory(out_path)

    # One scratch directory for the whole fanout, prefixed for greppability.
    # All shard listfiles, shard videos, and the callable .rpo blobs live in
    # here with legible names — easier to debug than 16 anonymous /tmp/tmpXXXX
    # paths scattered across the system tempdir.
    tmp_dir = tempfile.mkdtemp(prefix="exr_to_mp4_")
    pad = len(str(num_shards - 1))                                     # 16 shards -> 2-digit zero-pad

    shards = rp.split_into_n_sublists(exr_paths, num_shards)
    ext = rp.get_file_extension(out_path)  # shards share out_path's container (.mp4/.mov/...)
    shard_listfiles = [os.path.join(tmp_dir, "shard_" + str(i).zfill(pad) + "_frames.txt") for i in range(num_shards)]
    shard_outputs   = [os.path.join(tmp_dir, "shard_" + str(i).zfill(pad) + "." + ext)     for i in range(num_shards)]
    shard_metadatas = None
    if meta_path is not None:
        shard_metadatas = [os.path.join(tmp_dir, "shard_" + str(i).zfill(pad) + "_metadata.jsonl") for i in range(num_shards)]
    for listfile, shard in zip(shard_listfiles, shards):
        rp.string_to_text_file(listfile, "\n".join(shard))

    # `rp call` parses `--kwarg value` by evaluating value as Python and
    # `---kwarg value` by treating it as a literal string. Strings whose value
    # *parses* as Python (e.g. 'ACES2065-1' → `ACES2065 - 1` → NameError) must
    # use `---`. Bools/ints/floats want `--` so 'True'/'20' become real values.
    def _flag(name, val):
        return ["---" + name if isinstance(val, str) else "--" + name, str(val)]

    forwarded = []
    for name in _FANOUT_FORWARDED_KWARGS:
        if name in kwargs and kwargs[name] is not None:
            forwarded.extend(_flag(name, kwargs[name]))

    # Callable kwargs (frame_transform, pre_unsquash_frame_transform) are
    # serialized to one shared .rpo file per kwarg (rp's "RP Object" format,
    # dill-based, the same thing object_to_file / file_to_object / omni_save /
    # omni_load all use). Forwarded as the Python expression
    # `file_to_object(".../frame_transform.rpo")` — rp call evaluates the expr
    # at startup and the child receives a real callable, no API change inside
    # exr_to_mp4. Lives in tmp_dir so it's deleted by the same cleanup.
    for name in ("frame_transform", "pre_unsquash_frame_transform"):
        val = kwargs.get(name)
        if val is not None:
            rpo = os.path.join(tmp_dir, name + ".rpo")
            rp.object_to_file(val, rpo)
            forwarded.extend(["--" + name, "file_to_object(" + json.dumps(rpo) + ")"])

    # Probe ONCE in the parent and forward the result to every shard, so the
    # shards skip their own _read_header + frame probe + user-transform-on-
    # frame-0 entirely. Probe runs on CPU — the parent never touches a GPU,
    # so it pays no CUDA cold-init cost on top of the shards'.
    import torch as _torch
    from einops import rearrange as _parent_rearrange
    parent_dev = _torch.device("cpu")
    header_fps, pixel_aspect = _read_header(exr_paths[0])
    probe_fps = kwargs.get("fps") or header_fps
    probe_par = 1.0 if (kwargs.get("unsquash", True) is False) else pixel_aspect
    probe_t = _torch.from_numpy(_read_image(exr_paths[0])).to(parent_dev)
    if kwargs.get("pre_unsquash_frame_transform") is not None:
        probe_t = _parent_rearrange(
            kwargs["pre_unsquash_frame_transform"](_parent_rearrange(probe_t, "h w c -> c h w")),
            "c h w -> h w c",
        )
    probe_t = _unsquash_gpu(probe_t, probe_par)
    if kwargs.get("frame_transform") is not None:
        probe_t = _parent_rearrange(
            kwargs["frame_transform"](_parent_rearrange(probe_t, "h w c -> c h w")),
            "c h w -> h w c",
        )
    probe_out_h, probe_out_w = probe_t.shape[:2]
    probe_out_h, probe_out_w = rp.r._round_dimensions_to_even(probe_out_h, probe_out_w)
    del probe_t
    probe_rpo = os.path.join(tmp_dir, "probe.rpo")
    rp.object_to_file((probe_fps, probe_par, probe_out_h, probe_out_w), probe_rpo)
    forwarded.extend(["--_probe", "file_to_object(" + json.dumps(probe_rpo) + ")"])

    # First positional is exr_paths, given as a Python expression that rp call
    # will eval — `load_file_lines("/tmp/x.txt")`. The path is rendered with
    # json.dumps so it stays in double quotes; the whole expr then survives
    # bash's outer single-quote wrap without any apostrophe escaping.
    plans = []
    for i, (listfile, shard_out) in enumerate(zip(shard_listfiles, shard_outputs)):
        device_str = devices[i % len(devices)]
        cmd = ["rp", "call", "exr_to_mp4",
               "load_file_lines(" + json.dumps(listfile) + ")",
               "---", shard_out,
               *_flag("device", device_str),
               *forwarded]
        if shard_metadatas is not None:
            cmd.extend(_flag("meta_path", shard_metadatas[i]))
        plans.append(cmd)

    # Format the whole fanout as one bash script (copy-pasteable, ending with `wait`).
    script_lines = [
        "# exr_to_mp4 fanout: " + str(num_shards) + " shards across "
        + str(len(devices)) + " device(s) -> " + shlex.quote(out_path),
    ]
    for cmd in plans:
        script_lines.append(" ".join(shlex.quote(x) for x in cmd) + " &")
    script_lines.append("wait")
    rp.display_code_cell("\n".join(script_lines), language="bash", title="exr_to_mp4 fanout")

    started = time.perf_counter()
    # stdin=DEVNULL: launching from an interactive `rp` REPL leaves the
    # subprocesses sharing the parent's controlling tty. The first one to
    # touch stdin gets SIGTTIN and suspends, hanging the whole fanout. The
    # hand-pasted bash version doesn't hit this because `cmd &` in interactive
    # bash detaches stdin per backgrounded job.
    procs = [subprocess.Popen(c, stdin=subprocess.DEVNULL) for c in plans]
    fails = []
    try:
        for i, p in enumerate(procs):
            rc = p.wait()
            if rc != 0:
                fails.append((i, rc))
        if fails:
            raise RuntimeError("exr_to_mp4 fanout: shards failed " + repr(fails))
        rp.concat_video_files(shard_outputs, out_path)
        if shard_metadatas is not None:
            # Merge shard JSONLs in shard order — line order matches frame
            # order in the concatenated video (shards are contiguous chunks).
            rp.make_parent_directory(meta_path)
            rp.string_to_text_file(
                meta_path,
                "".join(rp.text_file_to_string(p) for p in shard_metadatas)
            )
    finally:
        rp.delete_folder(tmp_dir, recursive=True, strict=False)
    elapsed = time.perf_counter() - started
    console_print("exr_to_mp4 fanout done in " + str(round(elapsed, 3)) + "s -> " + out_path)
    return out_path


def _ffmpeg_command(out_path, fps, out_w, out_h, *, codec, crf, preset, pix_fmt, extra_args):
    return [
        "ffmpeg", "-hide_banner", "-nostats", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb48le",
        "-s", str(out_w) + "x" + str(out_h), "-r", str(fps),
        "-i", "-",
        "-vf", "format=" + pix_fmt,
        "-c:v", codec, "-preset", preset,
        *rp.r._ffmpeg_quality_flags(codec, crf),
        *extra_args,
        "-color_primaries", "bt709", "-color_trc", "bt709",
        "-colorspace", "bt709", "-color_range", "tv",
        "-movflags", "+faststart",
        out_path,
    ]


def exr_to_mp4(
    exr_paths,
    out_path,
    meta_path=None,                 # optional: also write per-frame EXR header metadata as JSONL
                                    # (one JSON object per input frame, in frame order). True derives
                                    # the path from out_path (out.mov -> out.jsonl). See Args.
    *,
    device=None,                    # int (cuda:N) | str ('cuda', 'mps', 'cpu', 'cuda:N') | list of those | None=auto.
                                    # A list (or len>1 after normalizing) triggers fanout: each shard pinned to one device
                                    # via CUDA_VISIBLE_DEVICES, round-robined across the list.
    num_shards=None,                # number of shards. Defaults to len(device list).
                                    # If < len(device list), only the first num_shards devices are used.
                                    # If > len(device list), devices are round-robined (multi-shard per GPU).
                                    # If > frame count, clamped down to frame count (one shard per frame).
    frame_transform=None,           # callable(CHW float32 tensor on device) -> same. None = identity. CHW matches rp convention; the pipeline's HWC internals are wrapped around the call.
    overwrite=True,
    fps=None,
    src_colorspace="ACES2065-1",
    lut_size=LUT3D_SIZE,
    num_threads=8,
    buffer_limit=None,
    show_progress=True,
    codec="libx264",
    crf=20,
    preset="ultrafast",
    pix_fmt="yuv420p10le",
    ffmpeg_extra_args=(),
    unsquash=True,
    atomic=False,
    clip=True,
    pre_unsquash_frame_transform=None,
    strict=True,                    # bad-EXR policy. True/'strict' (default) raises on any unreadable frame.
                                    # 'skip' drops bad frames (output is shorter). 'pad' substitutes the
                                    # previous good frame (or the first upcoming good frame for leading
                                    # bad ones, or black if every frame is bad).
    _probe=None                     # PRIVATE. (fps, pixel_aspect, out_h, out_w) tuple. When set, single-shard
                                    # path skips its probe + header read entirely — fanout's parent probes
                                    # once and passes the result to each shard so we don't duplicate
                                    # `_read_header` + `_read_image` + `frame_transform` across N shards.
):
    """
    Convert a sequence of EXR frames to MP4 (or MOV — see `out_path`) with a
    fully torch-resident pipeline.

    Color transform (`src_colorspace` -> Rec.709 SDR via the ACES 2.0 SDR view) is
    baked into a 65^3 3D LUT + log2 shaper at startup. Per frame everything runs
    on `device`: unsquash (bicubic), `pre_unsquash_frame_transform`,
    `frame_transform`, color transform, clip, uint16 quantize. Exactly one
    CPU->device upload (OIIO decode) and one device->CPU download (-> ffmpeg
    rgb48le bytes) per frame.

    `frame_transform` / `pre_unsquash_frame_transform` contract — strict:

        Input  : torch.Tensor, shape (C, H, W), dtype float32, on `device`.
                 Layout is CHW — matches rp's convention for torch images
                 (`rp.is_torch_image`, `rp.torch_resize_image`, etc), so
                 numpy-free rp helpers drop in as a frame_transform with no
                 wrapper. The pipeline's internal layout is HWC; we rearrange
                 to CHW around your call so you never see HWC. C is typically
                 3 (RGB) but may be 4 if the source EXR has alpha (alpha is
                 dropped after this transform). Values are scene-linear in
                 `src_colorspace` (e.g. ACES2065-1) — HDR, unbounded above;
                 expect highlights well above 1.0. The OCIO tonemap to
                 Rec.709 [0,1] runs AFTER `frame_transform`.

        Output : same — torch.Tensor, (C, H', W'), float32, on `device`,
                 CHW, scene-linear. No silent conversion; numpy returns,
                 wrong-device tensors, or non-float dtypes will crash the
                 next stage. If you need numpy ops, wrap them yourself.

        `pre_unsquash_frame_transform` is the same shape and dtype but
        runs BEFORE the anamorphic unsquash — pixels may be non-square if
        the EXR's PixelAspectRatio != 1.

    Performance:
        - OIIO decode runs in parallel across `num_threads` (GIL-released in C++).
        - GPU stage is serialized by a module-level lock (one frame on GPU at a time).
          The lock is fine — GPU work per frame is far smaller than decode + encode.
        - ffmpeg encodes as a separate OS process.

    Args:
        out_path: destination video file. The container is chosen by ffmpeg
            from the extension — `.mp4` and `.mov` are both supported (the
            function's name notwithstanding). This applies in every mode:
            single-shard, `atomic=True`, and fanout (shards are encoded in
            the same container, then losslessly concatenated).
        meta_path: optional (positional, right after out_path): ALSO capture
            per-frame EXR header metadata as JSONL — one JSON object per
            input frame, in frame order. Pass True to derive the path from
            out_path by swapping the extension (out.mov -> out.jsonl). Each line: 'path', core fields (width, height, x, y,
            nchannels, channelnames, format), and every header attribute
            (framesPerSecond, smpte:TimeCode, worldToCamera, compression,
            show-specific attribs, ...). Values are JSON-safe (tuples become
            lists; exotic types degrade to their str()).
            Why here and not a separate pass: headers are read from the SAME
            open file handle as the pixels — zero extra I/O. When EXRs sit
            behind a slow remote mount (e.g. rclone with a VFS cache), the
            metadata is grabbed while each file is already downloaded and
            hot, instead of re-downloading whole files later just for
            headers. (For a standalone metadata pass, see
            `rp.load_exr_metadatas` — note it returns raw OpenEXR header
            dicts, a different shape than these OIIO-derived lines.)
            With strict='skip'/'pad', unreadable frames still get a line:
            {"path": ..., "error": ...} — so line count always equals input
            frame count, even when the video has fewer/padded frames.
            Honors `atomic` (temp file + rename) and `overwrite`. In fanout
            mode each shard writes its own JSONL and they're merged in shard
            order, exactly like the shard videos.
        device: int | str | list of int/str | None.
            A scalar runs single-shard. A list (or `num_shards > 1`) triggers
            subprocess fanout: each shard is launched as `rp call exr_to_mp4`
            with `--device cuda:N` targeting one device from the resolved list
            (round-robined). Shard outputs are losslessly stitched into
            `out_path` via `rp.concat_video_files`. The bash for every shard
            is printed (via `rp.display_code_cell(language='bash')`) before
            launch for audit. Callable kwargs (`frame_transform` /
            `pre_unsquash_frame_transform`) are saved to a tmp `.rpo`
            (RP Object) file in fanout mode and re-loaded in each shard
            via `file_to_object("...")` in the printed bash — so closures,
            lambdas, and partials all survive the boundary. Non-empty
            `ffmpeg_extra_args` is the only thing fanout still rejects.
        lut_size: edge length of the baked 3D LUT (default 65). The LUT is
            lut_size^3 float32 RGB entries = lut_size^3 * 12 bytes on the GPU,
            baked once per (src_colorspace, device, lut_size) and cached for
            the process. See `_bake_lut_3d` for why a LUT is used at all.

            The shaper spans 20 stops (2^-10 .. 2^+10), so cells/stop =
            (n-1)/20 is what actually governs accuracy.

               n     entries        memory   cells/stop   bake      p99 err
              ----------------------------------------------------------------
              33      35,937        0.4 MB          1.6   0.01 s     44.6 cv
              65     274,625        3.3 MB          3.2   0.07 s     17.5 cv
             129   2,146,689       25.8 MB          6.4   0.53 s      6.7 cv
             257  16,974,593      203.7 MB         12.8   4.36 s      2.7 cv
             513 135,005,697        1.62 GB        25.6   ~35 s      ~1.1 cv
            1025 1,076,890,625     12.92 GB        51.2   ~4.7 min   ~0.5 cv

            `p99 err` is the 99th-percentile error against exact OCIO in 10-bit
            code values, measured on saturated content (the hard case); neutral
            content is roughly 4x better. The 513 and 1025 rows are extrapolated
            from the n^3 scaling, not measured.

            Powers of two work too and cost marginally less (64 -> 3.1 MB,
            128 -> 25.2 MB, 256 -> 201.3 MB, 512 -> 1.61 GB, 1024 -> 12.88 GB),
            but odd sizes are the interchange convention — they put a lattice
            point exactly at each end of the domain, which is what
            grid_sample(align_corners=True) expects. 65 is the industry-standard
            size (OCIO's ACES configs bake 3D LUTs at 65^3 by default:
            https://opencolorio.readthedocs.io/en/latest/configurations/aces_1.0.3.html
            — "The default resolution is 65x65x65 for the 3D LUTs").

            Anything under ~100 MB is fine for most uses, which puts everything
            up to 129 comfortably in range and makes 257 the first size you have
            to think about.

            129 is the best value if you can spend it: 2.9x the accuracy for
            21% more time (8.0 vs 6.6 ms/frame at 4K). Past 257 the returns are
            poor relative to the memory; those sizes are for archival masters.
            For dailies, 65 is already far below the noise floor of an ultrafast
            x264 encode.

            Size changes every pixel slightly, so keep one size for a whole
            project — mixing sizes across shots makes them fail to intercut.

        num_shards: total shards in fanout mode. Defaults to len(resolved
            device list). If smaller than the device list, only the first
            num_shards devices get work (the rest sit idle — user's call).
            If larger than the device list, devices are round-robined
            (multiple shards per GPU). If larger than the frame count,
            clamped down to the frame count (one shard per frame).

    Examples:

        #Process a bunch of foders of exr's
        exr_folders=rp_iglob('/dailies/*/exrs')
        out_dir='/users/burgert/dailies/mp4s'
        for exr_folder in exr_folders:
            fansi_print(exr_folder,'bold orange')
            mp4_filename=path_join(path_split(exr_folder)[-3:-1]).replace('/','>>')+'.mp4'
            exr_glob=path_join(exr_folder,'*.exr')
            exr_to_mp4(exr_glob,num_shards=32,out_path=mp4_filename,strict='pad')

        # Single GPU (auto), single process. Local development / testing.
        exr_to_mp4(paths, "out.mp4")

        # Pin to a specific GPU.
        exr_to_mp4(paths, "out.mp4", device="cuda:2")     # or device=2

        # Fan out across all visible GPUs (auto-detect via torch.cuda.device_count).
        # On an 8-GPU box: 8 subprocesses, one shard per GPU.
        exr_to_mp4(paths, "out.mp4", num_shards=8)
        # Equivalent shortcut: omit num_shards, it defaults to the visible GPU count.
        exr_to_mp4(paths, "out.mp4", device=None)

        # 2 shards per GPU on an 8-GPU box (16 processes, round-robined).
        exr_to_mp4(paths, "out.mp4", num_shards=16)

        # Pick a subset of GPUs explicitly.
        exr_to_mp4(paths, "out.mp4", device=[0, 2, 4, 6])               # 4 shards, one each
        exr_to_mp4(paths, "out.mp4", device=[0, 2, 4, 6], num_shards=8) # 8 shards, 2 per

        # CPU-only fanout (silly but works for testing).
        exr_to_mp4(paths, "out.mp4", device=["cpu", "cpu"], num_shards=2)

        # Downscale to fit 720x720 (preserves aspect → ~720p for 16:9 input).
        # rp.resize_image_to_fit accepts CHW torch tensors directly — pickled
        # by dill across fanout shards, runs on-device, no CPU roundtrip.
        from functools import partial
        exr_to_mp4(paths, "out.mp4",
                   frame_transform=partial(rp.resize_image_to_fit, height=720, width=720))

        # 10-bit AV1 via SVT-AV1 (fast, good quality, modern players).
        # Requires an ffmpeg build with libsvtav1 — check `ffmpeg -encoders`.
        exr_to_mp4(paths, "out.mp4",
                   codec="libsvtav1", pix_fmt="yuv420p10le", crf=30, preset="6")

        # 12-bit AV1 via libaom-av1 (archival; SVT-AV1 caps at 10-bit so 12-bit
        # needs libaom, which is much slower — -row-mt and -cpu-used=4 are
        # auto-applied to make it merely slow rather than glacial).
        exr_to_mp4(paths, "out.mp4",
                   codec="libaom-av1", pix_fmt="yuv420p12le", crf=28, preset="medium")

        # 10-bit H.265 (libx265; ubiquitous, fast, good quality).
        exr_to_mp4(paths, "out.mp4",
                   codec="libx265", pix_fmt="yuv420p10le", crf=20, preset="medium")

        # 12-bit H.265 (archival; libx264 caps at 10-bit so 12-bit needs libx265).
        exr_to_mp4(paths, "out.mp4",
                   codec="libx265", pix_fmt="yuv420p12le", crf=20, preset="medium")

        # MOV container: just use a .mov extension (works in all modes,
        # including atomic and fanout).
        exr_to_mp4(paths, "out.mov")

        # Capture per-frame EXR header metadata while encoding (one JSON line
        # per input frame, in frame order — timecode, camera matrices, etc).
        # Free: headers come from the same file handle as the pixels, so on a
        # slow mount (rclone etc) they're grabbed while each file is hot.
        exr_to_mp4(paths, "out.mp4", "out_metadata.jsonl")
        # Or just pass True to write alongside the video: out.mp4 -> out.jsonl
        exr_to_mp4(paths, "out.mp4", True)

        # ProRes 422 HQ in MOV (editorial delivery). NOTE: prores_ks ignores
        # `crf` and `preset` (ffmpeg warns but proceeds) — quality is set by
        # -profile:v (proxy/lt/standard/hq/4444) and optionally -qscale:v.
        exr_to_mp4(paths, "out.mov",
                   codec="prores_ks", pix_fmt="yuv422p10le",
                   ffmpeg_extra_args=("-profile:v", "hq"))

        # ---- GPU encoders: same `crf=` semantics, codec name does the work. ----
        # The function translates `crf` internally: -crf for libx*, -rc vbr -cq
        # for *_nvenc, -q:v on an inverted scale for *_videotoolbox. So one
        # script runs unchanged on a Mac (VideoToolbox) and an NVIDIA box
        # (NVENC) — just swap the codec name.
        #
        # Note: GPU encoders cap at 10-bit. For 12-bit you need libx265 / libaom-av1.
        # pix_fmt for 10-bit GPU is `p010le` (NV12-style 10-bit) — NVENC and
        # VideoToolbox reject the libx*-style `yuv420p10le`.

        # 10-bit HEVC on NVIDIA GPU (Turing+; ~5–10× faster than libx265).
        exr_to_mp4(paths, "out.mp4",
                   codec="hevc_nvenc", pix_fmt="p010le", crf=23, preset="p5")

        # 8-bit H.264 on NVIDIA GPU (every NVENC-capable card; max compatibility).
        exr_to_mp4(paths, "out.mp4",
                   codec="h264_nvenc", pix_fmt="yuv420p", crf=23, preset="p5")

        # 10-bit AV1 on NVIDIA GPU (RTX 40-series / Ada Lovelace+ only).
        exr_to_mp4(paths, "out.mp4",
                   codec="av1_nvenc", pix_fmt="p010le", crf=30, preset="p5")

        # 10-bit HEVC on Apple Silicon / Intel Mac (VideoToolbox).
        exr_to_mp4(paths, "out.mp4",
                   codec="hevc_videotoolbox", pix_fmt="p010le", crf=23, preset="medium")

        # 8-bit H.264 on Mac (VideoToolbox).
        exr_to_mp4(paths, "out.mp4",
                   codec="h264_videotoolbox", pix_fmt="yuv420p", crf=23, preset="medium")

        # ---- Bad-frame policies via `strict=` ---------------------------
        # Default `strict=True` raises immediately if any EXR can't be read
        # (truncated file, wrong format, permissions, ...). Two relaxed modes:

        # Skip unreadable frames entirely (output is shorter; surviving frames
        # advance in time at their original index — a slight jump-cut at each gap).
        exr_to_mp4(paths, "out.mp4", strict="skip")

        # Pad unreadable frames with the previous good frame's content (or the
        # first upcoming good frame for any leading bad ones, or black if every
        # frame is bad). Output length matches input frame count.
        exr_to_mp4(paths, "out.mp4", strict="pad")
    """
    # Resolve runtime deps in the parent BEFORE any fanout, so subprocesses
    # don't race each other to pip-install the same packages. Subsequent
    # pip_import calls in the shards are no-ops once the parent succeeds.
    rp.pip_import("OpenImageIO")
    rp.pip_import("PyOpenColorIO")
    rp.pip_import("torch")
    rp.pip_import("einops")
    rp.r._ensure_ffmpeg_installed()
    # Fail fast if the requested codec isn't in this ffmpeg build. Otherwise
    # we'd decode the entire shard before ffmpeg said "Unknown encoder".
    if codec not in rp.get_available_ffmpeg_codecs():
        raise ValueError(
            "codec=" + repr(codec) + " is not available in this ffmpeg build. "
            "Available codecs: rp.get_available_ffmpeg_codecs()"
        )

    # Normalize the `strict` kwarg to one of the three internal string values.
    # `True` is the user-facing default and aliases 'strict'; `False` aliases
    # 'skip' (the natural meaning of "stop being strict").
    if strict is True:  strict = "strict"
    if strict is False: strict = "skip"
    if strict not in ("strict", "skip", "pad"):
        raise ValueError("strict must be True/'strict', False/'skip', or 'pad'; got " + repr(strict))

    # meta_path=True derives the path from out_path: out.mov -> out.jsonl.
    # Resolved before fanout dispatch so the merged JSONL lands at the derived path.
    if meta_path is True:
        meta_path = rp.with_file_extension(out_path, "jsonl", replace=True)

    # Fanout dispatch: a list device or num_shards>1 means subprocess fanout.
    is_list_device = isinstance(device, (list, tuple))
    if is_list_device or (num_shards is not None and num_shards > 1):
        device_list = _normalize_device_list(device)
        if num_shards is None:
            num_shards = len(device_list)
        # If shards < devices (e.g. auto-detect grabbed 8 GPUs but user asked
        # for num_shards=4), round-robin only hits the first num_shards devices
        # and the rest sit idle. That's the user's call, not an error.
        if num_shards < len(device_list):
            device_list = device_list[:num_shards]
        # A single-element list with num_shards==1 is effectively single-shard — fall through.
        if not (len(device_list) == 1 and num_shards == 1):
            return _fanout_exr_to_mp4(
                exr_paths, out_path,
                devices=device_list,
                num_shards=num_shards,
                meta_path=meta_path,
                kwargs=dict(
                    src_colorspace=src_colorspace, num_threads=num_threads,
                    buffer_limit=buffer_limit, codec=codec, crf=crf, preset=preset,
                    pix_fmt=pix_fmt, unsquash=unsquash, atomic=atomic, clip=clip,
                    fps=fps, overwrite=overwrite, show_progress=show_progress,
                    lut_size=lut_size,
                    frame_transform=frame_transform,
                    pre_unsquash_frame_transform=pre_unsquash_frame_transform,
                    ffmpeg_extra_args=ffmpeg_extra_args,
                    strict=strict,
                ),
            )
        device = device_list[0]                                        # collapse [x] -> x for single-shard path

    import torch

    # Startup phase logging. Per-shard cold-start (CUDA init, OCIO config
    # first-load, OIIO plugin discovery, probe frame) can collectively take
    # tens of seconds before `rp.load_files` yields its first frame and the
    # progress bar starts ticking. Without these prints, the user sees a long
    # silence after the bash audit block and has no idea where the time goes.
    _startup_t0 = time.perf_counter()
    _shard_tag = "[" + str(device) + "]"
    def _phase(msg):
        console_print(_shard_tag + " " + msg + " (+" + str(round(time.perf_counter() - _startup_t0, 2)) + "s)")

    if isinstance(exr_paths, str):
        if rp.is_a_folder(exr_paths):
            exr_paths = rp.get_all_paths(exr_paths, file_extension_filter="exr", sort_by="number")
        else:
            exr_paths = rp.sorted_by_number(glob.glob(exr_paths))
    if not exr_paths:
        raise ValueError("exr_paths is empty")

    _phase("warming CUDA / picking device")
    dev = _pick_device(device)

    _phase("baking OCIO 3D LUT (" + str(lut_size) + "^3) to " + str(dev))
    lut_3d = _bake_lut_3d(src_colorspace, dev, lut_size)

    if _probe is not None:
        # Fanout parent already probed; skip _read_header + frame probe entirely.
        fps, pixel_aspect, out_h, out_w = _probe
        _phase("reusing probe from parent (fps=" + str(fps) + " out=" + str(out_w) + "x" + str(out_h) + ")")
    else:
        _phase("reading first EXR header (OIIO plugin discovery)")
        header_fps, pixel_aspect = _read_header(exr_paths[0])
        if fps is None:
            fps = header_fps
        if not unsquash:
            pixel_aspect = 1.0

        _phase("running probe frame to resolve output dims")
        # Probe frame 0 through the geometry stages to determine ffmpeg input dims.
        # Mirror the per-frame HWC↔CHW wrap so user transforms see CHW here too.
        from einops import rearrange as _probe_rearrange
        probe = torch.from_numpy(_read_image(exr_paths[0])).to(dev)
        if pre_unsquash_frame_transform is not None:
            probe = _probe_rearrange(pre_unsquash_frame_transform(_probe_rearrange(probe, "h w c -> c h w")), "c h w -> h w c")
        probe = _unsquash_gpu(probe, pixel_aspect)
        if frame_transform is not None:
            probe = _probe_rearrange(frame_transform(_probe_rearrange(probe, "h w c -> c h w")), "c h w -> h w c")
        out_h, out_w = probe.shape[:2]
        out_h, out_w = rp.r._round_dimensions_to_even(out_h, out_w)
        del probe

    n = len(exr_paths)
    _phase("startup done; output=" + str(out_w) + "x" + str(out_h) + " frames=" + str(n) + " — starting encode")

    codec_extras = {
        "libx264":    ("-x264-params", "threads=0:lookahead-threads=auto"),
        "libaom-av1": ("-row-mt", "1", "-cpu-used", "4"),
    }
    extra = (*codec_extras.get(codec, ()), *ffmpeg_extra_args)

    if not show_progress:
        console_print(
            "frames=" + str(n)
            + " num_threads=" + str(num_threads)
            + " device=" + str(dev)
            + " codec=" + codec
            + " pixel_aspect=" + str(pixel_aspect)
            + " output=" + str(out_w) + "x" + str(out_h)
            + " fps=" + str(fps)
        )

    if not overwrite and rp.file_exists(out_path):
        raise FileExistsError("out_path already exists and overwrite=False: " + out_path)
    rp.make_parent_directory(out_path)

    collect_metadata = meta_path is not None
    if collect_metadata:
        if not overwrite and rp.file_exists(meta_path):
            raise FileExistsError("meta_path already exists and overwrite=False: " + meta_path)
        rp.make_parent_directory(meta_path)

    # The temp file must share out_path's extension: ffmpeg picks the muxer from
    # the extension, so a hardcoded "mp4" here would mux MP4 then rename it to
    # .mov — a mislabeled container.
    encode_path = rp.temporary_file_path(rp.get_file_extension(out_path)) if atomic else out_path
    meta_encode_path = (rp.temporary_file_path("jsonl") if atomic else meta_path) if collect_metadata else None
    if not atomic:
        rp.delete_file(out_path, strict=False)

    cmd = _ffmpeg_command(encode_path, fps, out_w, out_h,
                          codec=codec, crf=crf, preset=preset,
                          pix_fmt=pix_fmt, extra_args=extra)
    progress = "eta:exr to mp4" if show_progress is True else show_progress

    fn = partial(
        _process_frame,
        frame_transform=frame_transform,
        pre_unsquash_frame_transform=pre_unsquash_frame_transform,
        pixel_aspect=pixel_aspect, out_h=out_h, out_w=out_w,
        clip=clip, lut_3d=lut_3d, device=dev,
        strict=strict, collect_metadata=collect_metadata,
    )

    # Wrap the per-frame stream with the bad-frame policy. _process_frame
    # returns None when `strict != 'strict'` and OIIO fails; the wrapper
    # decides what (if anything) goes to ffmpeg for those Nones.
    _bad_frame_wrap = {
        "strict": _strict_bad_frame_stream,
        "skip":   _skip_bad_frame_stream,
        "pad":    lambda s: _pad_bad_frame_stream(s, out_w=out_w, out_h=out_h),
    }[strict]

    started = time.perf_counter()
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    meta_file = None
    try:
        assert proc.stdin is not None
        stream = rp.load_files(
            fn, exr_paths,
            num_threads=num_threads,
            buffer_limit=buffer_limit,
            show_progress=progress,
            lazy=True,
        )
        if collect_metadata:
            # Tee sits upstream of the bad-frame policy: it writes one JSON
            # line per INPUT frame (in order) and passes plain bytes|None on,
            # so 'skip'/'pad' still see the stream shape they expect.
            meta_file = open(meta_encode_path, "w")
            stream = _metadata_tee_stream(stream, meta_file)
        for frame_bytes in _bad_frame_wrap(stream):
            proc.stdin.write(frame_bytes)
        proc.stdin.close()
        if meta_file is not None:
            meta_file.close()
        rc = proc.wait()
    except Exception:
        proc.kill()
        proc.wait()
        if meta_file is not None and not meta_file.closed:
            meta_file.close()
        if atomic:
            rp.delete_file(encode_path, strict=False)
            if collect_metadata:
                rp.delete_file(meta_encode_path, strict=False)
        raise
    elapsed = time.perf_counter() - started
    if rc != 0:
        if atomic:
            rp.delete_file(encode_path, strict=False)
            if collect_metadata:
                rp.delete_file(meta_encode_path, strict=False)
        raise RuntimeError("ffmpeg failed with exit " + str(rc))
    if atomic:
        rp.delete_file(out_path, strict=False)
        rp.move_path(encode_path, out_path)
        if collect_metadata:
            rp.delete_file(meta_path, strict=False)
            rp.move_path(meta_encode_path, meta_path)
    if not show_progress:
        console_print("elapsed_seconds=" + str(round(elapsed, 3)))
        console_print("fps_processed=" + str(round(n / elapsed, 3)))
        console_print("out=" + out_path)
