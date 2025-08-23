# RP Library: Network Web

Network and web integration: URL handling, HTTP requests, API interactions, and web scraping.

**Total Functions: 54**

## Function Inventory

| Function | Line | Description |
|----------|------|-------------|
| `is_valid_url()` | 5470 |  Return true iff the url string is syntactically valid  Enhanced Documentation:  Validates whether a... |
| `_disable_insecure_request_warning()` | 6199 | Url should either be like http://website.com/image.png or like data:image/png;base64,iVBORw0KGgoAAAA... |
| `load_image_from_url()` | 6208 | Url should either be like http://website.com/image.png or like data:image/png;base64,iVBORw0KGgoAAAA... |
| `save_image_webp()` | 6908 | Save image in WebP format. Set lossless=True for lossless compression, False for lossy. If add_exten... |
| `save_animated_webp()` | 7082 | Save an animated video in WebP format. If add_extension is True, adds '.webp' extension if not alrea... |
| `display_video_in_notebook_webp()` | 8504 | Displays an animated webp in a Jupyter notebook with a specified quality and framerate See rp.displa... |
| `_display_downloadable_image_in_notebook_via_ipython()` | 8550 |  Display an image at full resolution in a jupyter notebook. Returns an updatable channel.   channel ... |
| `display_website_in_terminal()` | 8961 | Enhanced Documentation:  Fetches and displays a website's content as formatted text in the terminal.... |
| `load_data_from_api()` | 10568 | *(No description)* |
| `_get_carbon_url()` | 11503 | Generate a Carbon URL to visualize code snippets with syntax highlighting.  code : str The code to d... |
| `load_image_from_webcam()` | 13232 | If your camera supports multiple resolutions, input the dimensions in the height and width parameter... |
| `load_webcam_stream()` | 13289 | Grabs a screenshot from the main monitor using the Multiple Screen Shots (MSS) Library Returns it as... |
| `_load_image_from_webcam_in_jupyter_notebook()` | 13359 | VIDEO_HTML =  <video autoplay width=800 height=600></video> <script> var video = document.querySelec... |
| `shorten_url()` | 16716 | *(No description)* |
| `unshorten_url()` | 16786 | Takes a shortened URL and returns the long one EXAMPLE: unshorten_url('bit.ly/labinacube')  -->  'ht... |
| `shorten_github_url()` | 16827 | Doesn't work anymore! git.io was discontinued for some god forsaken reason :( Use rp.shorten_url ins... |
| `open_url_in_web_browser()` | 18198 | Returns the URL for google-searching the given query  EXAMPLE: >>> google_search_url('What is a dog?... |
| `google_search_url()` | 18202 | Returns the URL for google-searching the given query  EXAMPLE: >>> google_search_url('What is a dog?... |
| `open_google_search_in_web_browser()` | 18215 | Opens up the web browser to a google search of a given query |
| `_load_text_from_file_or_url()` | 20867 | *(No description)* |
| `_download_rp_gists()` | 21838 | Change directory in pseudo_terminal with history tracking. Internal helper. dir=os.path.expanduser(d... |
| `download_google_font()` | 32324 | Original code from: https://gist.github.com/ravgeetdhillon/0063aaee240c0cddb12738c232bd8a49  downloa... |
| `get_urls()` | 32456 | Parses the css file and retrieves the font urls. Parameters: content (string): The data which needs ... |
| `download_font()` | 32565 | https://github.com/ctrlcctrlv/lcd-font/raw/master/otf/LCD14.otf |
| `download_fonts()` | 32581 | See download_google_font's docstring. This is it's plural form. font_names = detuple(font_names) ret... |
| `download_google_fonts()` | 32597 | See download_google_font's docstring. This is it's plural form. font_names = detuple(font_names) ret... |
| `get_downloaded_fonts()` | 32613 |  Returns a list of font files downloaded by rp  def get(x): try: return _get_all_paths_fast( x, recu... |
| `download_all_google_fonts()` | 32740 | Download all Google fonts I know of: 120.1MB Returns a list of paths to all downloaded fonts |
| `get_youtube_video_url()` | 36888 | Gets the url of a youtube video, given either the url (in which case nothing changes) or its id  Exa... |
| `_is_youtube_video_url()` | 36905 | Returns the captions/subtitles for a YouTube video based on the given URL or video ID.  NOTE: If it ... |
| `download_youtube_video()` | 36954 | Downloads a YouTube video based on the given URL or video ID. The function can selectively download ... |
| `_ensure_punkt_downloaded()` | 40941 | Gets a list of languages supported by nltk's punkt (sentence splitter) Current languages as of writi... |
| `is_s3_url()` | 41977 | Download files from URLs with multi-protocol support and automatic path handling.  Supports HTTP/HTT... |
| `is_gs_url()` | 41981 | Download files from URLs with multi-protocol support and automatic path handling.  Supports HTTP/HTT... |
| `download_url()` | 41985 | Download files from URLs with multi-protocol support and automatic path handling.  Supports HTTP/HTT... |
| `download_urls()` | 42164 | Plural of download_url Tune the num_threads and buffer_limit for optimal downloads to avoid too many... |
| `download_url_to_cache()` | 42255 | Like download_url, except you only specify the output diectory - the filename will be chosen for you... |
| `download_urls_to_cache()` | 42303 |  Plural of rp.download_url_to_cache  urls = detuple(urls)  if show_progress in ['eta', True]: show_p... |
| `download()` | 42321 | *(No description)* |
| `_datamuse_words_request()` | 42578 |  Uses https://www.datamuse.com/api/  pip_import('requests') import requests,json response=requests.g... |
| `_ensure_curl_installed()` | 43984 | *(No description)* |
| `_web_copy()` | 44754 |  Make the request for web-copying. Can also upload arbitrary HTML pages.  assert connected_to_intern... |
| `web_copy()` | 44776 |  Send an object to RyanPython's server's clipboard  assert connected_to_internet(),"Can't connect to... |
| `web_paste()` | 44783 |  Get an object from RyanPython's server's clipboard  assert connected_to_internet(),"Can't connect t... |
| `curl()` | 47670 | Meant to imitate the 'curl' command in linux Sends a get request to the given URL and returns the re... |
| `curl_bytes()` | 47680 | Fetches a file from a specified URL and returns its bytes  Parameters: url (str): The URL of the fil... |
| `_get_openai_api_key()` | 50990 | *(No description)* |
| `run_llm_api()` | 51024 | Takes an image, finds text on it, and returns the text as a string (Optical character recognition) I... |
| `web_paste_path()` | 51825 |  FP (file paste)  data = web_paste() return gather_args_call(_paste_path_from_bundle, data,path=path... |
| `request_replace()` | 51836 | *(No description)* |
| `web_copy_path()` | 51873 |  FC (file copy)  if is_a_module(path): path = get_module_path(path) web_copy(_copy_path_to_bundle(pa... |
| `get_git_remote_url()` | 54141 | *(No description)* |
| `_distill_github_url()` | 54225 | Distills a GitHub URL to its base repository URL.  https://github.com/fperazzi/davis-2017/tree/main ... |
| `_get_repo_name_from_url()` | 54240 | Url should look like: https://github.com/gabrielloye/RNN-walkthrough/ https://github.com/gabrielloye... |

## Architectural Analysis


## Function Relationships

### Batch Operations
- `download_font()` ↔ `download_fonts()`
- `download_google_font()` ↔ `download_google_fonts()`
- `download_url()` ↔ `download_urls()`

