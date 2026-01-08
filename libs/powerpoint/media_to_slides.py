"""
Upload media files (videos/images) to Google Drive and create a Google Slides presentation.

Usage:
    rp run ppt media_to_slides video1.mp4 video2.mp4 image.png
    rp run ppt media_to_slides folder_with_media/
    rp run ppt media_to_slides *.mp4 *.png --name "My Presentation"
"""

import os
import time
import tempfile

import rp

rp.pip_import("google.auth")
rp.pip_import("google_auth_oauthlib")
rp.pip_import("googleapiclient")
rp.pip_import("tqdm")

from tqdm import tqdm

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Reuse credentials from google_slides_upload
try:
    from .google_slides_upload import (
        SCOPES,
        CLIENT_JSON_FILE,
        TOKEN_PATH,
        get_credentials,
        create_folder,
        make_public,
        get_rp_slides_folder,
    )
except ImportError:
    from google_slides_upload import (
        SCOPES,
        CLIENT_JSON_FILE,
        TOKEN_PATH,
        get_credentials,
        create_folder,
        make_public,
        get_rp_slides_folder,
    )


def compress_video(input_path: str, output_path: str, crf: int = 28) -> str:
    """
    Compress a video using ffmpeg with H.264 codec.

    Args:
        input_path: Path to input video
        output_path: Path to output compressed video
        crf: Constant Rate Factor (18-28 typical, higher = smaller file)

    Returns:
        Path to compressed video
    """
    import subprocess

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-c:v",
        "libx264",
        "-crf",
        str(crf),
        "-preset",
        "fast",
        "-c:a",
        "aac",
        "-b:a",
        "64k",
        "-movflags",
        "+faststart",
        output_path,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


# Google Slides dimensions (16:9 widescreen) in points
SLIDE_WIDTH_PT, SLIDE_HEIGHT_PT = 720, 405
MEDIA_ASPECT = 16 / 9
TITLE_PADDING, LABEL_PADDING = 16, 8

# Default styling
DEFAULT_FONT = "Lexend"
DEFAULT_TITLE_SIZE, DEFAULT_LABEL_SIZE = 24, 12

# URL templates
DRIVE_FILE_URL = "https://drive.google.com/uc?id={}"
SLIDES_URL = "https://docs.google.com/presentation/d/{}/edit"
FOLDER_URL = "https://drive.google.com/drive/folders/{}"

# Media types
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
MIME_TYPES = {
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".avi": "video/x-msvideo",
    ".mkv": "video/x-matroska",
    ".webm": "video/webm",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
    ".webp": "image/webp",
}


def _get_ext(path: str) -> str:
    """Get file extension with leading dot, lowercase."""
    return "." + rp.get_file_extension(path).lower()


def is_image(path: str) -> bool:
    return _get_ext(path) in IMAGE_EXTENSIONS


def is_video(path: str) -> bool:
    return _get_ext(path) in VIDEO_EXTENSIONS


def is_media_path(x) -> bool:
    """Check if x looks like a media file path (by extension)."""
    if not isinstance(x, str):
        return False
    ext = _get_ext(x)
    return ext in IMAGE_EXTENSIONS or ext in VIDEO_EXTENSIONS


def _parse_labeled_dict(d: dict) -> tuple[list, list]:
    """Parse {label: path} dict. Returns (paths, labels) or raises if backwards."""
    labels = []
    paths = []
    for label, path in d.items():
        if is_media_path(path):
            labels.append(label)
            paths.append(path)
    if not paths and d:
        first_key = next(iter(d.keys()))
        if is_media_path(first_key):
            raise ValueError(
                f"Dict has paths as keys, but expected {{label: path}}. "
                f"Got {{{repr(first_key)}: ...}}. Flip your dict."
            )
    return paths, labels


def _parse_content(content, title=None) -> dict | None:
    """Parse content into a slide dict, or None if no valid paths."""
    if is_media_path(content):
        return {"paths": [content], "title": title, "labels": None}
    if isinstance(content, dict):
        paths, labels = _parse_labeled_dict(content)
        if paths:
            return {"paths": paths, "title": title, "labels": labels}
    elif rp.is_non_str_iterable(content):
        paths = [p for p in content if is_media_path(p)]
        if paths:
            return {"paths": paths, "title": title, "labels": None}
    return None


def normalize_slides_input(layout) -> list[dict]:
    """
    Normalize flexible input formats into list of slide dicts.

    Returns list of {'paths': [...], 'title': str or None, 'labels': [...] or None}

    Accepts:
        - List of paths: ['a.mp4', 'b.png'] -> one per slide, no titles
        - Nested lists: [['a.mp4', 'b.png'], 'c.mp4'] -> grid on first slide
        - Dict with slide titles: {'Slide 1': ['a.mp4'], 'Slide 2': 'b.png'}
        - Dict with nested labels: {'Slide 1': {'vid': 'a.mp4', 'img': 'b.png'}}
        - Single path: 'a.mp4'
    """
    if is_media_path(layout):
        return [{"paths": [layout], "title": None, "labels": None}]

    if isinstance(layout, dict):
        result = []
        for title, content in layout.items():
            slide = _parse_content(content, title)
            if slide:
                result.append(slide)
        return result

    result = []
    for item in layout:
        slide = _parse_content(item)
        if slide:
            result.append(slide)
    return result


def upload_media(
    service,
    file_path: str,
    folder_id: str = None,
    progress_callback=None,
) -> dict:
    """
    Upload a media file (video or image) to Google Drive.

    Returns dict with 'id', 'name', 'webViewLink', 'webContentLink', 'is_image'.
    """
    file_size = rp.get_file_size(file_path)
    file_name = rp.get_file_name(file_path)
    ext = _get_ext(file_path)
    mimetype = MIME_TYPES.get(ext, "application/octet-stream")

    metadata = {"name": file_name}
    if folder_id:
        metadata["parents"] = [folder_id]

    media = MediaFileUpload(
        file_path,
        mimetype=mimetype,
        chunksize=5 * 1024 * 1024,
        resumable=True,
    )

    request = service.files().create(
        body=metadata,
        media_body=media,
        fields="id,name,webViewLink,webContentLink",
    )

    response = None
    retries = 0
    max_retries = 5
    while response is None:
        try:
            status, response = request.next_chunk()
            if status and progress_callback:
                progress_callback(status.progress(), file_size)
            retries = 0
        except HttpError as e:
            if e.resp.status in [500, 502, 503, 504, 308]:
                retries += 1
                if retries > max_retries:
                    raise
                time.sleep(2**retries)
            else:
                raise

    return {
        "id": response.get("id"),
        "name": response.get("name"),
        "webViewLink": response.get("webViewLink"),
        "webContentLink": response.get("webContentLink"),
        "is_image": is_image(file_path),
    }


def make_file_public(service, file_id: str) -> str:
    """Make a file publicly viewable. Returns the direct link."""
    service.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"},
        fields="id",
    ).execute()
    return DRIVE_FILE_URL.format(file_id)


def _format_eta(done: int, total: int, elapsed: float) -> str:
    """Format ETA string based on progress and elapsed time."""
    if done <= 0 or elapsed <= 0:
        return ""
    rate = done / elapsed
    remaining = total - done
    eta_seconds = remaining / rate
    return f", ETA: {int(eta_seconds // 60)}m{int(eta_seconds % 60):02d}s"


def _format_progress(index: int, total: int, done: int, total_size: int, elapsed: float, use_bytes: bool = True) -> str:
    """Format overall progress string."""
    eta = _format_eta(done, total_size, elapsed)
    if use_bytes:
        done_str = rp.human_readable_file_size(done)
        total_str = rp.human_readable_file_size(total_size)
        return f"[{index}/{total}] {done_str} / {total_str}{eta}"
    return f"[{index}/{total}]{eta}"


def upload_media_sequential(
    service,
    file_paths: list[str],
    folder_id: str = None,
) -> list[dict]:
    """Upload multiple media files sequentially with progress bars."""
    results = []
    total_bytes = sum(rp.get_file_size(fp) for fp in file_paths)
    uploaded_bytes = 0
    start_time = time.time()

    for i, fp in enumerate(file_paths):
        size = rp.get_file_size(fp)
        elapsed = time.time() - start_time
        progress_str = _format_progress(i + 1, len(file_paths), uploaded_bytes, total_bytes, elapsed)
        rp.fansi_print(f"  {progress_str}", "cyan")

        pbar = tqdm(
            total=size,
            desc=rp.get_file_name(fp),
            unit="B",
            unit_scale=True,
            leave=False,
        )
        last_progress = [0]

        def progress_cb(progress, total):
            current = int(progress * total)
            pbar.update(current - last_progress[0])
            last_progress[0] = current

        result = upload_media(service, fp, folder_id, progress_cb)
        pbar.update(size - last_progress[0])  # Ensure 100%
        pbar.close()
        uploaded_bytes += size
        rp.fansi_print(f"  Uploaded: {result['webViewLink']}", "green")
        results.append(result)

    return results


# --- Slides API helpers ---


def _pt(val: float) -> dict:
    """Create a magnitude/unit dict in points."""
    return {"magnitude": val, "unit": "PT"}


def _size(w: float, h: float) -> dict:
    """Create size dict for Slides API."""
    return {"width": _pt(w), "height": _pt(h)}


def _transform(x: float, y: float) -> dict:
    """Create transform dict for Slides API (no scaling)."""
    return {
        "scaleX": 1,
        "scaleY": 1,
        "translateX": x,
        "translateY": y,
        "unit": "PT",
    }


def _element_props(
    page_id: str, x: float, y: float, w: float, h: float
) -> dict:
    """Create elementProperties dict for Slides API."""
    return {
        "pageObjectId": page_id,
        "size": _size(w, h),
        "transform": _transform(x, y),
    }


def _rgb(color: tuple) -> dict:
    """Create rgbColor dict from (r, g, b) float tuple."""
    return {"red": color[0], "green": color[1], "blue": color[2]}


def _fg_color(rgb: tuple) -> dict:
    """Create foregroundColor dict for text styling."""
    return {"opaqueColor": {"rgbColor": _rgb(rgb)}}


def _text_element_requests(
    obj_id: str,
    page_id: str,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str,
    font: str,
    size: int,
    color: tuple = None,
    bold: bool = False,
) -> list:
    """Create requests for a centered text box: createShape, insertText, updateTextStyle, updateParagraphStyle."""
    style = {"fontSize": _pt(size), "fontFamily": font}
    if bold:
        style["bold"] = True
    if color:
        style["foregroundColor"] = _fg_color(color)
    fields = (
        "fontSize,fontFamily"
        + (",bold" if bold else "")
        + (",foregroundColor" if color else "")
    )
    return [
        {
            "createShape": {
                "objectId": obj_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": _element_props(page_id, x, y, w, h),
            }
        },
        {"insertText": {"objectId": obj_id, "text": text}},
        {
            "updateTextStyle": {
                "objectId": obj_id,
                "style": style,
                "fields": fields,
            }
        },
        {
            "updateParagraphStyle": {
                "objectId": obj_id,
                "style": {"alignment": "CENTER"},
                "fields": "alignment",
            }
        },
    ]


def parse_color(color) -> tuple:
    """Parse color string to RGB float tuple (0-1 range) for Slides API."""
    if color is None:
        return None
    if isinstance(color, str):
        if color.startswith("#"):
            rgb = rp.hex_color_to_byte_color(color)
        else:
            rgb = rp.color_name_to_byte_color(color)
    else:
        rgb = color  # Assume already tuple
    # Convert byte (0-255) to float (0-1)
    return (rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)


def compute_grid_layout(
    n_items: int,
    slide_width: float,
    slide_height: float,
    label_height: float = 0,
    label_position: str = "top",
) -> list[dict]:
    """
    Compute positions for n items in a tight grid layout (no gaps).
    Labels are placed directly above or below media with no spacing.
    Returns list of {'x', 'y', 'width', 'height', 'label_y'}.
    """
    if n_items == 0:
        return []

    rows, cols = rp.get_best_tiling_dimensions(n_items, target_aspect_ratio=1)
    cell_w, cell_h = slide_width / cols, slide_height / rows
    avail_h = cell_h - label_height

    # Fit media with MEDIA_ASPECT ratio in available space
    if cell_w / avail_h > MEDIA_ASPECT:
        media_h, media_w = avail_h, avail_h * MEDIA_ASPECT
    else:
        media_w, media_h = cell_w, cell_w / MEDIA_ASPECT

    layouts = []
    for i in range(n_items):
        cell_x, cell_y = (i % cols) * cell_w, (i // cols) * cell_h
        x = cell_x + (cell_w - media_w) / 2
        if label_position == "top":
            # Label at top, media below it
            label_y, media_y = cell_y, cell_y + label_height
        else:
            # Media at top, label below it
            media_y, label_y = cell_y, cell_y + media_h
        layouts.append(
            {
                "x": x,
                "y": media_y,
                "width": media_w,
                "height": media_h,
                "label_x": cell_x,
                "label_y": label_y,
                "label_width": cell_w,
            }
        )
    return layouts


def create_slides_with_media_grid(
    slides_service,
    drive_service,
    slides_data: list[dict],
    presentation_name: str = "Media Presentation",
    label_position: str = "top",
    bg_color=None,
    font_color=None,
    font: str = DEFAULT_FONT,
    title_size: int = DEFAULT_TITLE_SIZE,
    label_size: int = DEFAULT_LABEL_SIZE,
) -> dict:
    """
    Create a Google Slides presentation with media in grids.

    Args:
        slides_data: List of {'media': [...], 'title': str|None, 'labels': [...]|None}
        label_position: 'top' or 'bottom' - where labels appear relative to media
        bg_color: Background color (name like 'black', hex like '#FFAABB', or RGB tuple)
        font_color: Text color (same format as bg_color)
        font: Font family name (default: 'Lexend')
        title_size: Title font size in pt (default: 24)
        label_size: Label font size in pt (default: 12)
    """
    bg_rgb = parse_color(bg_color)
    font_rgb = parse_color(font_color)
    presentation = (
        slides_service.presentations()
        .create(body={"title": presentation_name})
        .execute()
    )
    pres_id = presentation["presentationId"]
    default_slide_id = presentation["slides"][0]["objectId"]

    requests, autoplay_requests, media_counter = [], [], 0

    for slide_idx, slide in enumerate(slides_data):
        slide_id = f"slide_{slide_idx}"
        slide_media, title, labels = (
            slide["media"],
            slide.get("title"),
            slide.get("labels"),
        )

        requests.append(
            {
                "createSlide": {
                    "objectId": slide_id,
                    "insertionIndex": slide_idx,
                    "slideLayoutReference": {"predefinedLayout": "BLANK"},
                }
            }
        )

        if bg_rgb:
            requests.append(
                {
                    "updatePageProperties": {
                        "objectId": slide_id,
                        "pageProperties": {
                            "pageBackgroundFill": {
                                "solidFill": {
                                    "color": {"rgbColor": _rgb(bg_rgb)}
                                }
                            }
                        },
                        "fields": "pageBackgroundFill",
                    }
                }
            )

        title_h = (title_size + TITLE_PADDING) if title else 0
        grid_top, grid_h = title_h, SLIDE_HEIGHT_PT - title_h

        if title:
            requests.extend(
                _text_element_requests(
                    f"title_{slide_idx}",
                    slide_id,
                    0,
                    0,
                    SLIDE_WIDTH_PT,
                    title_h,
                    title,
                    font,
                    title_size,
                    font_rgb,
                    bold=True,
                )
            )

        label_h = (label_size + LABEL_PADDING) if labels else 0
        positions = compute_grid_layout(
            len(slide_media), SLIDE_WIDTH_PT, grid_h, label_h, label_position
        )

        for media_idx, media in enumerate(slide_media):
            obj_id, pos = f"media_{media_counter}", positions[media_idx]
            media_y = pos["y"] + grid_top
            elem_props = _element_props(
                slide_id, pos["x"], media_y, pos["width"], pos["height"]
            )

            if media.get("is_image"):
                requests.append(
                    {
                        "createImage": {
                            "objectId": obj_id,
                            "url": DRIVE_FILE_URL.format(media["id"]),
                            "elementProperties": elem_props,
                        }
                    }
                )
            else:
                requests.append(
                    {
                        "createVideo": {
                            "objectId": obj_id,
                            "source": "DRIVE",
                            "id": media["id"],
                            "elementProperties": elem_props,
                        }
                    }
                )
                autoplay_requests.append(
                    {
                        "updateVideoProperties": {
                            "objectId": obj_id,
                            "videoProperties": {"autoPlay": True},
                            "fields": "autoPlay",
                        }
                    }
                )

            if labels and media_idx < len(labels):
                requests.extend(
                    _text_element_requests(
                        f"label_{media_counter}",
                        slide_id,
                        pos["label_x"],
                        pos["label_y"] + grid_top,
                        pos["label_width"],
                        label_h,
                        labels[media_idx],
                        font,
                        label_size,
                        font_rgb,
                    )
                )

            media_counter += 1

    requests.append({"deleteObject": {"objectId": default_slide_id}})
    slides_service.presentations().batchUpdate(
        presentationId=pres_id, body={"requests": requests}
    ).execute()
    if autoplay_requests:
        slides_service.presentations().batchUpdate(
            presentationId=pres_id, body={"requests": autoplay_requests}
        ).execute()

    return {"id": pres_id, "url": SLIDES_URL.format(pres_id)}


def media_to_slides(
    layout,
    presentation_name: str = None,
    folder_name: str = None,
    label_position: str = "top",
    bg_color=None,
    font_color=None,
    font: str = DEFAULT_FONT,
    title_size: int = DEFAULT_TITLE_SIZE,
    label_size: int = DEFAULT_LABEL_SIZE,
) -> dict:
    """
    Upload media files (videos/images) and create a Google Slides presentation.

    Args:
        layout: Media to include. Accepts flexible formats:
            - str: Single file path ('a.mp4')
            - list[str]: One file per slide (['a.mp4', 'b.png'])
            - list[list[str]]: Grid layouts ([['a.mp4', 'b.png'], 'c.mp4'])
            - dict[str, str|list]: Slides with titles ({'Intro': 'a.mp4', 'Demo': ['b.mp4', 'c.png']})
            - dict[str, dict[str, str]]: Slides with titles and labels ({'Intro': {'cat': 'a.mp4', 'dog': 'b.png'}})
        presentation_name (str): Name for the presentation. Default: auto-generated from timestamp.
        folder_name (str): Name for Google Drive folder. Default: auto-generated from timestamp.
        label_position (str): Where labels appear relative to media. Default: 'top'.
            - 'top': Labels above media
            - 'bottom': Labels below media
        bg_color: Background color for slides. Default: None (white).
            Accepts: color name ('black', 'white', 'blue'), hex ('#FFAABB'), or RGB tuple ((255, 170, 187)).
        font_color: Text color for titles and labels. Default: None (black).
            Accepts: same formats as bg_color.
        font (str): Font family name. Default: 'Lexend'.
        title_size (int): Title font size in points. Default: 24.
        label_size (int): Label font size in points. Default: 12.

    Returns:
        dict: {'folder_id', 'folder_url', 'media', 'presentation': {'id', 'url', 'public_url', 'name'}}

    Examples:
        >>> media_to_slides(['a.mp4', 'b.png'])  # 2 slides, 1 item each
        >>> media_to_slides([['a.mp4', 'b.png'], 'c.mp4'])  # slide 1: 2-item grid, slide 2: single
        >>> media_to_slides({'Intro': 'a.mp4', 'Demo': ['b.mp4', 'c.png']})  # 2 titled slides
        >>> media_to_slides({'Gallery': {'cat': 'a.png', 'dog': 'b.png'}})  # 1 slide, titled, labeled grid
        >>> media_to_slides(files, bg_color='black', font_color='white')  # dark theme
        >>> media_to_slides(files, label_position='bottom', label_size=10)  # labels below, smaller
    """
    slides = normalize_slides_input(layout)

    # Flatten to get unique paths
    all_paths = []
    for slide in slides:
        for path in slide["paths"]:
            if path not in all_paths:
                all_paths.append(path)

    if not all_paths:
        raise ValueError(
            f"No media files found in layout. "
            f"Got {len(slides)} slides but no valid paths. "
            f"Layout type: {type(layout).__name__}, "
            f"Input: {repr(layout)[:500]}"
        )

    if folder_name is None:
        folder_name = f"Media_{time.strftime('%Y%m%d_%H%M%S')}"
    if presentation_name is None:
        presentation_name = folder_name

    rp.fansi_print(
        f"Uploading {len(all_paths)} media files to Google Drive...",
        "cyan",
        "bold",
    )
    for p in all_paths:
        rp.fansi_print(f"  {rp.get_file_name(p)}", "white")

    creds = get_credentials()
    drive_service = build("drive", "v3", credentials=creds)
    slides_service = build("slides", "v1", credentials=creds)

    rp.fansi_print(f"\nCreating folder: rp/generated_slides/{folder_name}", "cyan")
    parent_id = get_rp_slides_folder(drive_service)
    folder_id = create_folder(drive_service, folder_name, parent_id)
    folder_url = FOLDER_URL.format(folder_id)
    rp.fansi_print(f"  {folder_url}", "white")

    rp.fansi_print("\nUploading media...", "cyan")
    media = upload_media_sequential(drive_service, all_paths, folder_id)

    path_to_media = dict(zip(all_paths, media))

    rp.fansi_print("\nMaking files publicly accessible...", "cyan")
    start_time = time.time()
    for i, m in enumerate(media):
        elapsed = time.time() - start_time
        progress_str = _format_progress(i + 1, len(media), i, len(media), elapsed, use_bytes=False)
        rp.fansi_print(f"  {progress_str} {m['name']}", "cyan")
        make_file_public(drive_service, m["id"])

    # Build slides_data for create_slides_with_media_grid
    slides_data = []
    for slide in slides:
        slides_data.append(
            {
                "media": [path_to_media[p] for p in slide["paths"]],
                "title": slide.get("title"),
                "labels": slide.get("labels"),
            }
        )

    rp.fansi_print(f"\nCreating presentation: {presentation_name}", "cyan")
    rp.fansi_print(f"  {len(slides)} slides", "white")
    for i, slide in enumerate(slides):
        title_str = f" - {slide['title']}" if slide.get("title") else ""
        rp.fansi_print(
            f"    Slide {i+1}: {len(slide['paths'])} items{title_str}", "white"
        )

    presentation = create_slides_with_media_grid(
        slides_service,
        drive_service,
        slides_data,
        presentation_name,
        label_position=label_position,
        bg_color=bg_color,
        font_color=font_color,
        font=font,
        title_size=title_size,
        label_size=label_size,
    )

    drive_service.files().update(
        fileId=presentation["id"],
        addParents=folder_id,
        fields="id",
    ).execute()

    rp.fansi_print("\nSetting sharing permissions...", "cyan")
    public_url = make_public(drive_service, presentation["id"])

    rp.fansi_print("\nSuccess!", "green", "bold")
    rp.fansi_print(f"  Media: {len(media)}", "green")
    rp.fansi_print(f"  Slides: {len(slides)}", "green")
    rp.fansi_print(f"  Folder: {folder_url}", "green")
    if public_url:
        rp.fansi_print(
            f"  Presentation (public): {public_url}", "green", "bold"
        )
    else:
        rp.fansi_print(
            f"  Presentation: {presentation['url']}", "green", "bold"
        )

    return {
        "folder_id": folder_id,
        "folder_url": folder_url,
        "media": media,
        "presentation": {
            "id": presentation["id"],
            "url": presentation["url"],
            "public_url": public_url,
            "name": presentation_name,
        },
    }


SORT_METHODS = {"name", "date", "size", "number"}


def get_media_files(path_or_glob: str, sort_by: str = "name") -> list[str]:
    """Get media files from a folder or glob pattern, sorted."""
    if rp.folder_exists(path_or_glob):
        exts = " ".join(
            ext.lstrip(".") for ext in VIDEO_EXTENSIONS | IMAGE_EXTENSIONS
        )
        return rp.get_all_files(
            path_or_glob, file_extension_filter=exts, sort_by=sort_by
        )
    else:
        files = [f for f in rp.glob(path_or_glob) if is_media_path(f)]
        if sort_by == "number":
            return rp.sorted_by_number(files)
        elif sort_by == "date":
            return sorted(files, key=rp.get_file_date)
        elif sort_by == "size":
            return sorted(files, key=rp.get_file_size)
        return sorted(files, key=lambda f: rp.get_file_name(f).lower())


def cli(
    *paths,
    name: str = None,
    folder_name: str = None,
    title: str = None,
    captions: bool = False,
    label_position: str = "top",
    bg_color: str = None,
    font_color: str = None,
    font: str = DEFAULT_FONT,
    title_size: int = DEFAULT_TITLE_SIZE,
    label_size: int = DEFAULT_LABEL_SIZE,
    sort_by: str = "name",
    per_slide: int = None,
):
    """Upload media to Google Drive and create a Google Slides presentation.

    Arguments:
        paths           Media files, folders, or glob patterns (e.g., "*.png")

    Options:
        --name NAME             Presentation name (default: auto-generated timestamp)
        --folder_name NAME      Google Drive folder name (default: auto-generated timestamp)
        --title TITLE           Slide title (applies to all slides)
        --captions              Use filenames as captions for each media item
        --label_position POS    Label position: 'top' (default) or 'bottom'
        --bg_color COLOR        Background color: name ('black'), hex ('#FFAABB'), default: white
        --font_color COLOR      Text color: name ('white'), hex ('#FFAABB'), default: black
        --font FONT             Font family (default: Lexend)
        --title_size SIZE       Title font size in pt (default: 24)
        --label_size SIZE       Label font size in pt (default: 12)
        --sort_by METHOD        Sort files by: 'name' (default), 'date', 'size', 'number'
        --per_slide N           Items per slide (optional, default: 1)

    Supported formats:
        Videos: .mp4, .mov, .avi, .mkv, .webm
        Images: .png, .jpg, .jpeg, .gif, .bmp, .webp

    Examples:
        rp run ppt media_to_slides video1.mp4 image.png                      # 2 files -> 2 slides
        rp run ppt media_to_slides media_folder/                             # folder -> one slide per file
        rp run ppt media_to_slides "*.png" --name "My Images" --captions     # glob with captions
        rp run ppt media_to_slides folder/ --title "Demo" --bg_color black --font_color white  # dark theme
        rp run ppt media_to_slides frames/ --sort_by number --captions --label_position bottom

    Note: First run opens browser for Google OAuth authentication.
    """
    # Collect media files
    media_paths = []
    for p in paths:
        if rp.folder_exists(p) or "*" in p or "?" in p:
            media_paths.extend(get_media_files(p, sort_by))
        elif rp.file_exists(p) and is_media_path(p):
            media_paths.append(p)

    if not media_paths:
        raise ValueError(
            f"No media files found. Searched {len(paths)} paths. "
            f"Supported formats: {', '.join(MEDIA_EXTENSIONS)}"
        )

    # Split into grids if requested
    if per_slide is not None:
        media_paths = rp.split_into_sublists(media_paths, per_slide)

    # Build layout
    if captions:
        # Each item gets its filename as a label, one per slide (or per grid if per_slide used)
        layout = [
            {rp.get_file_name(p, include_file_extension=False): p}
            if isinstance(p, str) else
            {rp.get_file_name(x, include_file_extension=False): x for x in p}
            for p in media_paths
        ]
        if title:
            layout = {title: layout[0]} if len(layout) == 1 else layout
    elif title:
        layout = {title: media_paths}
    else:
        layout = media_paths

    result = media_to_slides(
        layout,
        presentation_name=name,
        folder_name=folder_name,
        label_position=label_position,
        bg_color=bg_color,
        font_color=font_color,
        font=font,
        title_size=title_size,
        label_size=label_size,
    )
    print(f"\nPresentation URL: {result['presentation']['url']}")
    return result


if __name__ == "__main__":
    rp.pip_import("fire")
    import fire

    fire.Fire(cli)
