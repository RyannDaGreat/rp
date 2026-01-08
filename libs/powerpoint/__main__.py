"""CLI entry point for rp.libs.powerpoint.

Usage:
    python -m rp.libs.powerpoint convert input.pptx
    python -m rp.libs.powerpoint convert input.pptx --num-parts 3 --upload
    python -m rp.libs.powerpoint upload folder_with_pptx/
"""

import sys
import rp

from .convert_pptx_videos_to_gifs import convert_pptx_videos_to_gifs
from .google_slides_upload import upload_and_merge_pptx
from .convert_tmux import convert_tmux
from .media_to_slides import cli as media_to_slides_cli


def print_main_help():
    print("""PowerPoint tools for video-to-GIF conversion and Google Slides upload.

Commands:
    convert          Convert PowerPoint videos to GIFs
    convert_tmux     Parallel convert using tmux (faster for multi-part)
    upload           Upload PPTX files to Google Slides and merge
    media_to_slides  Upload media (videos/images) to Google Slides

Examples:
    rp run ppt convert input.pptx
    rp run ppt convert input.pptx --part-size 50MB
    rp run ppt convert input.pptx --num-parts 3 --upload
    rp run ppt convert_tmux input.pptx --num-parts 3
    rp run ppt upload output_folder/
    rp run ppt upload part1.pptx part2.pptx part3.pptx
    rp run ppt media_to_slides video.mp4 image.png
    rp run ppt media_to_slides folder/ --captions --title "My Gallery"

Run 'rp run ppt <command>' for command-specific help.""")


from .convert_pptx_videos_to_gifs import HELP as CONVERT_HELP
from .google_slides_upload import HELP as UPLOAD_HELP
from .convert_tmux import HELP as CONVERT_TMUX_HELP


def cmd_convert(
    input_pptx: str = None,
    output_pptx: str = None,
    target_size: str = '100MB',
    fps: int = 10,
    dpi_iters: int = 5,
    dither: bool = True,
    slides: str = None,
    num_parts: int = 1,
    upload: bool = False,
):
    if input_pptx is None:
        print(CONVERT_HELP)
        return
    return convert_pptx_videos_to_gifs(
        input_pptx, output_pptx, target_size, fps, dpi_iters,
        dither, slides, num_parts, upload
    )


def cmd_upload(*paths, folder_name: str = None, merged_name: str = None):
    if not paths:
        print(UPLOAD_HELP)
        return
    if len(paths) == 1 and rp.folder_exists(paths[0]):
        pptx_paths = sorted(rp.glob(rp.path_join(paths[0], '*.pptx')))
        if not pptx_paths:
            print(f"Error: No .pptx files found in {paths[0]}")
            return
    else:
        pptx_paths = list(paths)
    return upload_and_merge_pptx(pptx_paths, folder_name, merged_name)


def main():
    args = sys.argv[1:]

    if not args or args[0] in ('-h', '--help', 'help'):
        print_main_help()
        return

    cmd = args[0]
    rest = args[1:]

    if cmd == 'convert':
        if not rest or rest[0] in ('-h', '--help'):
            print(CONVERT_HELP)
            return
        # Parse args manually for convert
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
        while i < len(rest):
            arg = rest[i]
            if arg.startswith('--'):
                key = arg[2:].replace('-', '_')
                if key == 'upload':
                    kwargs['upload'] = True
                elif key == 'no_dither':
                    kwargs['dither'] = False
                elif key == 'dither':
                    kwargs['dither'] = True
                elif i + 1 < len(rest):
                    val = rest[i + 1]
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
        cmd_convert(**kwargs)

    elif cmd == 'convert_tmux':
        if not rest or rest[0] in ('-h', '--help'):
            print(CONVERT_TMUX_HELP)
            return
        # Parse args for convert-tmux
        kwargs = {
            'num_parts': 3,
            'target_size': '100MB',
            'fps': 10,
            'dpi_iters': 5,
            'dither': True,
            'output_folder': None,
        }
        input_pptx = None
        i = 0
        while i < len(rest):
            arg = rest[i]
            if arg.startswith('--'):
                key = arg[2:].replace('-', '_')
                if key == 'no_dither':
                    kwargs['dither'] = False
                elif key == 'dither':
                    kwargs['dither'] = True
                elif i + 1 < len(rest):
                    val = rest[i + 1]
                    if key == 'part_size':
                        key = 'target_size'
                    if key in ('fps', 'dpi_iters', 'num_parts'):
                        kwargs[key] = int(val)
                    elif key == 'output':
                        kwargs['output_folder'] = val
                    else:
                        kwargs[key] = val
                    i += 1
            elif input_pptx is None:
                input_pptx = arg
            i += 1
        if input_pptx is None:
            print(CONVERT_TMUX_HELP)
            return
        convert_tmux(input_pptx, **kwargs)

    elif cmd == 'upload':
        if not rest or rest[0] in ('-h', '--help'):
            print(UPLOAD_HELP)
            return
        # Parse args for upload
        paths = []
        folder_name = None
        merged_name = None
        i = 0
        while i < len(rest):
            arg = rest[i]
            if arg == '--folder-name' and i + 1 < len(rest):
                folder_name = rest[i + 1]
                i += 1
            elif arg == '--merged-name' and i + 1 < len(rest):
                merged_name = rest[i + 1]
                i += 1
            elif not arg.startswith('--'):
                paths.append(arg)
            i += 1
        cmd_upload(*paths, folder_name=folder_name, merged_name=merged_name)

    elif cmd == 'media_to_slides':
        # Use fire - it handles all the arg parsing
        rp.pip_import('fire')
        import fire
        sys.argv = ['media_to_slides'] + rest
        fire.Fire(media_to_slides_cli)

    else:
        print(f"Unknown command: {cmd}")
        print()
        print_main_help()


if __name__ == '__main__':
    main()
