# https://gist.github.com/SqrtRyan/719c46b275db344ec4bd9f1bcc82945c

import glob
import subprocess
import threading
import time
from functools import partial

import numpy as np
import rp


OCIO_CONFIG = "studio-config-v4.0.0_aces-v2.0_ocio-v2.5"
DST_DISPLAY = "Rec.1886 Rec.709 - Display"          # output is locked to Rec.709 SDR
DST_VIEW = "ACES 2.0 - SDR 100 nits (Rec.709)"
PRINT_STYLE = "bold orange"                          # used for every line we emit via console_print


def console_print(text):
    # Wrapper around rp.fansi_print so the rp attribute lookup is deferred to call time
    # (a module-level `partial(rp.fansi_print, ...)` would break when this file is imported
    # mid-load by rp.r — `rp.fansi_print` may not exist yet at that point).
    rp.fansi_print(text, text_color=PRINT_STYLE)

_thread_state = threading.local()


def _read_header(path):
    """Read framesPerSecond and PixelAspectRatio from an EXR header (defaults: 24.0, 1.0)."""
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


def _unsquash(image, pixel_aspect):
    """Stretch image width by pixel_aspect so pixels become square. No-op for PAR == 1.0."""
    if pixel_aspect == 1.0:
        return image
    import cv2
    h, w = image.shape[:2]
    return cv2.resize(image, (int(round(w * pixel_aspect)), h), interpolation=cv2.INTER_CUBIC)


def _get_processor(src_colorspace):
    # OCIO processor construction is expensive (~50ms); cache per worker thread, keyed by src_colorspace.
    import PyOpenColorIO as ocio
    cache = getattr(_thread_state, "processors", None)
    if cache is None:
        _thread_state.processors = cache = {}
    if src_colorspace not in cache:
        config = ocio.Config.CreateFromBuiltinConfig(OCIO_CONFIG)
        transform = ocio.DisplayViewTransform(src=src_colorspace, display=DST_DISPLAY, view=DST_VIEW)
        cache[src_colorspace] = config.getProcessor(transform).getDefaultCPUProcessor()
    return cache[src_colorspace]


def _read_image(path):
    import OpenImageIO as oiio
    inp = oiio.ImageInput.open(path)
    if inp is None:
        raise RuntimeError("Could not open " + path)
    try:
        image = inp.read_image(format=oiio.FLOAT)
    finally:
        inp.close()
    if image is None:
        raise RuntimeError("Could not read " + path)
    return image


def _process_frame(path, *, frame_transform, src_colorspace, pixel_aspect, out_h, out_w):
    image = _read_image(path)
    image = _unsquash(image, pixel_aspect)                 # anamorphic → square pixels, before any user transform
    if frame_transform is not None:
        image = frame_transform(image)
    image = image[:out_h, :out_w]                          # crop to announced even dims if transform left odd
    image = np.ascontiguousarray(image, dtype=np.float32)
    _get_processor(src_colorspace).applyRGB(image)
    image = np.clip(image, 0.0, 1.0)
    return (image * 65535.0 + 0.5).astype("<u2", copy=False).tobytes()


def _ffmpeg_command(out_path, fps, out_w, out_h, *, codec, crf, preset, pix_fmt, extra_args):
    # Color metadata is locked to Rec.709 SDR / bt709 / TV-range to match the OCIO output.
    return [
        "ffmpeg", "-hide_banner", "-nostats", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb48le",
        "-s", str(out_w) + "x" + str(out_h), "-r", str(fps),
        "-i", "-",
        "-vf", "format=" + pix_fmt,
        "-c:v", codec, "-preset", preset, "-crf", str(crf),
        *extra_args,
        "-color_primaries", "bt709", "-color_trc", "bt709",
        "-colorspace", "bt709", "-color_range", "tv",
        "-movflags", "+faststart",
        out_path,
    ]


def exr_to_mp4(
    exr_paths,
    out_path,
    *,
    frame_transform=None,           # callable(HWC float) -> HWC float; None = identity (no resize/flip/crop)
    overwrite=True,                 # if False, raise FileExistsError when out_path already exists instead of clobbering it
    fps=None,                       # None = use EXR header's framesPerSecond (fallback 24); pass a float to override
    src_colorspace="ACES2065-1",    # OCIO source; output is locked to Rec.709 SDR
    num_threads=10,                 # parallel EXR reader / OCIO worker threads
    buffer_limit=None,              # max in-flight frames; None = num_threads (rp default)
    show_progress=True,             # True = "eta:exr to mp4" bar; False = silent; or pass any rp.load_files-style str ("eta:My Title", "tqdm")
    codec="libx264",                # ffmpeg encoder: libx264, libx265, libsvtav1, libaom-av1, ...
    crf=20,                         # quality, lower = better/larger. x264/265 ~20, AV1 ~30
    preset="ultrafast",             # speed/quality. x264/265 ultrafast..veryslow; svtav1 "0".."13"
    pix_fmt="yuv420p10le",          # output pixel format; drives bit depth & chroma (yuv420p / yuv420p10le / yuv420p12le / yuv444p10le ...)
    ffmpeg_extra_args=(),           # extra ffmpeg flags for codec-specific tuning, e.g. ("-svtav1-params", "tune=0:film-grain=8")
    unsquash=True                   # custom flag (see docstring): undo anamorphic squash from EXR's PixelAspectRatio header. No-op for square-pixel EXRs.
):
    """
    Convert a sequence of EXR frames to an MP4. EXRs are tone-mapped from
    `src_colorspace` to Rec.709 SDR via OCIO (using the ACES 2.0 SDR view),
    then piped raw to ffmpeg for encoding. Output color metadata is locked to
    Rec.709 / bt709 / TV-range so players interpret the pixels correctly.

    Performance:
        EXR reads + OCIO transforms run in parallel across `num_threads`
        Python threads (the GIL is released during EXR disk I/O and the
        C-implemented OCIO `applyRGB` call). Encoded frames stream lazily
        into ffmpeg's stdin as raw rgb48le bytes; ffmpeg runs as a separate
        OS process with its own internal codec threading.

        There is no Python-side wrapper around the encoder — no PyAV, no
        imageio-ffmpeg, no cv2.VideoWriter — so the only data crossing the
        Python ↔ ffmpeg boundary is the raw pixel buffer through an OS pipe.
        That gives three independent parallelism layers (disk read fan-out,
        OCIO compute, codec encode) running concurrently, and throughput is
        bounded by whichever of disk-bandwidth / OCIO-CPU / encoder-CPU
        saturates first rather than by interpreter overhead.

        Requires the `ffmpeg` binary on the system PATH
        (e.g. `brew install ffmpeg` / `apt install ffmpeg`).

    Args:
        exr_paths: The EXR sequence to convert. Accepts:
            - a list of EXR file path strings (used as-is, in order)
            - a folder path string (all .exr files inside, sorted by frame
              number)
            - a glob pattern string (expanded, sorted by frame number)
        out_path: Output .mp4 file path. The parent directory is created if
            missing. An existing file at this path is deleted and replaced
            unless `overwrite=False` (in which case `FileExistsError` is
            raised).
        frame_transform: Optional callable applied to each loaded EXR after
            `unsquash` and before the OCIO transform. Signature
            `(HWC float ndarray) -> (HWC float ndarray)`. None = identity
            (no resize/crop/flip). The first frame's transformed dimensions
            determine the output video size (rounded down to even).
        overwrite: If True (default), an existing file at `out_path` is
            deleted and re-encoded. If False, raise `FileExistsError` when
            `out_path` already exists instead of clobbering it.
        fps: Output framerate. `None` (default) = read from the first EXR's
            `framesPerSecond` header attribute, falling back to 24 if absent.
            Pass a float to override.
        src_colorspace: OCIO source colorspace name. Default "ACES2065-1".
            Output is always Rec.709 SDR — that side is locked because the
            ffmpeg color metadata tags would have to change in lockstep with
            any output colorspace change.
        num_threads: Parallel EXR reader / OCIO worker threads. Each worker
            reads one frame from disk and runs the OCIO transform on it.
            Default 10.
        buffer_limit: Maximum in-flight processed frames buffered ahead of
            ffmpeg's stdin consumer. None = use `num_threads` (rp's
            `lazy_par_map` default).
        show_progress: Progress bar control. `True` (default) shows
            `"eta:exr to mp4"`; `False` is silent; or pass any
            `rp.load_files`-style string (`"eta:My Title"`, `"tqdm"`).
        codec: ffmpeg encoder name. Tested: `"libx264"` (default),
            `"libx265"`, `"libsvtav1"`, `"libaom-av1"`. Other codecs work
            but the default `crf`/`preset` values are tuned for libx264.
        crf: Constant Rate Factor — quality knob. Lower = better quality,
            larger file. libx264/265: 0-51, ~20 looks good.
            libsvtav1/libaom-av1: 0-63, ~30 looks good.
        preset: Speed/quality tradeoff. libx264/265:
            `"ultrafast"`..`"veryslow"`. libsvtav1: `"0"`..`"13"` (higher =
            faster).
        pix_fmt: Output pixel format. Drives bit depth and chroma
            subsampling. Common values: `"yuv420p"` (8-bit, max compat),
            `"yuv420p10le"` (10-bit, default), `"yuv420p12le"` (12-bit,
            libx265 / AV1 only), `"yuv444p10le"` (full chroma resolution).
            libx264 auto-selects the right profile from this.
        ffmpeg_extra_args: Tuple of extra flag/value strings appended to
            the ffmpeg command for codec-specific tuning. Examples:
            `("-svtav1-params", "tune=0:film-grain=8")`, `("-tiles", "2x2")`.
            Auto-applied per-codec (this kwarg appends on top):
              - libx264: `("-x264-params", "threads=0:lookahead-threads=auto")`
              - libaom-av1: `("-row-mt", "1", "-cpu-used", "4")` (libaom's
                stock defaults are single-threaded and ~10-100x slower).
            libsvtav1 and libx265 get nothing automatic (their defaults are
            already sane).
        unsquash: Undo anamorphic squash by stretching each frame horizontally
            to match its EXR header's `PixelAspectRatio`. Default True.
            No-op for square-pixel EXRs.

            This is a CUSTOM, script-specific flag, not a generic ffmpeg/OCIO
            concept. Background:

                Anamorphic source — typically from cinema lenses, wide-format
                renders, or legacy DV/NTSC formats — stores a non-square
                pixel grid plus a `PixelAspectRatio` (PAR) attribute in the
                EXR header indicating how much to stretch each pixel
                horizontally for correct display. For example, a 2:1
                anamorphic shot might be stored as 960x1080 with PAR=2.0,
                meaning the intended display size is 1920x1080. Dumping
                those pixels straight to a square-pixel MP4 produces a
                horizontally-squashed image.

                With `unsquash=True` (default), this function reads
                `PixelAspectRatio` from the first EXR header and
                pre-stretches every frame horizontally by that factor (via
                `cv2.resize`, cubic interpolation) BEFORE passing the image
                to `frame_transform`. So `frame_transform` always sees
                square-pixel geometry and never has to know or care about
                anamorphic source. For square-pixel EXRs (PAR=1.0, the
                common case) this is a complete no-op: no resize, no
                overhead, no extra allocations.

                Set `unsquash=False` only if you want raw non-square pixels
                passed through unchanged and you'll handle the aspect math
                yourself inside `frame_transform`.

                The PAR is read once from the first EXR and applied to all
                frames. If your sequence mixes PARs (very unusual) you'd
                need to handle it in `frame_transform` with `unsquash=False`.

    Recipes (codec + bit-depth combos — copy-paste these kwargs):

        # 8-bit H.264 (max compatibility, smallest CPU)
        codec="libx264", pix_fmt="yuv420p", crf=23

        # 10-bit H.264 (default — best balance of quality and compatibility)
        codec="libx264", pix_fmt="yuv420p10le", crf=20

        # 12-bit H.265 (archival; libx264 caps at 10-bit so 12-bit needs libx265 or AV1)
        codec="libx265", pix_fmt="yuv420p12le", crf=20, preset="medium"

        # 8-bit AV1 via SVT-AV1 (fast modern encode)
        codec="libsvtav1", pix_fmt="yuv420p", crf=30, preset="6"

        # 10-bit AV1 via SVT-AV1
        codec="libsvtav1", pix_fmt="yuv420p10le", crf=30, preset="6"

        # 12-bit AV1 via libaom-av1 (SVT-AV1 caps at 10-bit; libaom is slower)
        # (-row-mt 1 and -cpu-used 4 are auto-applied for libaom-av1 — see codec_extras)
        codec="libaom-av1", pix_fmt="yuv420p12le", crf=28, preset="medium"

    Examples:

        # Default: H.264 10-bit, source resolution (with anamorphic unsquash if applicable)
        exr_to_mp4(paths, "out.mp4")

        # Resize to 480p (matches the legacy CLI's default behavior)
        from functools import partial
        exr_to_mp4(paths, "out.mp4",
                   frame_transform=partial(rp.resize_image_to_fit, height=480))

        # AV1 via SVT-AV1
        exr_to_mp4(paths, "out.mp4", codec="libsvtav1", crf=30, preset="6")

        # 8-bit fast preview
        exr_to_mp4(paths, "out.mp4", pix_fmt="yuv420p", crf=23)

        # Non-ACES source colorspace (any OCIO ACES Studio config name works)
        exr_to_mp4(paths, "out.mp4", src_colorspace="Linear ARRI Wide Gamut 3")

        # Vertical flip via frame_transform
        exr_to_mp4(paths, "out.mp4", frame_transform=np.flipud)

        # Pass a folder of EXRs directly (auto-sorted by frame number)
        exr_to_mp4("/renders/shot_010", "out.mp4")

        # Or a glob pattern
        exr_to_mp4("/renders/shot_010/*.exr", "out.mp4")

        # Silent / custom progress
        exr_to_mp4(paths, "out.mp4", show_progress=False)
        exr_to_mp4(paths, "out.mp4", show_progress="eta:shot_010")
    """
    # Ensure runtime deps (no-op if already installed); kept inside the public
    # function so importing this module is cheap and the only entry point that
    # touches OIIO / OCIO / cv2 / ffmpeg is the one that asks for them.
    rp.pip_import("OpenImageIO")
    rp.pip_import("PyOpenColorIO")
    rp.pip_import("cv2")
    rp.r._ensure_ffmpeg_installed()

    # Mirror rp.save_video_mp4's input dispatch: folder | glob | list-of-paths.
    if isinstance(exr_paths, str):
        if rp.is_a_folder(exr_paths):
            exr_paths = rp.get_all_paths(exr_paths, file_extension_filter="exr", sort_by="number")
        else:
            exr_paths = rp.sorted_by_number(glob.glob(exr_paths))
    if not exr_paths:
        raise ValueError("exr_paths is empty")

    header_fps, pixel_aspect = _read_header(exr_paths[0])
    if fps is None:
        fps = header_fps
    if not unsquash:
        pixel_aspect = 1.0

    # Probe frame 0 through the same pre-transform pipeline to determine ffmpeg output dims.
    probe = _unsquash(_read_image(exr_paths[0]), pixel_aspect)
    if frame_transform is not None:
        probe = frame_transform(probe)
    out_h, out_w = probe.shape[:2]
    out_h, out_w = rp.r._round_dimensions_to_even(out_h, out_w)
    n = len(exr_paths)

    # Per-codec defaults that we always want unless overridden in ffmpeg_extra_args:
    #   - libx264: explicit threading params (matches libx264's own defaults but kept for the
    #     perf this script was tuned for).
    #   - libaom-av1: row-mt + a usable cpu-used. libaom's defaults are notoriously bad
    #     (single-threaded, cpu-used=1) and would otherwise encode 10-100x slower than necessary.
    #     libsvtav1 has sensible defaults so it gets nothing extra.
    codec_extras = {
        "libx264":    ("-x264-params", "threads=0:lookahead-threads=auto"),
        "libaom-av1": ("-row-mt", "1", "-cpu-used", "4"),
    }
    extra = (*codec_extras.get(codec, ()), *ffmpeg_extra_args)

    if not show_progress:
        console_print(
            "frames=" + str(n)
            + " num_threads=" + str(num_threads)
            + " codec=" + codec
            + " pixel_aspect=" + str(pixel_aspect)
            + " output=" + str(out_w) + "x" + str(out_h)
            + " fps=" + str(fps)
        )

    if not overwrite and rp.file_exists(out_path):
        raise FileExistsError("out_path already exists and overwrite=False: " + out_path)
    rp.make_parent_directory(out_path)
    rp.delete_file(out_path, strict=False)

    cmd = _ffmpeg_command(out_path, fps, out_w, out_h,
                          codec=codec, crf=crf, preset=preset,
                          pix_fmt=pix_fmt, extra_args=extra)
    progress = "eta:exr to mp4" if show_progress is True else show_progress
    fn = partial(_process_frame,
                 frame_transform=frame_transform, src_colorspace=src_colorspace,
                 pixel_aspect=pixel_aspect, out_h=out_h, out_w=out_w)

    started = time.perf_counter()
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    try:
        assert proc.stdin is not None
        stream = rp.load_files(
            fn, exr_paths,
            num_threads=num_threads,
            buffer_limit=buffer_limit,
            show_progress=progress,
            lazy=True,
        )
        for frame_bytes in stream:
            proc.stdin.write(frame_bytes)
        proc.stdin.close()
        rc = proc.wait()
    except Exception:
        proc.kill()
        proc.wait()
        raise
    elapsed = time.perf_counter() - started
    if rc != 0:
        raise RuntimeError("ffmpeg failed with exit " + str(rc))
    if not show_progress:
        console_print("elapsed_seconds=" + str(round(elapsed, 3)))
        console_print("fps_processed=" + str(round(n / elapsed, 3)))
        console_print("out=" + out_path)
