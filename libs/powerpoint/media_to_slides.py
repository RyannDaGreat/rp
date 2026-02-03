"""
Upload media files (videos/images) to Google Drive and create a Google Slides presentation.

Usage:
    rp run ppt media_to_slides video1.mp4 video2.mp4 image.png
    rp run ppt media_to_slides folder_with_media/
    rp run ppt media_to_slides *.mp4 *.png --name "My Presentation"

Glossary:
    content     Any string input. If it's a path to an existing file, use the file.
                Otherwise treat it as literal text to display in a text box.
    media       An image or video file (uploaded to Google Drive).
    text        Literal string or contents of a non-media file, shown as a text box.
    title       Large text at the top of a slide (--title_size, default 24pt).
    text_size   Font size for text boxes (--text_size, default 12pt).
    label       Small text near each grid item (--label_size, default: same as text_size).
                In the CLI, --captions creates labels from filenames.
"""

import os
import time
import tempfile

import rp

__all__ = ["cli", "media_to_slides"]

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
DEFAULT_TITLE_SIZE, DEFAULT_TEXT_SIZE = 24, 12

# URL templates
DRIVE_FILE_URL = "https://drive.google.com/uc?id={}"
SLIDES_URL = "https://docs.google.com/presentation/d/{}/edit"
FOLDER_URL = "https://drive.google.com/drive/folders/{}"

# Upload cache path (same folder as token.json)
UPLOAD_CACHE_PATH = rp.with_file_name(TOKEN_PATH, "upload_cache.json", keep_extension=False)

# Cache modes: "off" (no cache), "copy" (server-side copy), "reuse" (direct URL reuse)
CACHE_MODES = {"off", "copy", "reuse"}


def _load_upload_cache() -> dict:
    """Load the upload cache from disk. Returns empty dict if not found."""
    if rp.file_exists(UPLOAD_CACHE_PATH):
        return rp.load_json(UPLOAD_CACHE_PATH)
    return {}


def _save_upload_cache(cache: dict) -> None:
    """Save the upload cache to disk."""
    rp.save_json(cache, UPLOAD_CACHE_PATH)


def copy_drive_file(
    service,
    file_id: str,
    folder_id: str,
    new_name: str = None,
) -> dict:
    """
    Copy a file on Google Drive to a folder (server-side, fast).

    This creates a new file object in the target folder - like a hard link,
    deleting one copy doesn't affect the other.

    Args:
        service: Google Drive API service instance
        file_id: ID of the file to copy
        folder_id: ID of the destination folder
        new_name: Optional new name for the copy

    Returns:
        Dict with 'id', 'name', 'webViewLink', 'webContentLink' of the new copy
    """
    metadata = {"parents": [folder_id]}
    if new_name:
        metadata["name"] = new_name

    result = service.files().copy(
        fileId=file_id,
        body=metadata,
        fields="id,name,webViewLink,webContentLink",
    ).execute()

    return {
        "id": result.get("id"),
        "name": result.get("name"),
        "webViewLink": result.get("webViewLink"),
        "webContentLink": result.get("webContentLink"),
    }

# Media types
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
MEDIA_EXTENSIONS = VIDEO_EXTENSIONS | IMAGE_EXTENSIONS
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


def is_media_file(path: str) -> bool:
    """Check if path is an existing media file (image or video)."""
    return rp.file_exists(path) and _get_ext(path) in MEDIA_EXTENSIONS


def content_to_slide_item(content: str, path_to_media: dict) -> dict:
    """Convert a content string to a slide item dict.

    Args:
        content: File path or literal text
        path_to_media: Dict mapping media file paths to their uploaded Drive info

    Returns:
        Dict with either Drive info (for media) or {'is_text': True, 'text': str}
    """
    if is_media_file(content):
        return path_to_media[content]
    elif rp.file_exists(content):
        return {"is_text": True, "text": rp.text_file_to_string(content)}
    else:
        return {"is_text": True, "text": content}


def _parse_labeled_dict(d: dict) -> tuple[list, list]:
    """Parse {label: content} dict. Returns (contents, labels)."""
    labels = []
    contents = []
    for label, content in d.items():
        if isinstance(content, str):
            labels.append(label)
            contents.append(content)
    return contents, labels


def _parse_content(content, title=None) -> dict | None:
    """Parse content into a slide dict.

    Content can be:
    - A file path (if file exists, use it as image/video/text file)
    - Literal text (if file doesn't exist, render as text box)
    """
    if isinstance(content, str):
        return {"contents": [content], "title": title, "labels": None}
    if isinstance(content, dict):
        contents, labels = _parse_labeled_dict(content)
        if contents:
            return {"contents": contents, "title": title, "labels": labels}
    elif rp.is_non_str_iterable(content):
        contents = [c for c in content if isinstance(c, str)]
        if contents:
            return {"contents": contents, "title": title, "labels": None}
    return None


def normalize_slides_input(layout) -> list[dict]:
    """
    Normalize flexible input formats into list of slide dicts.

    Returns list of {'contents': [...], 'title': str or None, 'labels': [...] or None}

    Each content item is either:
    - A path to an existing file (image, video, or text file to read)
    - Literal text (rendered as a text box)

    Accepts:
        - Single string: 'a.mp4' or 'Hello world'
        - List: ['a.mp4', 'b.png', 'Some text here']
        - Nested lists: [['a.mp4', 'b.png'], 'c.mp4'] -> grid on first slide
        - Dict with titles: {'Slide 1': ['a.mp4'], 'Notes': 'Some notes here'}
        - Dict with labels: {'Gallery': {'cat': 'cat.png', 'desc': 'A cute cat'}}
    """
    if isinstance(layout, str):
        return [{"contents": [layout], "title": None, "labels": None}]

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
    cache_mode: str = "copy",
) -> list[dict]:
    """Upload multiple media files sequentially with progress bars.

    Args:
        service: Google Drive API service instance
        file_paths: List of file paths to upload
        folder_id: Destination folder ID on Google Drive
        cache_mode: Cache behavior - "off", "copy", or "reuse" (bool also accepted)

    Returns:
        List of dicts with 'id', 'name', 'webViewLink', 'webContentLink', 'is_image'
    """
    if cache_mode is True:  cache_mode = "copy"
    if cache_mode is False: cache_mode = "off"
    if cache_mode not in CACHE_MODES:
        raise ValueError(f"cache_mode must be one of {CACHE_MODES}, got {cache_mode!r}")

    results = []
    total_bytes = sum(rp.get_file_size(fp) for fp in file_paths)
    uploaded_bytes = 0
    start_time = time.time()

    use_cache = cache_mode in ("copy", "reuse")

    # Load cache if using it
    cache = _load_upload_cache() if use_cache else {}
    cache_modified = False

    if cache_mode == "reuse":
        rp.fansi_print("  [reuse mode] Using cached URLs directly (no copy)", "yellow", "bold")

    for i, fp in enumerate(file_paths):
        size = rp.get_file_size(fp)
        elapsed = time.time() - start_time
        progress_str = _format_progress(i + 1, len(file_paths), uploaded_bytes, total_bytes, elapsed)
        rp.fansi_print(f"  {progress_str}", "cyan")

        file_name = rp.get_file_name(fp)
        file_hash = rp.get_sha256_hash(fp) if use_cache else None

        # Check cache for this file
        if use_cache and file_hash in cache:
            cached = cache[file_hash]
            if cache_mode == "reuse":
                # Reuse cached entry directly - no copy, no API call
                rp.fansi_print(f"  {file_name}: reusing cached URL", "yellow")
                cache_result = cached
                rp.fansi_print(f"  Reused: {result['webViewLink']}", "green")
            else:
                # Copy mode - server-side copy to new folder
                rp.fansi_print(f"  {file_name}: cache hit, copying...", "yellow")
                copy_result = copy_drive_file(
                    service,
                    cached["id"],
                    folder_id,
                    new_name=file_name,
                )
                cache_result=copy_result
                rp.fansi_print(f"  Copied: {result['webViewLink']}", "green")
            result = {
                "id": cache_result["id"],
                "name": cache_result["name"],
                "webViewLink": cache_result["webViewLink"],
                "webContentLink": cache_result["webContentLink"],
                "is_image": cached["is_image"],
            }
        else:
            # Upload normally
            pbar = tqdm(
                total=size,
                desc=file_name,
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
            rp.fansi_print(f"  Uploaded: {result['webViewLink']}", "green")

            # Add to cache (only for copy/reuse modes, not off)
            if cache_mode != "off" and file_hash:
                cache[file_hash] = {
                    "id": result["id"],
                    "name": result["name"],
                    "webViewLink": result["webViewLink"],
                    "webContentLink": result["webContentLink"],
                    "is_image": result["is_image"],
                }
                cache_modified = True

        uploaded_bytes += size
        results.append(result)

    # Save cache if modified
    if cache_modified:
        _save_upload_cache(cache)

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


# Navbar constants
NAVBAR_BUTTON_SIZE = 36
NAVBAR_PADDING = 12
NAVBAR_BUTTON_GAP = 8


def _get_nav_button_paths() -> tuple[str, str]:
    """Get paths to nav button PNGs, generating them if needed.

    Saves to same folder as token.json (user's config dir) so they persist
    and don't need to be regenerated or shipped with the package.
    """
    token_dir = rp.get_parent_folder(TOKEN_PATH)
    prev_path = rp.path_join(token_dir, "nav_prev.png")
    next_path = rp.path_join(token_dir, "nav_next.png")

    # Generate if either is missing
    if not rp.file_exists(prev_path) or not rp.file_exists(next_path):
        _generate_nav_button_pngs(prev_path, next_path)

    return prev_path, next_path


def _generate_nav_button_pngs(prev_path: str, next_path: str):
    """Generate nav button PNGs: white circle (50% alpha) with black triangle."""
    import cv2
    import numpy as np
    import math

    size = 144  # pixels (crisp when scaled down)
    center = size // 2
    radius = size // 2 - 4
    tri_radius = radius * 0.45 * 1.3  # triangle 1.3x larger

    white_bg = (255, 255, 255)
    black = (0, 0, 0)

    for direction, path in [("left", prev_path), ("right", next_path)]:
        img = np.zeros((size, size, 4), dtype=np.uint8)
        cv2.circle(img, (center, center), radius, (*white_bg, 128), -1, cv2.LINE_AA)

        # Equilateral triangle vertices
        angles = [180, 300, 60] if direction == "left" else [0, 120, 240]
        pts = np.array([
            [center + int(tri_radius * math.cos(math.radians(a))),
             center + int(tri_radius * math.sin(math.radians(a)))]
            for a in angles
        ], dtype=np.int32)

        cv2.fillPoly(img, [pts], (*black, 255), cv2.LINE_AA)
        cv2.imwrite(path, img)


def _upload_nav_buttons(drive_service, folder_id: str) -> dict:
    """Upload nav button PNGs to Drive, return {name: file_id}."""
    prev_path, next_path = _get_nav_button_paths()
    result = {}
    for name, path in [("prev", prev_path), ("next", next_path)]:
        uploaded = upload_media(drive_service, path, folder_id)
        make_file_public(drive_service, uploaded["id"])
        result[name] = uploaded["id"]
    return result


def _navbar_button_requests(
    obj_id: str,
    page_id: str,
    center_x: float,
    center_y: float,
    size: float,
    image_url: str,
    target_slide_id: str,
) -> list:
    """Create requests for a nav button image with transparent linked shape overlay."""
    half = size / 2
    x, y = center_x - half, center_y - half
    overlay_id = obj_id + "_link"

    return [
        # Create image
        {
            "createImage": {
                "objectId": obj_id,
                "url": image_url,
                "elementProperties": _element_props(page_id, x, y, size, size),
            }
        },
        # Create transparent shape overlay for the link
        {
            "createShape": {
                "objectId": overlay_id,
                "shapeType": "ELLIPSE",
                "elementProperties": _element_props(page_id, x, y, size, size),
            }
        },
        # Make shape fully transparent
        {
            "updateShapeProperties": {
                "objectId": overlay_id,
                "shapeProperties": {
                    "shapeBackgroundFill": {"propertyState": "NOT_RENDERED"},
                    "outline": {"propertyState": "NOT_RENDERED"},
                },
                "fields": "shapeBackgroundFill,outline",
            }
        },
        # Insert invisible text to hold the link (single space)
        {"insertText": {"objectId": overlay_id, "text": " "}},
        # Add link to the text
        {
            "updateTextStyle": {
                "objectId": overlay_id,
                "style": {
                    "link": {"pageObjectId": target_slide_id},
                    "fontSize": _pt(size),  # Make clickable area large
                },
                "fields": "link,fontSize",
            }
        },
    ]


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
    title_font: str = None,
    title_color=None,
    text_size: int = None,
    text_font: str = None,
    text_color=None,
    label_size: int = None,
    label_font: str = None,
    label_color=None,
    autoplay: bool = True,
    navbar: bool = False,
    nav_button_urls: dict = None,
) -> dict:
    """
    Create a Google Slides presentation with content in grids.

    Args:
        slides_data: List of {'media': [...], 'title': str|None, 'labels': [...]|None}
            Each item in 'media' can be:
            - Image/video: dict with 'id', 'is_image' (from Drive upload)
            - Text: dict with 'is_text': True, 'text': str (content to display)
        label_position: 'top' or 'bottom' - where labels appear relative to content
        bg_color: Background color (name like 'black', hex like '#FFAABB', or RGB tuple)
        font_color: Default text color (same format as bg_color)
        font: Default font family name (default: 'Lexend')
        title_size: Title font size in pt (default: 24)
        title_font: Title font family (default: same as font)
        title_color: Title color (default: same as font_color)
        text_size: Text box font size in pt (default: 12)
        text_font: Text box font family (default: same as font)
        text_color: Text box color (default: same as font_color)
        label_size: Label font size in pt (default: same as text_size)
        label_font: Label font family (default: same as text_font)
        label_color: Label color (default: same as text_color)
        autoplay: Whether videos autoplay when the slide is shown. Default: True.
        navbar: Whether to add prev/next navigation buttons. Default: False.
        nav_button_urls: Dict with 'prev' and 'next' Drive URLs for nav buttons (required if navbar=True).
    """
    # Apply defaults: text inherits from font/font_color, label inherits from text
    if text_size   is None: text_size   = DEFAULT_TEXT_SIZE
    if text_font   is None: text_font   = font
    if text_color  is None: text_color  = font_color
    if label_size  is None: label_size  = text_size
    if label_font  is None: label_font  = text_font
    if label_color is None: label_color = text_color
    if title_font  is None: title_font  = font
    if title_color is None: title_color = font_color

    bg_rgb = parse_color(bg_color)
    title_rgb = parse_color(title_color)
    label_rgb = parse_color(label_color)
    text_rgb = parse_color(text_color)
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
        title = slide.get("title")
        slide_media = slide["media"]
        labels = slide.get("labels")

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
        navbar_h = (NAVBAR_BUTTON_SIZE + NAVBAR_PADDING) if navbar else 0
        grid_top, grid_h = title_h, SLIDE_HEIGHT_PT - title_h - navbar_h

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
                    title_font,
                    title_size,
                    title_rgb,
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

            if media.get("is_text"):
                # Text content renders as a text box in the grid cell
                text_content = media["text"]
                requests.append(
                    {
                        "createShape": {
                            "objectId": obj_id,
                            "shapeType": "TEXT_BOX",
                            "elementProperties": elem_props,
                        }
                    }
                )
                requests.append({"insertText": {"objectId": obj_id, "text": text_content}})
                style = {"fontSize": _pt(text_size), "fontFamily": text_font}
                if text_rgb:
                    style["foregroundColor"] = _fg_color(text_rgb)
                fields = "fontSize,fontFamily" + (",foregroundColor" if text_rgb else "")
                requests.append(
                    {"updateTextStyle": {"objectId": obj_id, "style": style, "fields": fields}}
                )
                requests.append(
                    {"updateParagraphStyle": {"objectId": obj_id, "style": {"alignment": "START"}, "fields": "alignment"}}
                )
            elif media.get("is_image"):
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
                if autoplay:
                    # Note (January 9, 2026): Google Slides API has a bug where setting autoPlay=True
                    # adds a SECOND animation entry instead of replacing the default "Play (on click)".
                    # This results in duplicate animations in the UI but autoplay still works.
                    # See: https://issuetracker.google.com/issues/283097101
                    autoplay_requests.append(
                        {
                            "updateVideoProperties": {
                                "objectId": obj_id,
                                "videoProperties": {"autoPlay": True},
                                "fields": "autoPlay",
                            }
                        }
                    )

            if labels and media_idx < len(labels) and labels[media_idx]:
                requests.extend(
                    _text_element_requests(
                        f"label_{media_counter}",
                        slide_id,
                        pos["label_x"],
                        pos["label_y"] + grid_top,
                        pos["label_width"],
                        label_h,
                        labels[media_idx],
                        label_font,
                        label_size,
                        label_rgb,
                    )
                )

            media_counter += 1

        # Add navbar buttons (PNG images with transparent link overlay)
        if navbar and nav_button_urls:
            btn_size = NAVBAR_BUTTON_SIZE
            btn_center_y = SLIDE_HEIGHT_PT - NAVBAR_PADDING - btn_size / 2
            n_slides = len(slides_data)
            # Prev button (links to previous slide, wraps to last)
            prev_slide_idx = (slide_idx - 1) % n_slides
            prev_center_x = NAVBAR_PADDING + btn_size / 2
            requests.extend(
                _navbar_button_requests(
                    f"nav_prev_{slide_idx}",
                    slide_id,
                    prev_center_x,
                    btn_center_y,
                    btn_size,
                    nav_button_urls["prev"],
                    f"slide_{prev_slide_idx}",
                )
            )
            # Next button (links to next slide, wraps to first)
            next_slide_idx = (slide_idx + 1) % n_slides
            next_center_x = prev_center_x + btn_size + NAVBAR_BUTTON_GAP
            requests.extend(
                _navbar_button_requests(
                    f"nav_next_{slide_idx}",
                    slide_id,
                    next_center_x,
                    btn_center_y,
                    btn_size,
                    nav_button_urls["next"],
                    f"slide_{next_slide_idx}",
                )
            )

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
    title_font: str = None,
    title_color=None,
    text_size: int = DEFAULT_TEXT_SIZE,
    text_font: str = None,
    text_color=None,
    label_size: int = None,
    label_font: str = None,
    label_color=None,
    autoplay: bool = True,
    navbar: bool = False,
    cache_mode: str = "copy",
    show_folder_size: bool = True,
) -> dict:
    """
    Upload media files (videos/images) and create a Google Slides presentation.

    Args:
        layout: Content to include. Accepts flexible formats:
            - str: Single file path ('a.mp4', 'notes.txt', 'readme.md')
            - list[str]: One file per slide (['a.mp4', 'b.png', 'notes.txt'])
            - list[list[str]]: Grid layouts ([['a.mp4', 'b.png'], 'c.mp4'])
            - dict[str, str|list]: Slides with titles ({'Intro': 'a.mp4', 'Notes': 'notes.txt'})
            - dict[str, dict[str, str]]: Slides with titles and labels
        presentation_name (str): Name for the presentation. Default: auto-generated from timestamp.
        folder_name (str): Name for Google Drive folder. Default: auto-generated from timestamp.
        label_position (str): Where labels appear relative to media. Default: 'top'.
        bg_color: Background color for slides. Default: None (white).
        font_color: Default text color. Default: None (black).
        font (str): Default font family. Default: 'Lexend'.
        title_size (int): Title font size in points. Default: 24.
        title_font (str): Title font family. Default: same as font.
        title_color: Title color. Default: same as font_color.
        text_size (int): Text box font size in points. Default: 12.
        text_font (str): Text box font family. Default: same as font.
        text_color: Text box color. Default: same as font_color.
        label_size (int): Label font size in points. Default: same as text_size.
        label_font (str): Label font family. Default: same as text_font.
        label_color: Label color. Default: same as text_color.
        autoplay (bool): Whether videos autoplay when the slide is shown. Default: True.
        navbar (bool): Whether to add prev/next navigation buttons. Default: False.
        cache_mode (str): How to handle previously uploaded files. Default: "copy".
            - "off": Always upload fresh (no caching)
            - "copy": Server-side copy of cached files to new folder (safe, isolated)
            - "reuse": Directly reuse cached URLs (fastest, but shared references)
        show_folder_size (bool): If True (default), append total file size to folder name.
            Useful because Google Drive doesn't show folder sizes. Default: True.

    Returns:
        dict: {'folder_id', 'folder_url', 'media', 'presentation': {'id', 'url', 'public_url', 'name'}}

    Examples:
        >>> media_to_slides(['a.mp4', 'b.png'])  # 2 slides, 1 item each
        >>> media_to_slides({'Intro': 'a.mp4', 'Notes': 'Hello world!'})  # media + text
        >>> media_to_slides(['Just some text'])  # text-only presentation
        >>> media_to_slides(files, bg_color='black', font_color='white')  # dark theme
    """
    slides = normalize_slides_input(layout)

    # Collect unique media file paths (only existing image/video files need upload)
    media_paths = []
    for slide in slides:
        for content in slide["contents"]:
            if is_media_file(content) and content not in media_paths:
                media_paths.append(content)

    if not slides:
        raise ValueError(
            f"No content found in layout. "
            f"Layout type: {type(layout).__name__}, "
            f"Input: {repr(layout)[:500]}"
        )

    # Cascade defaults: presentation_name -> folder_name -> auto-generated timestamp
    if presentation_name is None and folder_name is None:
        folder_name = f"Slides_{time.strftime('%Y%m%d_%H%M%S')}"
        presentation_name = folder_name
    elif presentation_name is None:
        presentation_name = folder_name
    elif folder_name is None:
        folder_name = presentation_name

    creds = get_credentials()
    drive_service = build("drive", "v3", credentials=creds)
    slides_service = build("slides", "v1", credentials=creds)

    folder_id = None
    folder_url = None
    media = []
    path_to_media = {}

    # Create folder if we have media files OR navbar (need to upload nav button images)
    if media_paths or navbar:
        # Append total file size to folder name (Google Drive doesn't show folder sizes)
        # In reuse mode, only count files that will actually be uploaded (cache misses)
        display_folder_name = folder_name
        if show_folder_size and media_paths:
            if cache_mode == "reuse":
                cache = _load_upload_cache()
                sizes = [rp.get_file_size(p) for p in media_paths if rp.get_sha256_hash(p) not in cache]
            else:
                sizes = rp.get_file_sizes(*media_paths)
            if sizes:
                total_size = sum(sizes)
                size_str = rp.human_readable_file_size(total_size, mib=False)
                display_folder_name = f"{folder_name} ({size_str})"
        rp.fansi_print(f"\nCreating folder: rp/generated_slides/{display_folder_name}", "cyan")
        parent_id = get_rp_slides_folder(drive_service)
        folder_id = create_folder(drive_service, display_folder_name, parent_id)
        folder_url = FOLDER_URL.format(folder_id)
        rp.fansi_print(f"  {folder_url}", "white")

    # Upload media files if any
    if media_paths:
        rp.fansi_print(
            f"\nUploading {len(media_paths)} media files to Google Drive...",
            "cyan",
            "bold",
        )
        for p in media_paths:
            rp.fansi_print(f"  {rp.get_file_name(p)}", "white")

        rp.fansi_print("\nUploading media...", "cyan")
        media = upload_media_sequential(drive_service, media_paths, folder_id, cache_mode=cache_mode)

        path_to_media = dict(zip(media_paths, media))

        # Skip permissions for reuse mode - cached files are already public
        if cache_mode != "reuse":
            rp.fansi_print("\nMaking files publicly accessible...", "cyan")
            start_time = time.time()
            for i, m in enumerate(media):
                elapsed = time.time() - start_time
                progress_str = _format_progress(i + 1, len(media), i, len(media), elapsed, use_bytes=False)
                rp.fansi_print(f"  {progress_str} {m['name']}", "cyan")
                make_file_public(drive_service, m["id"])

    # Build slides_data - each content item becomes either media or text box
    slides_data = []
    for slide in slides:
        slide_items = [content_to_slide_item(c, path_to_media) for c in slide["contents"]]
        slides_data.append({
            "media": slide_items,
            "title": slide.get("title"),
            "labels": slide.get("labels"),
        })

    # Upload nav button images if navbar enabled
    nav_button_urls = None
    if navbar:
        rp.fansi_print("\nUploading nav buttons...", "cyan")
        nav_ids = _upload_nav_buttons(drive_service, folder_id)
        nav_button_urls = {
            "prev": DRIVE_FILE_URL.format(nav_ids["prev"]),
            "next": DRIVE_FILE_URL.format(nav_ids["next"]),
        }

    rp.fansi_print(f"\nCreating presentation: {presentation_name}", "cyan")
    rp.fansi_print(f"  {len(slides_data)} slides", "white")

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
        title_font=title_font,
        title_color=title_color,
        label_size=label_size,
        label_font=label_font,
        label_color=label_color,
        text_size=text_size,
        text_font=text_font,
        text_color=text_color,
        autoplay=autoplay,
        navbar=navbar,
        nav_button_urls=nav_button_urls,
    )

    # Move presentation to folder if we created one
    if folder_id:
        drive_service.files().update(
            fileId=presentation["id"],
            addParents=folder_id,
            fields="id",
        ).execute()

    rp.fansi_print("\nSetting sharing permissions...", "cyan")
    public_url = make_public(drive_service, presentation["id"])

    rp.fansi_print("\nSuccess!", "green", "bold")
    if media:
        rp.fansi_print(f"  Media: {len(media)}", "green")
    rp.fansi_print(f"  Slides: {len(slides_data)}", "green")
    if folder_url:
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
        exts = " ".join(ext.lstrip(".") for ext in MEDIA_EXTENSIONS)
        return rp.get_all_files(
            path_or_glob, file_extension_filter=exts, sort_by=sort_by
        )
    else:
        files = [f for f in rp.glob(path_or_glob) if is_media_file(f)]
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
    title_font: str = None,
    title_color: str = None,
    text_size: int = DEFAULT_TEXT_SIZE,
    text_font: str = None,
    text_color: str = None,
    label_size: int = None,
    label_font: str = None,
    label_color: str = None,
    sort_by: str = "name",
    per_slide: int = None,
    autoplay: bool = True,
    navbar: bool = False,
    cache_mode: str = "copy",
    show_folder_size: bool = True,
):
    """Upload media to Google Drive and create a Google Slides presentation.

    Arguments:
        paths           Media files, folders, or glob patterns (e.g., "*.png")

    Options:
        --name NAME             Presentation name (default: same as --title, or auto-generated timestamp)
        --folder_name NAME      Google Drive folder name (default: same as --name)
        --title TITLE           Slide title (applies to all slides)
        --captions              Use filenames as captions for each media item
        --label_position POS    Label position: 'top' (default) or 'bottom'
        --bg_color COLOR        Background color: name ('black'), hex ('#FFAABB'), default: white
        --font_color COLOR      Default text color (default: black)
        --font FONT             Default font family (default: Lexend)
        --title_size SIZE       Title font size in pt (default: 24)
        --title_font FONT       Title font family (default: same as --font)
        --title_color COLOR     Title color (default: same as --font_color)
        --text_size SIZE        Text box font size in pt (default: 12)
        --text_font FONT        Text box font family (default: same as --font)
        --text_color COLOR      Text box color (default: same as --font_color)
        --label_size SIZE       Label font size in pt (default: same as --text_size)
        --label_font FONT       Label font family (default: same as --text_font)
        --label_color COLOR     Label color (default: same as --text_color)
        --sort_by METHOD        Sort files by: 'name' (default), 'date', 'size', 'number'.
                                Only applies to folders and glob patterns; individual files
                                keep the order you specify them.
        --per_slide N           Items per slide (optional, default: 1)
        --autoplay              Enable video autoplay (default: True). Use --noautoplay to disable.
        --navbar                Add prev/next navigation buttons (default: False)
        --cache_mode MODE       How to handle previously uploaded files (default: 'copy'):
                                  'off'   - No caching, always upload fresh
                                  'copy'  - Copy cached files to new folder (safe, each presentation isolated)
                                  'reuse' - Reuse cached URLs directly (fastest, saves Drive storage)
                                Benefits of 'reuse': Faster uploads, reduced Google Drive storage usage.
                                Risks of 'reuse': If the cached file's source folder is deleted, this
                                presentation's media will break. Only use for temporary presentations
                                or when you're sure the source media won't be deleted.
        --show_folder_size      Append total file size to folder name (default: True).
                                Google Drive doesn't show folder sizes, so this helps track storage.
                                In 'reuse' mode, only counts cache misses (files actually uploaded).
                                Use --noshow_folder_size to disable.

    Supported formats:
        Videos: .mp4, .mov, .avi, .mkv, .webm
        Images: .png, .jpg, .jpeg, .gif, .bmp, .webp
        Text:   Any string that's not a file path, or any non-media file

    Examples:
        rp run ppt media_to_slides video1.mp4 image.png                      # 2 files -> 2 slides
        rp run ppt media_to_slides media_folder/                             # folder -> one slide per file
        rp run ppt media_to_slides "*.png" --name "My Images" --captions     # glob with captions
        rp run ppt media_to_slides folder/ --title "Demo" --bg_color black --font_color white  # dark theme
        rp run ppt media_to_slides "Hello World" image.png                   # text + image
        rp run ppt media_to_slides "Big text" --text_size 36                 # larger text
        rp run ppt media_to_slides videos/ --noautoplay                      # disable video autoplay
        rp run ppt media_to_slides videos/ --navbar                          # add prev/next buttons
        rp run ppt media_to_slides videos/ --cache_mode off                  # force re-upload all files
        rp run ppt media_to_slides videos/ --cache_mode reuse                # fastest, reuse cached URLs

    Note: First run opens browser for Google OAuth authentication.
    """
    # Collect content - files or literal text
    content = []
    for p in paths:
        if rp.folder_exists(p) or "*" in p or "?" in p:
            content.extend(get_media_files(p, sort_by))
        else:
            # Either a file path or literal text - both are valid
            content.append(p)

    if not content:
        raise ValueError(f"No content provided. Got {len(paths)} paths.")

    # Default name to title (folder_name cascading handled in media_to_slides)
    if name is None and title is not None:
        name = title

    # Split into grids if requested
    if per_slide is not None:
        content = rp.split_into_sublists(content, per_slide)

    # Build layout
    if captions:
        # Files get filename as label, literal text gets no label
        def get_label(item):
            if rp.file_exists(item):
                return rp.get_file_name(item, include_file_extension=False)
            return ""

        layout = [
            {get_label(p): p} if isinstance(p, str) else
            {get_label(x): x for x in p}
            for p in content
        ]
        if title:
            layout = {title: layout[0]} if len(layout) == 1 else layout
    elif title:
        layout = {title: content}
    else:
        layout = content

    result = media_to_slides(
        layout,
        presentation_name=name,
        folder_name=folder_name,
        label_position=label_position,
        bg_color=bg_color,
        font_color=font_color,
        font=font,
        title_size=title_size,
        title_font=title_font,
        title_color=title_color,
        label_size=label_size,
        label_font=label_font,
        label_color=label_color,
        text_size=text_size,
        text_font=text_font,
        text_color=text_color,
        autoplay=autoplay,
        navbar=navbar,
        cache_mode=cache_mode,
        show_folder_size=show_folder_size,
    )
    print(f"\nPresentation URL: {result['presentation']['url']}")
    return result


if __name__ == "__main__":
    rp.pip_import("fire")
    import fire

    fire.Fire(cli)
