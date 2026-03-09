"""CLI entry point for rp.libs.powerpoint.

Usage:
    python -m rp.libs.powerpoint convert input.pptx
    python -m rp.libs.powerpoint convert input.pptx --num_parts 3 --upload
    python -m rp.libs.powerpoint upload folder_with_pptx/
"""

import rp

rp.pip_import('fire')
import fire

from .convert_pptx_videos_to_gifs import convert_pptx_videos_to_gifs
from .google_slides_upload import upload_and_merge_pptx, _upload_cli
from .convert_tmux import convert_tmux
from .media_to_slides import cli as media_to_slides_cli


def main():
    fire.Fire({
        'convert': convert_pptx_videos_to_gifs,
        'convert_tmux': convert_tmux,
        'upload': _upload_cli,
        'media_to_slides': media_to_slides_cli,
    })


if __name__ == '__main__':
    main()
