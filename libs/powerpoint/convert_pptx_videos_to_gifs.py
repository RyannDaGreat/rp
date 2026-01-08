"""
Convert PowerPoint videos to GIFs with target file size.
"""

import re
import tempfile

import rp

from . import google_slides_upload as gsu
from .pptx_utils import get_video_placements, get_thumbnail_mappings


# --- Slide selection helpers ---

def _parse_slides(slides: str) -> set[int]:
    """
    Parse slide range string into set of 1-indexed slide numbers.

    >>> _parse_slides("1-5")
    {1, 2, 3, 4, 5}
    >>> _parse_slides("1,3,7-10")
    {1, 3, 7, 8, 9, 10}
    >>> _parse_slides("5")
    {5}
    """
    result = set()
    for part in slides.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-', 1)
            result.update(range(int(start), int(end) + 1))
        else:
            result.add(int(part))
    return result


def _get_slide_video_mapping(placements: dict) -> dict[int, list[str]]:
    """
    Get mapping of slide number -> list of video filenames on that slide.

    >>> placements = {'media1.mp4': [type('P', (), {'slide_number': 1})()]}
    >>> _get_slide_video_mapping(placements)
    {1: ['media1.mp4']}
    """
    slide_to_videos: dict[int, list[str]] = {}
    for video_name, places in placements.items():
        for p in places:
            slide_to_videos.setdefault(p.slide_number, []).append(video_name)
    return slide_to_videos


def _count_slides(work_dir: str) -> int:
    """Count total number of slides in extracted PPTX."""
    slides_dir = rp.path_join(work_dir, 'ppt', 'slides')
    return len(rp.glob(rp.path_join(slides_dir, 'slide*.xml')))


def _filter_pptx_to_slides(work_dir: str, start: int, end: int):
    """
    Filter extracted PPTX to only include slides start..end (1-indexed, inclusive).
    Deletes slides outside range and updates presentation.xml.
    """
    slides_dir = rp.path_join(work_dir, 'ppt', 'slides')
    rels_dir = rp.path_join(slides_dir, '_rels')

    # Delete slides outside range
    for slide_xml in rp.glob(rp.path_join(slides_dir, 'slide*.xml')):
        slide_num = int(re.search(r'slide(\d+)\.xml', slide_xml).group(1))
        if not (start <= slide_num <= end):
            rp.delete_file(slide_xml)
            rp.delete_file(rp.path_join(rels_dir, f'slide{slide_num}.xml.rels'), strict=False)

    # Update presentation.xml and rels to remove references to deleted slides
    pres_xml = rp.path_join(work_dir, 'ppt', 'presentation.xml')
    pres_rels = rp.path_join(work_dir, 'ppt', '_rels', 'presentation.xml.rels')
    content = rp.text_file_to_string(pres_xml)
    rels_content = rp.text_file_to_string(pres_rels)

    # Find rIds for deleted slides and remove from both files
    for match in re.finditer(r'<Relationship[^>]*Id="(rId\d+)"[^>]*Target="slides/slide(\d+)\.xml"', rels_content):
        rid, slide_num = match.group(1), int(match.group(2))
        if not (start <= slide_num <= end):
            content = re.sub(rf'<p:sldId[^>]*r:id="{rid}"[^>]*/>', '', content)
            rels_content = re.sub(rf'<Relationship[^>]*Id="{rid}"[^>]*/>', '', rels_content)

    rp.string_to_text_file(pres_xml, content)
    rp.string_to_text_file(pres_rels, rels_content)


def _delete_unused_media(work_dir: str):
    """Delete media files not referenced by any remaining slides."""
    media_dir = rp.path_join(work_dir, 'ppt', 'media')
    if not rp.folder_exists(media_dir):
        return

    # Find all media referenced by slide rels
    used = set()
    for rels_file in rp.glob(rp.path_join(work_dir, 'ppt', 'slides', '_rels', '*.rels')):
        for match in re.finditer(r'Target="\.\./media/([^"]+)"', rp.text_file_to_string(rels_file)):
            used.add(match.group(1))

    for media_file in rp.get_all_files(media_dir):
        if rp.get_file_name(media_file) not in used:
            rp.delete_file(media_file)


def _estimate_slide_gif_sizes(
    slide_to_videos: dict[int, list[str]],
    video_info: dict,
    fps: int,
    dithered: bool,
) -> dict[int, int]:
    """Estimate GIF size in bytes for each slide at DPI=100."""
    DPI = 100
    sizes = {}
    for slide_num, videos in slide_to_videos.items():
        total = 0
        for name in videos:
            info = video_info.get(name)
            if not info or not info.get('visible_size'):
                continue
            vis_w, vis_h = info['visible_size']
            w, h = int(vis_w * DPI), int(vis_h * DPI)
            frames = info['num_frames']
            if fps < info['fps']:
                frames = int(frames * fps / info['fps'])
            total += _estimate_gif_size(w, h, frames, dithered)
        sizes[slide_num] = total
    return sizes


def _partition_slides_contiguous(num_slides: int, slide_sizes: dict[int, int], num_parts: int) -> list[tuple[int, int]]:
    """
    Partition slides 1..num_slides into num_parts contiguous ranges with roughly equal GIF sizes.
    Returns list of (start, end) tuples (1-indexed, inclusive).

    >>> _partition_slides_contiguous(10, {1: 100, 5: 100, 10: 100}, 2)
    [(1, 5), (6, 10)]
    >>> _partition_slides_contiguous(6, {1: 100, 2: 100, 3: 100, 4: 100, 5: 100, 6: 100}, 3)
    [(1, 2), (3, 4), (5, 6)]
    """
    if num_parts >= num_slides:
        return [(i, i) for i in range(1, num_slides + 1)]

    # Build cumulative size array for slides 1..num_slides
    cumsum = [0] * (num_slides + 1)
    for i in range(1, num_slides + 1):
        cumsum[i] = cumsum[i - 1] + slide_sizes.get(i, 0)

    total = cumsum[num_slides]
    target_per_part = total / num_parts

    parts = []
    start = 1
    for part_idx in range(num_parts - 1):
        target_cumsum = cumsum[start - 1] + target_per_part
        # Find best split point
        best_end = start
        best_diff = float('inf')
        for end in range(start, num_slides - (num_parts - part_idx - 1) + 1):
            diff = abs(cumsum[end] - target_cumsum)
            if diff < best_diff:
                best_diff = diff
                best_end = end
        parts.append((start, best_end))
        start = best_end + 1

    # Last part gets the rest
    parts.append((start, num_slides))
    return parts


# --- Core conversion logic ---

def convert_pptx_videos_to_gifs(
    input_pptx: str,
    output_pptx: str = None,
    target_size: str = '100MB',
    fps: int = 10,
    dpi_iters: int = 5,
    dither: bool = True,
    slides: str = None,
    num_parts: int = 1,
    upload: bool = False,
) -> str:
    """
    Convert PowerPoint videos to GIFs, targeting a file size via DPI bisection.

    DPI = PPI (pixels per inch of display size).

    Examples:
        python convert_pptx_videos_to_gifs.py presentation.pptx
        python convert_pptx_videos_to_gifs.py presentation.pptx --target_size 50MB
        python convert_pptx_videos_to_gifs.py presentation.pptx --slides 1-10 --num_parts 3
        python convert_pptx_videos_to_gifs.py presentation.pptx output.pptx --target_size 80MB

    Args:
        input_pptx: Path to input PowerPoint file.
        output_pptx: Output path. If None, creates <input_stem>_gifs_<target_size>.pptx in the
            same directory as input, with a unique suffix if the file already exists.
        target_size: Target file size. Accepts strings like '100MB', '50MB', '1GiB', or an integer
            for bytes. Uses decimal MB by default (1MB = 1,000,000 bytes) to match Finder/Google.
            Note: Google Slides has a 100MB upload limit. Default: '100MB'.
        fps: Target frame rate. Output fps will be <= this value, never greater (frames are
            only dropped, never duplicated). Use a high value like 10000 to keep all original
            frames. Default: 10.
        dpi_iters: Number of DPI bisection search iterations. More iterations = finer-grained
            search for optimal quality within target size. Default: 5.
        dither: If True (default), use FFmpeg for GIF creation with dithering (better color
            accuracy, larger files). If False, use PIL without dithering (smaller files, may
            have color banding).
        slides: Slide range to process (e.g., "1-5", "1,3,7-10"). If None, process all slides.
        num_parts: Number of output files to create. If > 1, splits slides into N parts
            (partitioned by estimated GIF size), each getting its own DPI bisection search.
            Returns folder path containing part1.pptx, part2.pptx, etc. Default: 1.
        upload: If True, upload to Google Slides. If num_parts > 1, also merges all
            parts into one presentation. Requires OAuth setup (first run opens browser).
            Creates on Drive (e.g. <name>=MyPresentation, <size>=50MB):
              MyDrive/
                <name>_gifs_<size>/        <- new folder
                  <name>_gifs_<size>_part1 <- Google Slides (converted)
                  <name>_gifs_<size>_part2
                  ...
                  <name>                   <- merged presentation (all slides)

    Returns:
        Path to output file/folder, or dict with upload results if upload=True.
    """
    if not rp.file_exists(input_pptx):
        raise FileNotFoundError(f"Input not found: {input_pptx}")

    target_bytes = rp.string_to_file_size(target_size, always_mib=False)

    # Parse slide selection
    selected_slides = _parse_slides(slides) if slides else None

    # Generate output path/folder name
    if output_pptx is None:
        stem = rp.get_file_name(input_pptx, include_file_extension=False)
        base_name = f'{stem}_gifs_{target_size}'
        if num_parts > 1:
            output_folder = rp.get_unique_copy_path(rp.with_file_name(input_pptx, base_name, keep_extension=False))
        else:
            output_pptx = rp.get_unique_copy_path(rp.with_file_name(input_pptx, base_name))

    rp.fansi_print(f"Converting: {rp.get_file_name(input_pptx)}", 'cyan', 'bold')
    rp.fansi_print(f"Target: {rp.human_readable_file_size(target_bytes, mib=False)}, FPS: {fps}", 'cyan')
    if selected_slides:
        rp.fansi_print(f"Slides: {slides}", 'cyan')
    if num_parts > 1:
        rp.fansi_print(f"Splitting into {num_parts} parts", 'cyan')

    with tempfile.TemporaryDirectory() as tmpdir:
        work_dir = rp.path_join(tmpdir, 'work')

        # Analyze source
        rp.unzip_to_folder(input_pptx, work_dir, treat_as='zip')
        placements = get_video_placements(work_dir)
        thumb_map = get_thumbnail_mappings(work_dir)['thumbnail_mappings']
        video_info = _get_video_info(work_dir, placements)

        # Build slide -> videos mapping
        slide_to_videos = _get_slide_video_mapping(placements)

        # Filter by selected slides if specified
        if selected_slides:
            slide_to_videos = {s: v for s, v in slide_to_videos.items() if s in selected_slides}
            # Filter video_info to only videos on selected slides
            selected_videos = set()
            for videos in slide_to_videos.values():
                selected_videos.update(videos)
            video_info = {k: v for k, v in video_info.items() if k in selected_videos}
            placements = {k: v for k, v in placements.items() if k in selected_videos}

        visible = {k: v for k, v in video_info.items() if v['visible_size']}
        offscreen = [k for k, v in video_info.items() if not v['visible_size']]

        rp.fansi_print(f"Videos: {len(visible)} visible, {len(offscreen)} offscreen (will delete)", 'white')

        if not visible:
            rp.fansi_print("No visible videos - nothing to convert", 'yellow')
            return input_pptx

        # Multi-output: partition slides into contiguous ranges and process each part
        if num_parts > 1:
            num_slides = _count_slides(work_dir)
            slide_sizes = _estimate_slide_gif_sizes(slide_to_videos, video_info, fps, dither)
            partitions = _partition_slides_contiguous(num_slides, slide_sizes, num_parts)

            # Print partition plan
            total_est = sum(slide_sizes.values())
            rp.fansi_print(f"Total slides: {num_slides}", 'white')
            rp.fansi_print(f"Partition plan ({num_parts} parts):", 'white')
            for i, (start, end) in enumerate(partitions, 1):
                part_size = sum(slide_sizes.get(s, 0) for s in range(start, end + 1))
                pct = 100 * part_size / total_est if total_est else 0
                rp.fansi_print(f"  Part {i}: slides {start}-{end} (~{pct:.0f}% of GIF data)", 'white')

            rp.make_directory(output_folder)
            folder_stem = rp.get_file_name(output_folder)

            for i, (start, end) in enumerate(partitions, 1):
                part_name = f'{folder_stem}_part{i}.pptx'
                part_path = rp.path_join(output_folder, part_name)
                rp.fansi_print(f"\n{'='*60}", 'magenta')
                rp.fansi_print(f"Part {i}/{len(partitions)}: slides {start}-{end}", 'magenta', 'bold')

                # Get videos for this partition (slides in range start..end inclusive)
                part_videos = set()
                for s in range(start, end + 1):
                    part_videos.update(slide_to_videos.get(s, []))
                part_visible = {k: v for k, v in visible.items() if k in part_videos}
                part_offscreen = [k for k in offscreen if k in part_videos]

                if not part_visible:
                    rp.fansi_print(f"No videos in part {i}, skipping", 'yellow')
                    continue

                _convert_single(
                    input_pptx, part_path, target_bytes, fps, dpi_iters, dither,
                    part_visible, part_offscreen, thumb_map, tmpdir, work_dir,
                    slide_range=(start, end)
                )

            rp.fansi_print(f"\n{'='*60}", 'green')
            rp.fansi_print(f"Created folder: {output_folder}", 'green', 'bold')

            if upload:
                rp.fansi_print("\nUploading to Google Slides...", 'cyan', 'bold')
                folder_name = rp.get_file_name(output_folder)
                merged_name = rp.get_file_name(input_pptx, include_file_extension=False)
                import sys
                import shlex
                cmd = '%s -m rp.libs.powerpoint upload %s --folder-name %s --merged-name %s' % (
                    shlex.quote(sys.executable),
                    shlex.quote(output_folder),
                    shlex.quote(folder_name),
                    shlex.quote(merged_name),
                )
                rp.fansi_print("Running: " + cmd, 'cyan')
                rp.r._run_sys_command(cmd)

            return output_folder

        # Single output
        _convert_single(
            input_pptx, output_pptx, target_bytes, fps, dpi_iters, dither,
            visible, offscreen, thumb_map, tmpdir, work_dir
        )

    if upload:
        rp.fansi_print(f"\nUploading to Google Slides...", 'cyan', 'bold')
        result = gsu.upload_and_merge_pptx([output_pptx])
        rp.fansi_print(f"\n{'='*60}", 'green')
        rp.fansi_print(f"Local file: {output_pptx}", 'green')
        rp.fansi_print(f"Drive folder: {result['folder_url']}", 'green')
        rp.fansi_print(f"Presentation: {result['merged']['url']}", 'green', 'bold')
        return {'local_file': output_pptx, **result}

    return output_pptx


def _convert_single(
    input_pptx: str,
    output_pptx: str,
    target_bytes: int,
    fps: int,
    dpi_iters: int,
    dither: bool,
    visible: dict,
    offscreen: list,
    thumb_map: dict,
    tmpdir: str,
    work_dir: str,
    slide_range: tuple[int, int] = None,
):
    """Convert a single PPTX with the given visible videos.

    If slide_range is provided as (start, end), only include those slides.
    """
    # Estimate initial DPI (use a rough base estimate for now, will measure accurately per attempt)
    initial_dpi = _estimate_initial_dpi(visible, target_bytes, fps, dithered=dither, base_pptx_bytes=0)
    rp.fansi_print(f"Estimated initial DPI: {initial_dpi}", 'white')

    # Build test function that tries a DPI and returns path if under target
    attempt_counter = [0]
    def try_dpi(dpi: int):
        attempt_counter[0] += 1
        rp.fansi_print(f"\nIteration {attempt_counter[0]}/{dpi_iters}: DPI={dpi}", 'blue', 'bold')

        rp.delete_all_paths_in_folder(work_dir)
        rp.unzip_to_folder(input_pptx, work_dir, treat_as='zip')

        # Filter to slide range if specified
        if slide_range:
            _filter_pptx_to_slides(work_dir, slide_range[0], slide_range[1])

        media_dir = rp.path_join(work_dir, 'ppt', 'media')
        replacements = {}
        for name, info in rp.eta(visible.items(), title='Creating GIFs'):
            if name not in thumb_map:
                continue
            gif_name = _convert_video_to_gif(
                info['path'], media_dir, thumb_map[name],
                info['visible_size'], dpi, fps, info, dither
            )
            replacements[thumb_map[name]] = gif_name

        _apply_pptx_transformations(work_dir, replacements, offscreen, thumb_map)

        # Delete unused media (slides outside range, videos converted to GIF, etc.)
        _delete_unused_media(work_dir)

        temp_out = rp.path_join(tmpdir, f'attempt_{attempt_counter[0]}.pptx')
        _create_pptx(work_dir, temp_out)
        size = rp.get_file_size(temp_out)

        size_str = rp.human_readable_file_size(size, mib=False)
        target_str = rp.human_readable_file_size(target_bytes, mib=False)
        ok = size <= target_bytes
        rp.fansi_print(f"  Result: {size_str} {'<=' if ok else '>'} {target_str}", 'green' if ok else 'yellow')

        return temp_out if ok else None

    # Search for best DPI using geometric+bisection
    best_dpi, best_path = _find_max_satisfying(
        try_dpi, lo=10, hi=300, initial=initial_dpi, max_calls=dpi_iters
    )

    # Save best result
    if best_path:
        rp.copy_file(best_path, output_pptx)
        final_dpi = best_dpi
    else:
        _create_pptx(work_dir, output_pptx)
        final_dpi = 10  # fallback

    final_size = rp.get_file_size(output_pptx)
    rp.fansi_print(f"\nCreated: {output_pptx}", 'green', 'bold')
    rp.fansi_print(f"Final: {rp.human_readable_file_size(final_size, mib=False)} at DPI={final_dpi}", 'green')


# --- Utility functions ---

def _find_max_satisfying(test_fn, lo: int = 10, hi: int = 300, initial: int = None, max_calls: int = 5):
    """Find highest integer in [lo, hi] where test_fn returns truthy, using geometric+bisection.

    Args:
        test_fn: Function taking int, returning truthy on success, falsy on failure.
        lo, hi: Search bounds (inclusive).
        initial: Starting guess. If None, uses geometric mean of lo and hi.
        max_calls: Maximum number of test_fn calls.

    Returns:
        (best_value, best_result) or (None, None) if nothing satisfies.
    """
    calls = 0
    best = None

    def try_val(x):
        nonlocal calls
        calls += 1
        return test_fn(x)

    # Initial guess
    x = initial if initial is not None else int((lo * hi) ** 0.5)
    x = max(lo, min(hi, x))  # Clamp to bounds

    result = try_val(x)
    if result:
        best = (x, result)

    if result:
        # Success: double until fail or hit ceiling
        while calls < max_calls and x < hi:
            x = min(x * 2, hi)
            result = try_val(x)
            if result:
                best = (x, result)
            else:
                hi, lo = x - 1, best[0] + 1
                break
        else:
            return best
    else:
        # Fail: halve until success or hit floor
        hi = x - 1
        while calls < max_calls and x > lo:
            x = max(x // 2, lo)
            result = try_val(x)
            if result:
                best = (x, result)
                lo = x + 1
                break
        else:
            return (None, None)

    # Bisect remaining range
    while calls < max_calls and lo <= hi:
        x = (lo + hi) // 2
        result = try_val(x)
        if result:
            best = (x, result)
            lo = x + 1
        else:
            hi = x - 1

    return best or (None, None)


def _estimate_gif_size(width: int, height: int, num_frames: int, dithered: bool = True) -> int:
    """
    Estimate GIF file size in bytes given dimensions and frame count.

    Dithered GIFs (FFmpeg) have pseudo-random patterns that compress poorly,
    often 2-3 bytes per pixel per frame. Non-dithered GIFs (PIL) have solid
    color regions that compress well, typically ~1 byte per pixel per frame.
    """
    bytes_per_pixel_per_frame = 2.0 if dithered else 1.0
    return int(width * height * num_frames * bytes_per_pixel_per_frame)


def _estimate_initial_dpi(
    video_info: dict, target_bytes: int, fps: int, dithered: bool = True, base_pptx_bytes: int = 0
) -> int:
    """
    Estimate initial DPI for bisection based on target file size.

    DPI = PPI (pixels per inch of display size). Calculates what DPI would produce
    GIFs that sum to approximately target_bytes. Returns a conservative (lower)
    estimate to avoid slow first iterations.

    Args:
        video_info: Dict of video name -> info dict with visible_size, fps, num_frames.
        target_bytes: Target total file size in bytes.
        fps: Target frame rate.
        dithered: Whether GIFs will be dithered (affects size estimate).
        base_pptx_bytes: Size of PPTX without videos/GIFs (measured, not estimated).
    """
    # Calculate total "pixel-frames" at DPI=1 (i.e., 1 pixel per inch)
    total_pixel_frames_per_dpi_squared = 0

    for info in video_info.values():
        visible = info.get('visible_size')
        if not visible:
            continue

        vis_w_inches, vis_h_inches = visible
        src_fps = info['fps']
        num_frames = info['num_frames']

        # Effective frames at target fps
        if fps >= src_fps:
            eff_frames = num_frames
        else:
            eff_frames = int(num_frames * fps / src_fps)

        # At DPI=d, dimensions are (vis_w_inches * d) x (vis_h_inches * d)
        # So pixel count scales with d^2
        total_pixel_frames_per_dpi_squared += vis_w_inches * vis_h_inches * eff_frames

    if total_pixel_frames_per_dpi_squared == 0:
        return 100  # fallback

    # GIF size ≈ width * height * frames * bytes_per_pixel
    # Dithered ~2 bytes/pixel, non-dithered ~1 byte/pixel
    bytes_per_pixel = 2.0 if dithered else 1.0
    available_bytes = max(target_bytes - base_pptx_bytes, 1_000_000)
    dpi_squared = available_bytes / (total_pixel_frames_per_dpi_squared * bytes_per_pixel)
    dpi = int(dpi_squared ** 0.5)

    # Be conservative - halve estimate to avoid slow first iteration
    # (Higher DPI = larger GIFs = longer processing time)
    dpi = dpi // 2

    # Clamp to reasonable range
    return max(10, min(300, dpi))


def _get_video_info(work_dir: str, placements: dict) -> dict:
    """Get info for each video: path, dimensions, fps, and max visible size."""
    media_dir = rp.path_join(work_dir, 'ppt', 'media')
    result = {}

    for name, places in placements.items():
        path = rp.path_join(media_dir, name)
        if not rp.file_exists(path):
            continue

        visible_size = _max_visible_size(places)
        result[name] = {
            'path': path,
            'width': rp.get_video_file_width(path),
            'height': rp.get_video_file_height(path),
            'fps': rp.get_video_file_framerate(path),
            'num_frames': rp.get_video_file_num_frames(path),
            'visible_size': visible_size,
        }

    return result


def _max_visible_size(places: list) -> tuple[float, float] | None:
    """Get max visible size (inches) across all placements. None if all offscreen."""
    max_w, max_h = 0, 0
    for p in places:
        if p.visibility == 'offscreen':
            continue
        # Clip to slide bounds
        vis_w = min(p.slide_width, p.x + p.width) - max(0, p.x)
        vis_h = min(p.slide_height, p.y + p.height) - max(0, p.y)
        max_w, max_h = max(max_w, vis_w), max(max_h, vis_h)
    return (max_w, max_h) if max_w or max_h else None


def _convert_video_to_gif(
    video_path: str,
    media_dir: str,
    thumb_name: str,
    visible_inches: tuple[float, float],
    dpi: int,
    target_fps: int,
    info: dict,
    use_ffmpeg: bool = True,
) -> str:
    """
    Convert a video to GIF at specified DPI and FPS. Returns new filename.

    DPI = PPI (pixels per inch of display size).
    """
    gif_name = rp.with_file_extension(thumb_name, 'gif', replace=True)
    gif_path = rp.path_join(media_dir, gif_name)

    # Calculate target dimensions (don't upscale)
    target_w = min(int(visible_inches[0] * dpi), info['width'])
    target_h = min(int(visible_inches[1] * dpi), info['height'])
    target_w, target_h = max(16, target_w), max(16, target_h)

    # Calculate frame indices and output fps to preserve video duration
    # Duration = num_frames / src_fps must equal len(output_frames) / out_fps
    src_fps, num_frames = info['fps'], info['num_frames']
    original_duration = num_frames / src_fps

    if target_fps >= src_fps:
        indices = None  # Use all frames
        out_fps = int(round(src_fps))
    else:
        # Sample frames at target_fps rate
        step = src_fps / target_fps
        indices = [int(i * step) for i in range(int(num_frames / step)) if int(i * step) < num_frames]
        # Set output fps to preserve original duration (must be int for ffmpeg)
        out_fps = max(1, int(round(len(indices) / original_duration)))

    # Load and resize
    video = rp.load_video_via_decord(video_path, indices=indices)
    video = rp.resize_video_to_fit(video, height=target_h, width=target_w, allow_growth=False)

    # Save as GIF
    if use_ffmpeg:
        temp_mp4 = rp.temporary_file_path('.mp4')
        rp.save_video_mp4(video, temp_mp4, framerate=out_fps, show_progress=False)
        rp.convert_to_gif_via_ffmpeg(temp_mp4, gif_path, framerate=out_fps, show_progress=False)
        rp.delete_file(temp_mp4)
    else:
        rp.save_video_gif_via_pil(video, gif_path, framerate=out_fps)

    return gif_name


def _apply_pptx_transformations(work_dir: str, replacements: dict, offscreen: list, thumb_map: dict):
    """Apply all XML transformations to convert videos to images."""
    slides_dir = rp.path_join(work_dir, 'ppt', 'slides')
    media_dir = rp.path_join(work_dir, 'ppt', 'media')
    rels_dir = rp.path_join(slides_dir, '_rels')

    # Update references in slide XMLs and rels
    xml_files = rp.glob(rp.path_join(slides_dir, '*.xml')) + rp.glob(rp.path_join(rels_dir, '*.rels'))
    for xml_file in xml_files:
        content = rp.text_file_to_string(xml_file)
        for old, new in replacements.items():
            content = content.replace(old, new)
        rp.string_to_text_file(xml_file, content)

    # Remove offscreen videos
    for name in offscreen:
        rp.delete_file(rp.path_join(media_dir, name), strict=False)
        if name in thumb_map:
            rp.delete_file(rp.path_join(media_dir, thumb_map[name]), strict=False)

    # Strip video elements from XML
    for slide_xml in rp.glob(rp.path_join(slides_dir, 'slide*.xml')):
        content = rp.text_file_to_string(slide_xml)
        content = re.sub(r'<a:hlinkClick[^>]*action="ppaction://media"[^>]*/>', '', content)
        content = re.sub(r'<a:videoFile[^>]*/>', '', content)
        content = re.sub(r'<p:extLst>\s*<p:ext[^>]*>\s*<p14:media[^>]*/>\s*</p:ext>\s*</p:extLst>', '', content)
        content = re.sub(r'<p:timing>.*?</p:timing>', '', content, flags=re.DOTALL)
        rp.string_to_text_file(slide_xml, content)

    for rels_file in rp.glob(rp.path_join(rels_dir, '*.rels')):
        content = rp.text_file_to_string(rels_file)
        content = re.sub(r'<Relationship[^>]*Type="[^"]*video"[^>]*/>', '', content)
        content = re.sub(r'<Relationship[^>]*Type="[^"]*relationships/media"[^>]*/>', '', content)
        rp.string_to_text_file(rels_file, content)

    # Remove video files
    rp.delete_files(*rp.get_all_video_files(media_dir), strict=False)

    # Update content types
    ct_file = rp.path_join(work_dir, '[Content_Types].xml')
    content = rp.text_file_to_string(ct_file)
    content = re.sub(r'<Default Extension="(mp4|mov|avi|wmv|m4v|webm)"[^>]*/>', '', content)
    if 'Extension="gif"' not in content:
        content = content.replace('</Types>', '<Default Extension="gif" ContentType="image/gif"/></Types>')
    rp.string_to_text_file(ct_file, content)


def _create_pptx(work_dir: str, output_path: str):
    """Create PPTX ZIP from directory."""
    rp.delete_file(output_path, strict=False)
    zip_path = rp.make_zip_file_from_folder(work_dir)
    rp.move_file(zip_path, output_path)


# --- CLI ---

HELP = """Convert PowerPoint videos to GIFs with target file size.

Usage:
    python convert_pptx_videos_to_gifs.py <input_pptx> [output_pptx] [options]

Arguments:
    input_pptx      Path to input PowerPoint file (required)
    output_pptx     Output path (optional, default: <input>_gifs_<size>.pptx)

Options:
    --part_size     Target file size per part (default: 100MB)
    --num_parts     Split output into N parts (default: 1)
    --fps           Max GIF frames per second (default: 10)
    --dpi_iters     Binary search iterations to match part_size (default: 5)
    --dither        Enable GIF dithering (default: True)
    --no_dither     Disable dithering (smaller files, may have color banding)
    --slides        Slide range to process (default: all)
    --upload        Upload to Google Slides after conversion (default: False)

Examples:
    python convert_pptx_videos_to_gifs.py input.pptx
    python convert_pptx_videos_to_gifs.py input.pptx output.pptx
    python convert_pptx_videos_to_gifs.py input.pptx --part_size 50MB
    python convert_pptx_videos_to_gifs.py input.pptx --part_size 50MB --num_parts 3
    python convert_pptx_videos_to_gifs.py input.pptx --num_parts 3 --upload
    python convert_pptx_videos_to_gifs.py input.pptx --fps 5
    python convert_pptx_videos_to_gifs.py input.pptx --fps 10000              # keep original fps
    python convert_pptx_videos_to_gifs.py input.pptx --dpi_iters 10
    python convert_pptx_videos_to_gifs.py input.pptx --no_dither
    python convert_pptx_videos_to_gifs.py input.pptx --slides 1-10
    python convert_pptx_videos_to_gifs.py input.pptx --slides 1,3,5,10-15
    python convert_pptx_videos_to_gifs.py input.pptx --part_size 50MB --fps 8 --num_parts 5 --upload"""


if __name__ == '__main__':
    import sys

    args = sys.argv[1:]

    if not args or args[0] in ('-h', '--help', 'help'):
        print(HELP)
        sys.exit(0)

    # Parse arguments
    kwargs = {
        'input_pptx': None,
        'output_pptx': None,
        'target_size': '100MB',
        'fps': 10,
        'dpi_iters': 5,
        'dither': True,
        'slides': None,
        'num_parts': 1,
        'upload': False,
    }

    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith('--'):
            key = arg[2:]
            if key == 'upload':
                kwargs['upload'] = True
            elif key == 'no_dither':
                kwargs['dither'] = False
            elif key == 'dither':
                kwargs['dither'] = True
            elif key in ('-h', 'help'):
                print(HELP)
                sys.exit(0)
            elif i + 1 < len(args):
                val = args[i + 1]
                if key == 'part_size':
                    key = 'target_size'  # alias
                if key in ('fps', 'dpi_iters', 'num_parts'):
                    kwargs[key] = int(val)
                else:
                    kwargs[key] = val
                i += 1
        elif kwargs['input_pptx'] is None:
            kwargs['input_pptx'] = arg
        else:
            kwargs['output_pptx'] = arg
        i += 1

    if kwargs['input_pptx'] is None:
        print("Error: input_pptx is required\n")
        print(HELP)
        sys.exit(1)

    convert_pptx_videos_to_gifs(**kwargs)
