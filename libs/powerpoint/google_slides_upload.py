"""
Upload PPTX files to Google Drive, convert to Google Slides, and merge into one presentation.

Uses Google Apps Script for slide merging (REST API doesn't support cross-presentation slide copy).

Usage:
    python google_slides_upload.py folder_with_pptx_parts/
    python google_slides_upload.py part1.pptx part2.pptx part3.pptx
"""

import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import rp

rp.pip_import('google.auth')
rp.pip_import('google_auth_oauthlib')
rp.pip_import('googleapiclient')
rp.pip_import('tqdm')
rp.pip_import('requests')

from tqdm import tqdm
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Scopes needed for Drive upload, Slides access, and Apps Script execution
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/script.projects',
    'https://www.googleapis.com/auth/script.deployments',
]

# Encrypted OAuth client credentials (safe to push to GitHub)
CRYPT_CREDS = 'UFdFTkMAAAAxg6N2ZXIBq2tkZl9wcm9maWxlp3JwXzIwMjWuY2lwaGVyX3Byb2ZpbGWncnBfMjAyNaeCKdJD5499vDY/GtDYQPp1fLudX4fkAY7ZheNoE21GhwufvDXIQD1Ro8QYRZYWOC2TRI8q6QhNFYmos/0l3EewcWg89hRbfmtCe0u6TRA19/EOMkefsWl/zuN9ghtwdFbadX3o1srmo/RyrmU3FN4mjDbnOvUjeGNwEuscLNCMaV7SUt/kUXw6qwOWymohvlg5q6lga4I4r0VMq8rHjQPlpICIFoBqppglaejqf+P9KEWZgskyHPjuzc2QYHO8i5CVGz6Oqp7hIBauyLwvuKaAC+QQ3/RQHdxAxBOT8Ml22yFYbTk0iEyrq82ssNGOb5tOE5w6XamvohuBXJHeTJZuJTAgsH1P6JP7wIYLgjLHGLfneHIk61FsuRAVtyvdzbfTMXSxL3GWn4FDbVhXCb3nxIK2rKGNYvpNcC5jZh+Qw4IUGNHLUr7pIRHEEk8k5NhsbS1ndwUDOAKePRbN/wEX/rZ+KrsEGG4nWiKymHquZK1NtSXmzZaE43epEcBLmVznPSAW0iRheP2PtWqlYGpjsXqzum6ggCZb4Nt5ZwiCV2vl/1ReqENYa6y9Nz0sd7jrzVOcR25Hm3CL+YxVv9LxiPmYoPjEXgpgOExkzzpR'
_creds_json = rp.decrypt_bytes_with_password(rp.base64_to_bytes(CRYPT_CREDS), 'elbow').decode()
CLIENT_JSON_FILE = rp.get_cache_file_path(_creds_json, file_extension='json')
rp.save_text_file(_creds_json, CLIENT_JSON_FILE)


TOKEN_PATH = rp.with_file_name(__file__, 'token.json', keep_extension=False)


def get_credentials(token_path: str = None) -> Credentials:
    """Get or refresh Google API credentials."""
    if token_path is None:
        token_path = TOKEN_PATH
    creds = None

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_JSON_FILE, SCOPES)
            # Try local server first (browser), fall back to console (headless)
            try:
                creds = flow.run_local_server(port=0)
            except Exception:
                # Headless: prints URL, user pastes auth code
                creds = flow.run_console()

        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds


def create_folder(service, folder_name: str, parent_id: str = None) -> str:
    """Create a folder on Google Drive. Returns folder ID."""
    metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        metadata['parents'] = [parent_id]

    folder = service.files().create(body=metadata, fields='id').execute()
    return folder.get('id')


def make_public(service, file_id: str) -> str:
    """
    Make a file publicly viewable by anyone with the link.
    Returns the shareable link, or None if sharing failed (e.g., org policy).
    """
    try:
        service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'},
            fields='id'
        ).execute()
        return f"https://docs.google.com/presentation/d/{file_id}/view"
    except HttpError as e:
        # Some orgs block public sharing - fail silently
        rp.fansi_print(f"  (Could not make public: {e.reason})", 'yellow')
        return None


def upload_pptx_as_slides(
    service,
    file_path: str,
    folder_id: str = None,
    progress_callback=None
) -> dict:
    """
    Upload a PPTX file and convert to Google Slides.

    Returns dict with 'id', 'name', 'url'.
    """
    file_size = rp.get_file_size(file_path)

    metadata = {
        'name': rp.get_file_name(file_path, include_file_extension=False),
        'mimeType': 'application/vnd.google-apps.presentation',  # Convert to Slides
    }
    if folder_id:
        metadata['parents'] = [folder_id]

    media = MediaFileUpload(
        file_path,
        mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
        chunksize=5 * 1024 * 1024,  # 5MB chunks
        resumable=True
    )

    request = service.files().create(body=metadata, media_body=media, fields='id,name,webViewLink')

    response = None
    retries = 0
    max_retries = 5
    while response is None:
        try:
            status, response = request.next_chunk()
            if status and progress_callback:
                progress_callback(status.progress(), file_size)
            retries = 0  # Reset on success
        except HttpError as e:
            if e.resp.status in [500, 502, 503, 504] or e.resp.status == 308:
                retries += 1
                if retries > max_retries:
                    raise
                time.sleep(2 ** retries)  # Exponential backoff
            else:
                raise

    return {
        'id': response.get('id'),
        'name': response.get('name'),
        'url': response.get('webViewLink'),
    }


def upload_pptx_files_sequential(
    service,
    file_paths: list[str],
    folder_id: str = None,
) -> list[dict]:
    """
    Upload multiple PPTX files sequentially with progress bars.

    Returns list of dicts with 'id', 'name', 'url' in the same order as input.
    """
    tqdm = rp.pip_import('tqdm').tqdm
    results = []

    for i, fp in enumerate(file_paths):
        size = rp.get_file_size(fp)
        pbar = tqdm(
            total=size,
            desc=rp.get_file_name(fp),
            unit='B',
            unit_scale=True,
        )
        last_progress = [0]

        def progress_cb(progress, total):
            current = int(progress * total)
            pbar.update(current - last_progress[0])
            last_progress[0] = current

        result = upload_pptx_as_slides(service, fp, folder_id, progress_cb)
        pbar.close()
        rp.fansi_print("  Uploaded: " + result['url'], 'green')
        results.append(result)

    return results


# Google Apps Script web app for merging slides across presentations.
# Edit the script: https://script.google.com/home/projects/1zWUiYdF8iBHmDu4vsOpDS6JR8nXOiXr1qCec5FmbhAZqUrZsdr8tMv1s/edit
#
# Why this exists: Google Slides REST API cannot copy slides between presentations.
# Only Apps Script's SlidesApp.appendSlide() can do this. The web app receives
# presentation IDs via POST, creates a new presentation, and appends all slides.
#
# The script code (doPost): receives {presentationIds: [...], mergedName: "..."},
# creates new presentation, removes default blank slide, loops through each source
# presentation calling merged.appendSlide(slide) for each slide, returns JSON with
# {success: true, presentationId, url, slideCount}.
#
# Deployment settings (critical):
#   - Execute as: "Me" (runs with deployer's permissions to create presentations)
#   - Who has access: "Anyone" (allows unauthenticated HTTP calls from Python)
#
# Future users: They authenticate once via OAuth (token.json) for Drive upload.
# The merge web app runs as the deployer (Ryan), so users don't need separate
# Apps Script permissions - they just need Drive access to upload the source files.
MERGE_WEBAPP_URL = 'https://script.google.com/macros/s/AKfycbyt8us8O8hjpg-TWcLNRYc1i5wZD9XViUi9_Zc6RyIIswGNKhf-oRAcGLvpVFaOXidR/exec'


def share_presentations_for_merge(presentation_ids: list[str]) -> None:
    """Share presentations with 'anyone with link' so the web app can access them."""
    creds = get_credentials()
    drive_service = build('drive', 'v3', credentials=creds)

    for pres_id in presentation_ids:
        drive_service.permissions().create(
            fileId=pres_id,
            body={'type': 'anyone', 'role': 'reader'},
            fields='id'
        ).execute()


def merge_presentations_via_webapp(
    presentation_ids: list[str],
    merged_name: str = 'Merged Presentation',
    auto_share: bool = True,
) -> dict:
    """
    Merge multiple Google Slides presentations into one using a deployed Apps Script web app.

    This works around the REST API limitation that doesn't support cross-presentation
    slide copying. The web app uses Apps Script's appendSlide() method.

    Returns dict with 'presentationId', 'url', 'slideCount'.
    """

    if auto_share:
        share_presentations_for_merge(presentation_ids)

    response = requests.post(
        MERGE_WEBAPP_URL,
        json={'presentationIds': presentation_ids, 'mergedName': merged_name},
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 401 or (response.status_code == 200 and 'accounts.google.com' in response.text):
        raise RuntimeError(
            f"Merge web app authentication error (status {response.status_code}).\n"
            "The web app requires redeployment with public access:\n"
            "  1. Go to https://script.google.com/home and open your project\n"
            "  2. Deploy > Manage deployments > Edit (pencil icon)\n"
            "  3. Change 'Who has access' to 'Anyone' (not 'Anyone with Google account')\n"
            "  4. Click Deploy\n"
            "  5. If URL changed, update MERGE_WEBAPP_URL in google_slides_upload.py"
        )
    if response.status_code != 200:
        raise RuntimeError(f"Merge web app error: {response.status_code} {response.text}")

    result = response.json()
    if not result.get('success'):
        raise RuntimeError(f"Merge failed: {result.get('error', 'Unknown error')}")

    return result


def upload_and_merge_pptx(
    pptx_paths: list[str],
    folder_name: str = None,
    merged_name: str = None,
    parent_folder_id: str = None,
    max_workers: int = 4,
) -> dict:
    """
    Upload multiple PPTX files, convert to Google Slides, and merge into one presentation.

    Args:
        pptx_paths: List of paths to PPTX files (will be merged in this order).
        folder_name: Name for the Google Drive folder. If None, auto-generated.
        merged_name: Name for the merged presentation. If None, auto-generated.
        parent_folder_id: Optional parent folder ID on Google Drive.
        max_workers: Number of parallel upload threads.

    Returns:
        Dict with 'folder_id', 'folder_url', 'parts' (list of uploaded presentations),
        'merged' (the merged presentation info).
    """
    # Sort paths by part number if they follow the naming convention
    def extract_part_num(path):
        match = re.search(r'part(\d+)', path, re.IGNORECASE)
        return int(match.group(1)) if match else 0

    pptx_paths = sorted(pptx_paths, key=extract_part_num)

    # Generate names if not provided
    if folder_name is None:
        first_file = rp.get_file_name(pptx_paths[0], include_file_extension=False)
        folder_name = re.sub(r'_part\d+$', '', first_file, flags=re.IGNORECASE)

    if merged_name is None:
        merged_name = folder_name

    rp.fansi_print(f"Uploading {len(pptx_paths)} PPTX files to Google Drive...", 'cyan', 'bold')
    for p in pptx_paths:
        rp.fansi_print(f"  {rp.get_file_name(p)}", 'white')

    # Authenticate
    creds = get_credentials()
    drive_service = build('drive', 'v3', credentials=creds)

    # Create folder
    rp.fansi_print(f"\nCreating folder: {folder_name}", 'cyan')
    folder_id = create_folder(drive_service, folder_name, parent_folder_id)
    folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
    rp.fansi_print(f"  {folder_url}", 'white')

    # Upload all PPTX files sequentially (parallel uploads crash)
    rp.fansi_print("\nUploading and converting to Google Slides...", 'cyan')
    parts = upload_pptx_files_sequential(drive_service, pptx_paths, folder_id)

    for part in parts:
        rp.fansi_print(f"  Uploaded: {part['name']}", 'green')

    # Merge presentations using web app
    rp.fansi_print(f"\nMerging {len(parts)} presentations into one...", 'cyan')
    presentation_ids = [p['id'] for p in parts]

    merged = merge_presentations_via_webapp(presentation_ids, merged_name)

    # Move merged presentation to the folder
    drive_service.files().update(
        fileId=merged['presentationId'],
        addParents=folder_id,
        fields='id'
    ).execute()

    # Try to make it publicly viewable (may fail due to org policy)
    rp.fansi_print("\nSetting sharing permissions...", 'cyan')
    public_url = make_public(drive_service, merged['presentationId'])

    merged_url = f"https://docs.google.com/presentation/d/{merged['presentationId']}/edit"
    share_url = public_url or merged_url

    rp.fansi_print("\nSuccess!", 'green', 'bold')
    rp.fansi_print(f"  Total slides: {merged['slideCount']}", 'green')
    if public_url:
        rp.fansi_print(f"  Shareable link (anyone can view): {public_url}", 'green', 'bold')
    else:
        rp.fansi_print(f"  Edit link: {merged_url}", 'green')

    return {
        'folder_id': folder_id,
        'folder_url': folder_url,
        'parts': parts,
        'merged': {
            'id': merged['presentationId'],
            'url': merged_url,
            'share_url': share_url,
            'name': merged_name,
            'slideCount': merged['slideCount'],
        }
    }


HELP = """Upload PPTX files to Google Drive, convert to Google Slides, and merge.

Usage:
    python google_slides_upload.py <paths...> [options]
    python google_slides_upload.py <folder> [options]

Arguments:
    paths           One or more PPTX file paths
    folder          A folder containing PPTX files

Options:
    --folder-name   Name for Google Drive folder (default: auto from first filename)
    --merged-name   Name for merged presentation (default: same as folder-name)

Examples:
    python google_slides_upload.py output_folder/
    python google_slides_upload.py part1.pptx part2.pptx part3.pptx
    python google_slides_upload.py output_folder/ --folder-name "My Presentation"
    python google_slides_upload.py output_folder/ --merged-name "Final Presentation"
    python google_slides_upload.py *.pptx --folder-name "Project X" --merged-name "Project X Final"

Creates on Google Drive:
    MyDrive/<folder_name>/
        <name>_part1    <- Google Slides (converted from PPTX)
        <name>_part2 ...
        <merged_name>   <- merged presentation with all slides

Note: First run opens browser for Google OAuth."""


if __name__ == '__main__':
    import sys

    args = sys.argv[1:]

    if not args or args[0] in ('-h', '--help', 'help'):
        print(HELP)
        sys.exit(0)

    # Parse arguments
    paths = []
    folder_name = None
    merged_name = None

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '--folder-name' and i + 1 < len(args):
            folder_name = args[i + 1]
            i += 1
        elif arg == '--merged-name' and i + 1 < len(args):
            merged_name = args[i + 1]
            i += 1
        elif arg in ('-h', '--help'):
            print(HELP)
            sys.exit(0)
        elif not arg.startswith('--'):
            paths.append(arg)
        i += 1

    if not paths:
        print("Error: No PPTX files or folder specified\n")
        print(HELP)
        sys.exit(1)

    # Handle single folder path
    if len(paths) == 1 and rp.folder_exists(paths[0]):
        folder = paths[0]
        pptx_paths = sorted(rp.glob(rp.path_join(folder, '*.pptx')))
        if not pptx_paths:
            print(f"Error: No .pptx files found in {folder}")
            sys.exit(1)
    else:
        pptx_paths = paths

    result = upload_and_merge_pptx(pptx_paths, folder_name, merged_name)
    print(f"\nMerged presentation URL: {result['merged']['url']}")
