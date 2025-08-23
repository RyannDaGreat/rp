# RP Network & Web Functions - Comprehensive Mapping

## Overview
The RP module contains a comprehensive suite of network and web-related functions spanning HTTP requests, API interactions, cloud storage, social media integration, email handling, and real-time communication. This document maps all network/web functions and their interconnections.

## Core HTTP/Web Functions

### Basic HTTP Operations
```python
# Core URL validation and handling
def is_valid_url(url: str) -> bool                        # Validates URL syntax
def open_url_in_web_browser(url: str)                     # Opens URL in default browser  
def google_search_url(query: str) -> None                 # Creates Google search URL
def open_google_search_in_web_browser(query: str)         # Opens Google search in browser

# Simple HTTP requests
def curl(url: str) -> str                                 # GET request returning text (like curl command)
def curl_bytes(url)                                       # GET request returning bytes
def unshorten_url(shortened_url)                          # Expand shortened URLs
def shorten_url(url: str) -> str                         # Shorten URLs using TinyURL
def dns_lookup(url: str) -> str                          # DNS resolution
```

### File Download System
The download system is built around a multiplexing pattern with protocol-specific backends:

```python
# Main download dispatcher
def download_url(url, path=None, *, skip_existing=False, show_progress=False, timeout=None)
    # Dispatches to appropriate backend based on URL:
    # - HTTP/HTTPS → requests with streaming
    # - s3:// → AWS CLI (aws s3 cp)
    # - gs:// → Google Cloud (gsutil cp)
    # - /cns/ → Google Colossus (fileutil cp)
    # - YouTube URLs → download_youtube_video()

# Batch operations
def download_urls(urls, paths=None, *, skip_existing=False, show_progress=False, max_workers=4, timeout=None)

# Caching system  
def download_url_to_cache(url, cache_dir=None, skip_existing=True, hash_func=None, show_progress=False, timeout=None)
def download_urls_to_cache(urls, *, cache_dir=None, skip_existing=True, hash_func=None, show_progress=False, timeout=None)
def get_cache_file_path(url, *, cache_dir=None, file_extension=None, hash_func=None)
def get_cache_file_paths(urls, *, cache_dir=None, file_extension=None, hash_func=None, lazy=False, show_progress=False)

# Context managers for temporary downloads
class TemporarilyDownloadUrl:
    def __init__(self, url: str, path=None)               # Downloads file, deletes on context exit

class TemporarilyDownloadUrlorPath:
    def __init__(self, url_or_path: str)                  # Handles both URLs and local paths
```

### Cloud Storage Integration

#### AWS S3
```python
def is_s3_url(url)                                        # Check if URL is S3 format
def s3_list_objects(s3url, *, recursive=True, include_metadata=False, lazy=False, show_progress=False)
```

#### Google Cloud Storage  
```python
def is_gs_url(url)                                        # Check if URL is GCS format
def running_in_gcp()                                      # Detect GCP environment
def get_cloud_provider()                                  # Detect cloud environment
```

## YouTube Integration

### YouTube Video System
Complete YouTube video handling pipeline:

```python
# URL/ID handling
def get_youtube_video_url(url_or_id)                     # Normalize to full YouTube URL
def _is_youtube_video_url(url)                           # Private: validate YouTube URL

# Metadata extraction
def get_youtube_video_title(url_or_id)                   # Extract video title
def get_youtube_video_thumbnail(url_or_id, *, use_cache=False, output='image')  # Get thumbnail as image
def get_youtube_video_transcript(url_or_id: str)         # Extract captions/subtitles

# Video download (highly configurable)
def download_youtube_video(url_or_id: str,
                          path=None,
                          *,
                          need_video=True,
                          need_audio=True, 
                          max_resolution=None,
                          min_resolution=None,
                          resolution_preference=max,
                          skip_existing=False,
                          show_progress=True,
                          overwrite=False,
                          filetype='mp4')
```

**YouTube Download Workflow:**
1. `get_youtube_video_url()` → normalize URL/ID
2. `download_youtube_video()` → pytubefix backend for download
3. Supports separate video/audio tracks for high quality
4. Integrates with RP's video processing pipeline

## GitHub Integration

### Gist System
```python
def load_gist(gist_url: str)                             # Load gist content as string
def shorten_github_url(url, title=None)                  # Shorten GitHub URLs

# GitHub API integration  
def get_number_of_github_gists(username="SqrtRyan")      # Count user's gists
def _get_all_github_gists_info(username="SqrtRyan", use_cache=True)  # Get gist metadata
def _download_rp_gists(max_filesize='10mb')              # Download RP-specific gists
```

### Git Operations
```python
def get_git_remote_url(repo='.')                         # Get remote URL for repo
def _distill_github_url(url)                             # Extract GitHub repo info
def _get_repo_name_from_url(url)                         # Extract repo name from URL
def git_clone(url, path=None, *, depth=None, branch=None, single_branch=False, show_progress=False)
```

## Font Download System

### Google Fonts API Integration
```python
def download_google_font(font_name, *, skip_existing=True)         # Download specific Google font
def download_font(url, *, skip_existing=True)                     # Download font from URL
def download_fonts(font_names_or_urls, *, skip_existing=True, show_progress=True, max_workers=4)
def download_google_fonts(font_names, *, skip_existing=True, show_progress=True, max_workers=4)
def download_all_google_fonts(*, show_progress=True)              # Download entire Google Fonts collection
def get_downloaded_fonts()                                         # List cached fonts

# Internal font system helpers
def _get_file_path(path_or_url)                                   # Handle URL vs path
def get_urls(content)                                             # Extract URLs from content
def fetch_data(urls)                                              # Batch fetch font data
```

## Web Clipboard System

### RP's Custom Web Clipboard
```python
def web_copy(data: object, *, show_progress=False) -> None        # Upload to RP's web clipboard
def web_paste()                                                   # Download from RP's web clipboard  
def _web_copy(data: object, *, show_progress=False) -> None       # Internal implementation

# File-based web clipboard
def web_copy_path(path: str = None, *, show_progress=False)       # Upload file to web clipboard
def web_paste_path(path=None, *, ask_to_replace=True)             # Download file from web clipboard

# Progress tracking for uploads
class _WebCopyProgressTracker:                                    # Internal progress tracking class
```

## Image/Media Loading from Web
**Connection to Image System:**
```python
def load_image_from_url(url: str)                                 # Load image directly from URL
def display_website_in_terminal(url)                              # Render website in terminal
def _load_text_from_file_or_url(location)                        # Handle both files and URLs
```

## API Integration

### OpenAI/LLM APIs
```python
def _get_openai_api_key(key=None)                                # Get OpenAI API key from environment
def _run_openai_llm(message, model, api_key=None)                # Execute OpenAI API call
def run_llm_api(message, model='gpt-4o-mini', api_key=None)      # Public LLM API interface
```

### Generic API Patterns
```python
# Example pattern found in codebase:
def load_data_from_api(api_url, api_key, timeout)               # Generic API data loading pattern
```

## Social Media Integration

### Facebook (Legacy - Currently Broken)
```python
def _get_facebook_client(email, password)                       # Facebook client creation (broken)
def send_facebook_message(message: str = None, my_email: str = None, my_password: str = None)  # Send FB message (broken)
def get_all_facebook_messages(my_email: str = None, my_password: str = None, my_name: str = None, max_number_of_messages: int = 9999) -> list  # Get FB messages (broken)
```

**Note:** Facebook functions are currently broken due to deprecated fbchat library and Facebook API changes.

## Email System (In Graveyard)

### Gmail Integration (Moved to Graveyard)
The email system has been moved to `/opt/homebrew/lib/python3.10/site-packages/rp/libs/graveyard.py` but remains accessible:

```python
# Email sending (from graveyard)
def send_gmail_email(recipients, subject="", body="", gmail_address=default_gmail_address, password=default_gmail_password, attachments=None, shutup=False)

# Email monitoring (from graveyard) 
def gmail_inbox_summary(gmail_address=default_gmail_address, password=default_gmail_password, max_emails=default_max_emails, just_unread_emails=True)
def continuously_scan_gmail_inbox(what_to_do_with_unread_emails=_default_what_to_do_with_unread_emails, gmail_address=default_gmail_address, password=default_gmail_password, max_emails=default_max_emails, include_old_but_unread_emails=False)
def _continuously_scan_gmail_inbox(what_to_do_with_unread_emails, gmail_address, password, max_emails, include_old_but_unread_emails)
def _default_what_to_do_with_unread_emails(x)                    # Default email handler (print + TTS)
```

## Socket Communication (In Graveyard)

### UDP Socket System (Moved to Graveyard)
Low-level socket communication moved to graveyard but still accessible:

```python
# Socket writers (from graveyard)
def socket_writer(targetIP: str, port: int = None)              # Create UDP socket writer
def socket_write(targetIP, port, message)                       # Send UDP message

# Socket readers (from graveyard)  
def socket_reader(port: int = None)                             # Create UDP socket reader (blocks)
def socket_read(port, just_data_if_true_else_tuple_with_data_then_ip_addr: bool = True)  # Read UDP message
def socket_reading_thread(handler, port: int = None, just_data_if_true_else_tuple_with_data_then_ip_addr: bool = True)  # Threaded UDP reader
```

## Web Evaluation System

### Distributed Computing via HTTP
RP includes a sophisticated web evaluation system (`web_evaluator.py`) for distributed Python execution:

```python
# Server-side
def run_server(server_port: int = None, ...)                    # Run evaluation server
def run_delegation_server(server_port=None, ...)                # Run load-balancing server

# Client-side  
class Client:
    def __init__(self, server_name: str = "localhost", server_port: int = None, *, sync=None, timeout=None)
    def evaluate(*, code, vars, server_url, sync, timeout)       # Execute code on remote server
    def register(self, server_port=DEFAULT_SERVER_PORT, server_name=None, *, sync=True, silent=False)

# Multi-client management
class ClientDelegator:
    def __init__(self, clients=[], *, on_connection_error='unregister', max_jobs_per_client=1)
    def register_client(self, client, *, unique=True, after_ping=False, silent=False)
    def unregister_client(self, client)  
    def evaluate(self, code, options=None, **vars)               # Load-balance across clients

# Evaluation results
class Evaluation:
    # Represents result of remote code execution
    # Attributes: code, value, error, errored, is_eval, is_exec, sync
```

## Connection Patterns & Workflows

### 1. Download → Process → Save Chain
```python
# Common pattern: download → process → save
url = "https://example.com/image.jpg"
path = download_url(url)                    # Download to local file
image = load_image(path)                    # Load into RP image system  
processed = resize_image(image, (512, 512)) # Process with RP functions
save_image(processed, "output.jpg")         # Save result
```

### 2. YouTube → Video Processing Pipeline
```python
# YouTube integration with video system
url = "https://www.youtube.com/watch?v=VIDEO_ID"
video_path = download_youtube_video(url, need_video=True, need_audio=False)  # High-res video only
audio_path = download_youtube_video(url, need_video=False, need_audio=True)  # Audio only
final_video = add_audio_to_video_file(video_path, audio_path)               # RP video function
```

### 3. Web Clipboard Workflow
```python
# Cross-machine data transfer
data = {"results": analysis_results, "metadata": meta}
web_copy(data)                              # Upload to RP's web clipboard

# On another machine:
received_data = web_paste()                 # Download from web clipboard
process_results(received_data["results"])   # Continue processing
```

### 4. Font Management Pipeline
```python
# Font download → text rendering pipeline  
download_google_font("Roboto")              # Download font
fonts = get_downloaded_fonts()              # List available fonts
text_image = text_to_image("Hello", font="Roboto")  # Use with RP text rendering
```

### 5. API Integration Patterns
```python
# API → Processing → Storage
response = run_llm_api("Analyze this data: " + str(data))      # LLM API call
processed = parse_llm_response(response)                       # Custom processing
save_json(processed, "analysis_results.json")                 # Save with RP I/O
```

### 6. Distributed Computing Workflow
```python
# Setup distributed evaluation
server = run_server(port=43234)                               # Start evaluation server on machine A

# On machine B:
client = Client("machine_a_ip", 43234)                        # Connect to server
result = client.evaluate("expensive_computation(data)")        # Execute on server
local_processing(result.value)                                # Process results locally
```

### 7. GitHub Integration Pipeline
```python
# GitHub → Processing → Sharing
gist_content = load_gist("https://gist.github.com/user/hash") # Load gist content
processed_code = process_code(gist_content)                   # Process with RP functions
shortened_url = shorten_github_url(repo_url)                  # Share via shortened URL
```

## Network Utility Functions

### Connection Testing
```python
def connected_to_internet()                                   # Test internet connectivity (used internally)
```

### Internal Network Helpers
```python
def _ensure_curl_installed()                                  # Ensure curl is available
def get_computer_name()                                       # Get computer hostname (via socket)
```

## Protocol Support Summary

| Protocol | Functions | Backend | Use Cases |
|----------|-----------|---------|-----------|
| HTTP/HTTPS | `curl()`, `curl_bytes()`, `download_url()` | requests | Web scraping, API calls, file download |
| AWS S3 | `download_url()`, `s3_list_objects()` | aws cli | Cloud storage access |  
| Google Cloud | `download_url()` (gs://), cloud detection | gsutil | GCP storage integration |
| Google Colossus | `download_url()` (/cns/) | fileutil | Internal Google systems |
| YouTube | `download_youtube_video()`, metadata functions | pytubefix | Video content acquisition |
| UDP Sockets | Socket functions (graveyard) | Python socket | Low-level networking |
| SMTP/IMAP | Email functions (graveyard) | smtplib/imaplib | Email automation |

## Integration Points

### With RP Image System
- `load_image_from_url()` → Direct URL to image loading
- `get_youtube_video_thumbnail()` → YouTube thumbnails as images
- Font downloads → Text rendering pipeline

### With RP Video System  
- `download_youtube_video()` → Video processing pipeline
- Web downloads → Video file handling

### With RP File I/O System
- All download functions → File path handling
- Cache management → Temporary file system
- Web clipboard → Object serialization

### With RP REPL System
- Web evaluation → Remote code execution  
- Progress display → REPL progress bars
- Error handling → REPL error display

## Security & Best Practices

### Authentication Patterns
- API keys via environment variables (`_get_openai_api_key()`)
- Credential management in graveyard email functions
- No hardcoded credentials in main codebase

### Error Handling
- Timeout support across HTTP functions
- Graceful fallbacks for network failures  
- Progress tracking for long operations
- Connection validation before operations

### Performance Optimizations
- Connection pooling in web evaluation system
- Concurrent downloads via `max_workers` parameters
- Caching systems for repeated downloads
- Streaming for large file downloads

This comprehensive mapping shows RP's network/web functions form a complete ecosystem for internet-connected Python programming, from simple HTTP requests to distributed computing systems.