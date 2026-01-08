"""
Tmux-based parallel PowerPoint converter.

Spawns multiple tmux panes to convert different slide ranges in parallel,
then merges the uploaded presentations.

Usage:
    python -m rp.libs.powerpoint convert-tmux input.pptx --num-parts 3
"""

import os
import sys
import json
import time
import tempfile
import shlex

import rp


def get_slide_partitions(input_pptx: str, num_parts: int) -> list[tuple[int, int]]:
    """
    Analyze the PPTX and return slide ranges for each part.
    Returns list of (start, end) tuples (1-indexed, inclusive).

    For now, just splits evenly by slide count. Could be enhanced
    to weight by video content later.
    """
    from .convert_pptx_videos_to_gifs import _count_slides

    with tempfile.TemporaryDirectory() as tmpdir:
        # Extract pptx
        work_dir = os.path.join(tmpdir, 'work')
        rp.extract_zip_file(input_pptx, work_dir)

        total_slides = _count_slides(work_dir)

        if total_slides == 0:
            raise ValueError("No slides found in presentation")

        # Split evenly
        partitions = []
        per_part = max(1, total_slides // num_parts)
        for i in range(num_parts):
            start = i * per_part + 1
            if i == num_parts - 1:
                end = total_slides
            else:
                end = (i + 1) * per_part
            if start <= total_slides:
                partitions.append((start, end))

        return partitions


def run_worker(
    input_pptx: str,
    output_pptx: str,
    slide_range: str,
    part_num: int,
    signal_dir: str,
    target_size: str = '100MB',
    fps: int = 10,
    dpi_iters: int = 5,
    dither: bool = True,
):
    """
    Worker process: converts a slide range and uploads, then signals completion.
    This runs in a tmux pane.
    """
    import rp
    from .convert_pptx_videos_to_gifs import convert_pptx_videos_to_gifs, _filter_pptx_to_slides, _delete_unused_media
    from . import google_slides_upload as gsu

    signal_file = os.path.join(signal_dir, f'part_{part_num}.json')

    try:
        rp.fansi_print(f"Part {part_num}: Converting slides {slide_range}", 'cyan', 'bold')

        # Parse slide range (e.g., "1-5" -> start=1, end=5)
        start, end = map(int, slide_range.split('-'))

        # Convert - returns input_pptx if no videos to convert
        result_path = convert_pptx_videos_to_gifs(
            input_pptx=input_pptx,
            output_pptx=output_pptx,
            target_size=target_size,
            fps=fps,
            dpi_iters=dpi_iters,
            dither=dither,
            slides=slide_range,
            num_parts=1,  # Single output per worker
            upload=False,  # We'll upload separately
        )

        # convert_pptx_videos_to_gifs with slides param only processes videos on those slides
        # but keeps all slides in output. We need to filter to just our slide range.
        if os.path.exists(output_pptx):
            rp.fansi_print(f"Part {part_num}: Filtering to slides {start}-{end}...", 'cyan')
            with tempfile.TemporaryDirectory() as tmpdir:
                work_dir = os.path.join(tmpdir, 'work')
                rp.extract_zip_file(output_pptx, work_dir)
                _filter_pptx_to_slides(work_dir, start, end)
                _delete_unused_media(work_dir)
                # Recreate output with filtered slides
                rp.make_zip_file_from_folder(work_dir, output_pptx)
        else:
            # No videos converted, extract just the slide range from input
            rp.fansi_print(f"Part {part_num}: No videos in range, extracting slides...", 'yellow')
            with tempfile.TemporaryDirectory() as tmpdir:
                work_dir = os.path.join(tmpdir, 'work')
                rp.extract_zip_file(input_pptx, work_dir)
                _filter_pptx_to_slides(work_dir, start, end)
                _delete_unused_media(work_dir)
                # Create output pptx
                os.makedirs(os.path.dirname(output_pptx), exist_ok=True)
                rp.make_zip_file_from_folder(work_dir, output_pptx)
            rp.fansi_print(f"Part {part_num}: Created {output_pptx}", 'cyan')

        rp.fansi_print(f"Part {part_num}: Uploading...", 'cyan', 'bold')

        # Upload
        creds = gsu.get_credentials()
        from googleapiclient.discovery import build
        drive_service = build('drive', 'v3', credentials=creds)

        result = gsu.upload_pptx_as_slides(drive_service, output_pptx, None, None)

        rp.fansi_print(f"Part {part_num}: Done! {result['url']}", 'green', 'bold')

        # Signal completion
        with open(signal_file, 'w') as f:
            json.dump({'status': 'success', 'result': result}, f)

    except Exception as e:
        rp.fansi_print(f"Part {part_num}: ERROR: {e}", 'red', 'bold')
        with open(signal_file, 'w') as f:
            json.dump({'status': 'error', 'error': str(e)}, f)
        raise


def run_orchestrator(
    input_pptx: str,
    num_parts: int,
    signal_dir: str,
    folder_name: str,
    merged_name: str,
):
    """
    Orchestrator process: waits for all workers, then merges.
    """
    import rp
    from . import google_slides_upload as gsu

    rp.fansi_print("Orchestrator: Waiting for all parts to complete...", 'cyan', 'bold')

    # Wait for all signal files
    results = []
    while len(results) < num_parts:
        for i in range(1, num_parts + 1):
            signal_file = os.path.join(signal_dir, f'part_{i}.json')
            if os.path.exists(signal_file) and i not in [r.get('part') for r in results]:
                with open(signal_file) as f:
                    data = json.load(f)
                data['part'] = i
                results.append(data)
                if data['status'] == 'success':
                    rp.fansi_print(f"Orchestrator: Part {i} completed", 'green')
                else:
                    rp.fansi_print(f"Orchestrator: Part {i} FAILED: {data.get('error')}", 'red')
        time.sleep(1)

    # Check for errors
    errors = [r for r in results if r['status'] == 'error']
    if errors:
        rp.fansi_print(f"Orchestrator: {len(errors)} part(s) failed!", 'red', 'bold')
        return

    # Sort by part number and get presentation IDs
    results.sort(key=lambda r: r['part'])
    presentation_ids = [r['result']['id'] for r in results]

    rp.fansi_print(f"\nOrchestrator: Merging {len(presentation_ids)} presentations...", 'cyan', 'bold')

    # Get credentials and merge
    creds = gsu.get_credentials()
    from googleapiclient.discovery import build
    drive_service = build('drive', 'v3', credentials=creds)

    # Create folder
    folder_id = gsu.create_folder(drive_service, folder_name)
    folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
    rp.fansi_print(f"  Folder: {folder_url}", 'white')

    # Move parts to folder
    for r in results:
        drive_service.files().update(
            fileId=r['result']['id'],
            addParents=folder_id,
            fields='id'
        ).execute()

    # Merge
    merged = gsu.merge_presentations_via_webapp(presentation_ids, merged_name)

    # Move merged to folder
    drive_service.files().update(
        fileId=merged['presentationId'],
        addParents=folder_id,
        fields='id'
    ).execute()

    # Set permissions
    public_url = gsu.make_public(drive_service, merged['presentationId'])
    merged_url = f"https://docs.google.com/presentation/d/{merged['presentationId']}/edit"

    rp.fansi_print("\n" + "="*60, 'green')
    rp.fansi_print("SUCCESS!", 'green', 'bold')
    rp.fansi_print(f"  Folder: {folder_url}", 'green')
    rp.fansi_print(f"  Total slides: {merged['slideCount']}", 'green')
    if public_url:
        rp.fansi_print(f"  Shareable link: {public_url}", 'green', 'bold')
    else:
        rp.fansi_print(f"  Edit link: {merged_url}", 'green')


def convert_tmux(
    input_pptx: str,
    num_parts: int = 3,
    target_size: str = '100MB',
    fps: int = 10,
    dpi_iters: int = 5,
    dither: bool = True,
    output_folder: str = None,
):
    """
    Main entry point: sets up tmux session with parallel workers.
    """
    if not rp.running_in_tmux():
        rp.fansi_print("This command must be run inside tmux!", 'red', 'bold')
        rp.fansi_print("Start tmux first, then run this command.", 'yellow')
        return

    input_pptx = os.path.abspath(input_pptx)
    base_name = rp.get_file_name(input_pptx, include_file_extension=False)

    if output_folder is None:
        output_folder = f"{base_name}_gifs_{target_size}"
    output_folder = os.path.abspath(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    # Create signal directory
    signal_dir = tempfile.mkdtemp(prefix='ppt_convert_')

    # Get slide partitions
    rp.fansi_print(f"Analyzing {input_pptx}...", 'cyan')
    partitions = get_slide_partitions(input_pptx, num_parts)

    # Actual number of parts may be less than requested
    actual_parts = len(partitions)
    if actual_parts < num_parts:
        rp.fansi_print(f"Note: Only {actual_parts} parts possible (fewer slides than requested)", 'yellow')

    rp.fansi_print(f"Partition plan ({actual_parts} parts):", 'cyan')
    for i, (start, end) in enumerate(partitions, 1):
        rp.fansi_print(f"  Part {i}: slides {start}-{end}", 'white')

    # Build commands for each worker pane
    python = sys.executable
    worker_cmds = []
    for i, (start, end) in enumerate(partitions, 1):
        output_pptx = os.path.join(output_folder, f"{base_name}_part{i}.pptx")
        slide_range = f"{start}-{end}"

        cmd = (
            f"{shlex.quote(python)} -c \""
            f"import sys; sys.path.insert(0, '/opt/homebrew/lib/python3.10/site-packages'); "
            f"from rp.libs.powerpoint.convert_tmux import run_worker; "
            f"run_worker("
            f"{repr(input_pptx)}, "
            f"{repr(output_pptx)}, "
            f"{repr(slide_range)}, "
            f"{i}, "
            f"{repr(signal_dir)}, "
            f"{repr(target_size)}, "
            f"{fps}, "
            f"{dpi_iters}, "
            f"{dither}"
            f")\""
        )
        worker_cmds.append(cmd)

    # Build orchestrator command
    orchestrator_cmd = (
        f"{shlex.quote(python)} -c \""
        f"import sys; sys.path.insert(0, '/opt/homebrew/lib/python3.10/site-packages'); "
        f"from rp.libs.powerpoint.convert_tmux import run_orchestrator; "
        f"run_orchestrator("
        f"{repr(input_pptx)}, "
        f"{actual_parts}, "
        f"{repr(signal_dir)}, "
        f"{repr(output_folder)}, "
        f"{repr(base_name)}"
        f")\""
    )

    # Create tmux session with workers in one window, orchestrator in another
    session_name = rp.tmux_get_unique_session_name(f"ppt_{os.getpid()}")

    # Window 1: All workers as panes
    # Window 2: Orchestrator
    windows = {
        "workers": worker_cmds,  # Multiple panes
        "orchestrator": orchestrator_cmd,  # Single pane
    }

    yaml = rp.tmuxp_create_session_yaml(windows, session_name=session_name)
    rp.fansi_print(f"\nLaunching tmux session in background: {session_name}", 'green', 'bold')
    rp.tmuxp_launch_session_from_yaml(yaml, attach=False)

    rp.fansi_print(f"\nTo view progress:", 'cyan')
    rp.fansi_print(f"  tmux switch-client -t {session_name}", 'white')
    rp.fansi_print(f"Or attach from another terminal:", 'cyan')
    rp.fansi_print(f"  tmux attach -t {session_name}", 'white')


HELP = """Parallel PowerPoint converter using tmux.

Usage:
    rp run ppt convert-tmux <input_pptx> [options]

Spawns multiple tmux panes to convert slide ranges in parallel,
uploads each part, then merges them into one presentation.

Options:
    --num-parts     Number of parallel workers (default: 3)
    --part-size     Target file size per part (default: 100MB)
    --fps           Max GIF frames per second (default: 10)
    --dpi-iters     Binary search iterations for size (default: 5)
    --dither        Enable dithering (default: True)
    --no-dither     Disable dithering
    --output        Output folder name

Examples:
    rp run ppt convert-tmux presentation.pptx
    rp run ppt convert-tmux presentation.pptx --num-parts 5
    rp run ppt convert-tmux presentation.pptx --part-size 50MB --fps 8
"""


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]

    if not args or args[0] in ('-h', '--help'):
        print(HELP)
        sys.exit(0)

    # Simple arg parsing
    input_pptx = args[0]
    kwargs = {
        'num_parts': 3,
        'target_size': '100MB',
        'fps': 10,
        'dpi_iters': 5,
        'dither': True,
        'output_folder': None,
    }

    i = 1
    while i < len(args):
        arg = args[i]
        if arg == '--num-parts' and i + 1 < len(args):
            kwargs['num_parts'] = int(args[i + 1])
            i += 1
        elif arg == '--part-size' and i + 1 < len(args):
            kwargs['target_size'] = args[i + 1]
            i += 1
        elif arg == '--fps' and i + 1 < len(args):
            kwargs['fps'] = int(args[i + 1])
            i += 1
        elif arg == '--dpi-iters' and i + 1 < len(args):
            kwargs['dpi_iters'] = int(args[i + 1])
            i += 1
        elif arg == '--dither':
            kwargs['dither'] = True
        elif arg == '--no-dither':
            kwargs['dither'] = False
        elif arg == '--output' and i + 1 < len(args):
            kwargs['output_folder'] = args[i + 1]
            i += 1
        i += 1

    convert_tmux(input_pptx, **kwargs)
