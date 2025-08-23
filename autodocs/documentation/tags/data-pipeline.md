# RP Library: Data Pipeline

Functions that handle data flow: loading, saving, encoding, decoding, and format conversion operations.

**Total Functions: 147**

## Function Inventory

| Function | Line | Description |
|----------|------|-------------|
| `_transform_fansi_arg()` | 1560 |  Allow for 'yellow green underlined on blue bold'  style_keywords = style_keywords or _fansi_styles ... |
| `load_files()` | 5529 | Load a list of files with optional multithreading.  - load_file (function): A function to load a sin... |
| `_load_files()` | 5574 | *(No description)* |
| `_load_file()` | 5635 | *(No description)* |
| `load_animated_gif()` | 5685 | Location should be a url or a file path pointing to a GIF file Loads an array of frames of an RGB an... |
| `load_image_from_clipboard()` | 5790 |  #Grab an image copied from your clipboard  #TODO: Use the "copykitten" library to paste images pip_... |
| `load_image()` | 5894 |  Automatically detect if location is a URL or a file path and try to smartly choose the appropriate ... |
| `load_rgb_image()` | 5960 | Like load_image, but makes sure there's no alpha channel This function is really only here to save y... |
| `load_images()` | 5978 | Simply the plural form of load_image This is much faster than using load_image sequentially because ... |
| `_load_image()` | 6017 | *(No description)* |
| `_load_images_via_pdf2image()` | 6069 |  Given a PDF, returns a list of images - one for each page  return _load_images_via_pdf2image(path) ... |
| `load_pdf_as_images()` | 6088 |  Given a PDF, returns a list of images - one for each page  return _load_images_via_pdf2image(path) ... |
| `load_pdf_as_text()` | 6099 |  Given a PDF, returns the text content as a string  return _load_pdf_as_text_via_pdfminer(path)  def... |
| `_load_pdf_as_text_via_pdfminer()` | 6103 |  Extract text from PDF using pdfminer.six  pip_import('pdfminer') from pdfminer.high_level import ex... |
| `load_image_from_file()` | 6130 |  Can try opencv as a fallback if this ever breaks  assert file_exists(file_name),'No such image file... |
| `_load_image_from_file_via_PIL()` | 6165 | NOTE if this method fails try the following function: imageio.plugins.freeimage.download() #https://... |
| `_load_image_from_file_via_imageio()` | 6175 | NOTE if this method fails try the following function: imageio.plugins.freeimage.download() #https://... |
| `_load_image_from_file_via_scipy()` | 6185 | *(No description)* |
| `_load_image_from_file_via_opencv()` | 6189 | Url should either be like http://website.com/image.png or like data:image/png;base64,iVBORw0KGgoAAAA... |
| `load_image_from_url()` | 6208 | Url should either be like http://website.com/image.png or like data:image/png;base64,iVBORw0KGgoAAAA... |
| `load_image_from_matplotlib()` | 6227 | Return matplotlib's current display as an image You can increase the DPI to get a higher resolution.... |
| `load_openexr_image()` | 6326 | Will load a floating point openexr image as a numpy array The 'channels' argument is used to specify... |
| `_encode_image_to_bytes()` | 6389 | *(No description)* |
| `encode_image_to_bytes()` | 6426 | Encodes an image into a bytestring, without actually saving it to your harddrive The bytes are the s... |
| `encode_images_to_bytes()` | 6485 | Batch encode multiple images to bytes. See encode_image_to_bytes for single images. |
| `decode_images_from_bytes()` | 6491 | Decode multiple images from byte-encoded format.  Converts a collection of byte-encoded images back ... |
| `encode_image_to_base64()` | 6537 | Encodes an image into a base64 string. Useful for HTTP requests, or displaying HTML images in jupyte... |
| `encode_images_to_base64()` | 6556 | Batch encode multiple images to base64 strings. See encode_image_to_base64 for single images. |
| `decode_image_from_base64()` | 6561 | Decode a base64 string back to an image. Convenience function combining base64_to_bytes and decode_b... |
| `decode_images_from_base64()` | 6567 | Decode multiple base64 strings back to images. Convenience function for batch decoding base64 encode... |
| `decode_bytes_to_image()` | 6573 | Supports any filetype in r._opencv_supported_image_formats, including jpg, bmp, png, exr and tiff TO... |
| `save_image()` | 6603 | Todo: Add support for imageio, which can also write images Simply save a numpy image to a file. The ... |
| `save_images()` | 6711 | Save images to specified paths concurrently.  Parameters: - images (list): List of image objects to ... |
| `_save_image()` | 6765 | *(No description)* |
| `temp_saved_image()` | 6805 | Return the path of an image, and return the path we saved it to Originally used for google colab to ... |
| `save_image_to_imgur()` | 6816 | Takes an image, or an image path Returns the url of the saved image Note: This function can sometime... |
| `save_image_jpg()` | 6842 | If add_extension is True, will add a '.jpg' or '.jpeg' extension to path IFF it doesn't allready end... |
| `save_image_webp()` | 6908 | Save image in WebP format. Set lossless=True for lossless compression, False for lossy. If add_exten... |
| `save_image_avif()` | 6935 | Save image in AVIF format. Set lossless=True for lossless compression, False for lossy. If add_exten... |
| `save_image_jxl()` | 6962 | Save image in JPEG XL format. Set quality=100 for lossless compression. If add_extension is True, ad... |
| `save_animated_webp()` | 7082 | Save an animated video in WebP format. If add_extension is True, adds '.webp' extension if not alrea... |
| `save_openexr_image()` | 7113 | Counterpart to load_openexr_image TODO: Add support for custom channels This code is based on https:... |
| `convert_image_file()` | 7173 | Converts an image file to a specified format and saves it to the provided output folder. It can also... |
| `convert_image_files()` | 7249 | Converts multiple image files to a specified format and saves them to the provided output folder. Th... |
| `_convert_image()` | 7327 | *(No description)* |
| `save()` | 7699 |  Do the Web request and save to `savefile`  with open(savefile,'wb') as f: self.write_to_fp(f) f.clo... |
| `load_mp3_file()` | 7888 | Takes an mp3 file path, and returns a bunch of samples as a numpy array Returns floating-point sampl... |
| `load_wav_file()` | 7912 | Takes a wav file path, and returns a bunch of samples as a numpy array Returns floating-point sample... |
| `load_sound_file()` | 7937 | Returns the contents of a sound file at file_path as a numpy array of floats in the range [-1, 1] sa... |
| `save_wav()` | 8003 | For stereo, use a np matrix Example: psfs((x%100)/100 for x in range(100000)) Each sample should ∈ [... |
| `convert_audio_file()` | 8166 | Convert an audio file to a different format using FFmpeg.  Args: input_file (str): Path to the input... |
| `save_video()` | 8519 | #      #     This will embed a video into the jupyter notebook you're using #     Warning: This func... |
| `_display_downloadable_image_in_notebook_via_ipython()` | 8550 |  Display an image at full resolution in a jupyter notebook. Returns an updatable channel.   channel ... |
| `_convert_content()` | 8668 | *(No description)* |
| `_convert_content_grid()` | 8686 | *(No description)* |
| `convert_grid_item()` | 8698 | Adds a new viewport from IPython.display import display, HTML display(self._converted_content, displ... |
| `load_data_from_api()` | 10568 | *(No description)* |
| `load_image_from_webcam()` | 13232 | If your camera supports multiple resolutions, input the dimensions in the height and width parameter... |
| `load_webcam_stream()` | 13289 | Grabs a screenshot from the main monitor using the Multiple Screen Shots (MSS) Library Returns it as... |
| `load_image_from_screenshot_via_mss()` | 13293 | Grabs a screenshot from the main monitor using the Multiple Screen Shots (MSS) Library Returns it as... |
| `load_image_from_screenshot()` | 13319 | Grabs a screenshot from the main monitor Returns it as a RGB byte image  EXAMPLE:  >>> while True: .... |
| `load_screenshot_stream()` | 13334 |  EXAMPLE:  >>> while True: ...     display_video(cv_resize_images(load_screenshot_stream(), size=.25... |
| `_load_image_from_screenshot_via_pyscreenshot()` | 13346 | REPLACED BY load_image_from_screenshot WHICH IS MUCH FASTER (This still works as a slow version thou... |
| `_load_image_from_webcam_in_jupyter_notebook()` | 13359 | VIDEO_HTML =  <video autoplay width=800 height=600></video> <script> var video = document.querySelec... |
| `load_pickled_value()` | 13548 | Load a Python object from a pickle file.  Enhanced Documentation: Deserializes Python objects that w... |
| `save_pickled_value()` | 13612 | Save variables to pickle file. Uses detuple for flexible argument handling.  Enhanced Documentation:... |
| `save_text_file()` | 13710 | text_file_to_string(file_path) reads text file  Enhanced Documentation: This is RP's primary text fi... |
| `load_file_lines()` | 13800 |  Returns all the lines in a file  return line_split(text_file_to_string(file_path, use_cache))  def ... |
| `save_file_lines()` | 13804 | Save an iterable of lines to a text file.  Convenient function for saving lists/collections of text ... |
| `load_text_files()` | 13843 | Plural of text_file_to_string Please see load_files and rp_iglob for more information Yields the str... |
| `load_json()` | 13954 | Load JSON file and convert to EasyDict for convenient attribute access.  Enhanced Documentation: Loa... |
| `load_jsons()` | 14043 | Plural of load_json Please see load_files and rp_iglob for more information Yields the jsons as an i... |
| `save_json()` | 14055 | Save Python data structures as JSON files with formatting options.  Enhanced Documentation: Serializ... |
| `load_tsv()` | 14124 | Read a TSV file with optional progress tracking and flexible header handling.  By default tries to b... |
| `load_parquet()` | 14248 | Read a Parquet file with optional progress tracking.  Parameters: file_path (str): Path to the Parqu... |
| `load_yaml_file()` | 14314 | EXAMPLE: >>> load_yaml_file('alphablock_without_ssim_256.yaml') ans = {'max_iter': 300000, 'batch_si... |
| `load_yaml_files()` | 14331 | Plural of load_yaml_file Please see load_files and rp_iglob for more information Yields the jsons as... |
| `load_dyaml_file()` | 14554 |  Load a dyaml file (a yaml file with some additional syntax features I added). Stands for "Delta Yam... |
| `encode_float_matrix_to_rgba_byte_image()` | 16615 | Can encode a 32-bit float into the 4 channels of an RGBA image The values should be between 0 and 1 ... |
| `decode_float_matrix_from_rgba_byte_image()` | 16635 | This function is the inverse of encode_float_matrix_to_rgba_image Takes an rgba byte-image (that was... |
| `load_gist()` | 16800 | Takes the URL of a gist, or the shortened url of a gist (by something like bit.ly), and returns the ... |
| `save_gist()` | 16940 | This function takes an input string, posts it as a gist on Github, then returns the URL of the new g... |
| `reload_module()` | 18228 | If rp changes mid-notebook, here's a convenient way to reload it |
| `reload_rp()` | 18232 | If rp changes mid-notebook, here's a convenient way to reload it |
| `_load_pyin_settings_file()` | 19664 | *(No description)* |
| `_load_pyin_settings_from_dict()` | 19674 | *(No description)* |
| `_save_pyin_settings_file()` | 19688 | *(No description)* |
| `_reload_modules()` | 20004 | Reload modified modules for development. Internal helper for pseudo_terminal. #Re-import any modules... |
| `_load_text_from_file_or_url()` | 20867 | *(No description)* |
| `load_page()` | 21811 | *(No description)* |
| `_download_rp_gists()` | 21838 | Change directory in pseudo_terminal with history tracking. Internal helper. dir=os.path.expanduser(d... |
| `_convert_powerpoint_file()` | 21949 | *(No description)* |
| `save_animated_png()` | 26416 | Save a sequence of images as an animated PNG (APNG) file.  Enhanced Documentation: Creates animated ... |
| `cv_distance_transform()` | 28889 | Compute distance transform using OpenCV.  Args: mask: 2D boolean array distance_to: What are we retu... |
| `_omni_load_animated_image()` | 30351 |  gif and webp and png can be either a video or image depending on context...  video = load_video(pat... |
| `_omni_save_animated_image()` | 30358 |  gif and webp and png can be either a video or image depending on context...  if is_image(video): re... |
| `_omni_save_default_extension()` | 30366 | Internal smart file loading dispatcher based on file extension and type detection.  Enhanced Documen... |
| `_omni_load()` | 30378 | Internal smart file loading dispatcher based on file extension and type detection.  Enhanced Documen... |
| `_omni_save()` | 30436 | *(No description)* |
| `download_google_font()` | 32324 | Original code from: https://gist.github.com/ravgeetdhillon/0063aaee240c0cddb12738c232bd8a49  downloa... |
| `download_font()` | 32565 | https://github.com/ctrlcctrlv/lcd-font/raw/master/otf/LCD14.otf |
| `download_fonts()` | 32581 | See download_google_font's docstring. This is it's plural form. font_names = detuple(font_names) ret... |
| `download_google_fonts()` | 32597 | See download_google_font's docstring. This is it's plural form. font_names = detuple(font_names) ret... |
| `get_downloaded_fonts()` | 32613 |  Returns a list of font files downloaded by rp  def get(x): try: return _get_all_paths_fast( x, recu... |
| `download_all_google_fonts()` | 32740 | Download all Google fonts I know of: 120.1MB Returns a list of paths to all downloaded fonts |
| `r_transform()` | 34041 | Stands for Ryan-Transform. Used for path matching in my 2019 Zebra summer internship. Removes transl... |
| `r_transform_inverse()` | 34052 | Note that we lose scale, rotation and translational information r_transform(r_transform_inverse(r_tr... |
| `_common_image_channel_converter()` | 35145 | Given a list of images, choose the cheapest as_*_image function that preserves as much data as possi... |
| `_common_image_dtype_converter()` | 35151 | Given a list of images, choose the cheapest as_*_image function that preserves as much data as possi... |
| `_common_image_converter()` | 35157 | *(No description)* |
| `converter()` | 35160 | *(No description)* |
| `download_youtube_video()` | 36954 | Downloads a YouTube video based on the given URL or video ID. The function can selectively download ... |
| `_load_video_stream()` | 37248 | *(No description)* |
| `load_video_stream()` | 37268 | Much faster than load_video, which loads all the frames into a numpy array. This means load_video ha... |
| `load_video_streams()` | 37308 |  Plural of load_video_stream. If transpose==True, returns a single iterator that returns tuples of f... |
| `load()` | 37331 | This function does not take into account framerates or audio. It just returns a numpy array full of ... |
| `load_video()` | 37350 | This function does not take into account framerates or audio. It just returns a numpy array full of ... |
| `load_videos()` | 37429 | Plural of load_video Loads many videos.  Args: See load_video for documentation on the paths, start_... |
| `load()` | 37456 | Saves the frames of the video to an .avi file |
| `save_video_avi()` | 37468 | Saves the frames of the video to an .avi file |
| `_cv_save_video_mp4()` | 37627 | *(No description)* |
| `_cv_save_video_mp4()` | 37661 | Uses quality instead of bitrate because of how opencv works: https://docs.opencv.org/3.4/d4/d15/grou... |
| `set_save_video_mp4_default_backend()` | 37713 | frames: a list of images as defined by rp.is_image(). Saves an .mp4 file at the path - frames can al... |
| `save_video_mp4()` | 37718 | frames: a list of images as defined by rp.is_image(). Saves an .mp4 file at the path - frames can al... |
| `load_frame()` | 37785 | *(No description)* |
| `save_video_gif_via_pil()` | 37809 | Save a video to a GIF with given path and framerate. Returns the path of the new GIF.  TODO: Support... |
| `convert_to_gif_via_ffmpeg()` | 37875 | Converts a video file to a GIF using FFmpeg. It does a really good job - with dithering! If you set ... |
| `convert_to_gifs_via_ffmpeg()` | 37969 |  Plural of convert_to_gif_via_ffmpeg. Arguments are broadcastable.  def run(bundle): return convert_... |
| `save_video()` | 38010 | #TODO: add options for sound and framerate. Possibly quality options but probably not (that should b... |
| `encode_video_to_bytes()` | 38050 | Encode video to bytes without saving to disk. |
| `decode_video_from_bytes()` | 38064 | Decode bytes back to video array. |
| `_ensure_punkt_downloaded()` | 40941 | Gets a list of languages supported by nltk's punkt (sentence splitter) Current languages as of writi... |
| `unicode_loading_bar()` | 41270 | EXAMPLE 1: for _ in range(200):print(end='\r'+unicode_loading_bar(_));sleep(.05) EXAMPLE 2: for _ in... |
| `download_url()` | 41985 | Download files from URLs with multi-protocol support and automatic path handling.  Supports HTTP/HTT... |
| `download_urls()` | 42164 | Plural of download_url Tune the num_threads and buffer_limit for optimal downloads to avoid too many... |
| `download_url_to_cache()` | 42255 | Like download_url, except you only specify the output diectory - the filename will be chosen for you... |
| `download_urls_to_cache()` | 42303 |  Plural of rp.download_url_to_cache  urls = detuple(urls)  if show_progress in ['eta', True]: show_p... |
| `download()` | 42321 | *(No description)* |
| `_ensure_claudecode_installed()` | 44013 | *(No description)* |
| `_load_ryan_lazygit_config()` | 44201 | config_lines=unindent( # < RP Lazygit Config Start > #DEFAULTS: https://github.com/jesseduffield/laz... |
| `can_convert_object_to_bytes()` | 44634 | Returns true if we can run object_to_bytes on x without getting an error See object_to_bytes for mor... |
| `encode_bytes_to_image()` | 44673 | Encode binary data into a numpy array representing an RGB image.  The function packs the data length... |
| `decode_image_to_bytes()` | 44706 | Decode a numpy array image back to the original binary data.  Extracts the data length from the firs... |
| `load_text()` | 52321 | *(No description)* |
| `load_annotated_lines()` | 52327 | *(No description)* |
| `load_safetensors()` | 54861 | Loads tensors from a .safetensors file.  Args: path (str): Path to .safetensors file, or a glob for ... |
| `save_safetensors()` | 54956 | Saves tensors to a .safetensors file.  Args: tensors (dict or easydict): Dictionary of tensors to sa... |

## Architectural Analysis

### Data Pipeline Architecture

RP's data pipeline enables seamless data flow:

1. **Universal Loaders**: Load from files, URLs, bytes, base64, clipboard
2. **Format Converters**: Automatic format detection and conversion
3. **Encoding System**: Multiple encoding formats (base64, bytes, etc.)
4. **Batch Processing**: Parallel loading/saving of multiple items
5. **Caching Layer**: Optional caching for performance optimization

### Key Patterns
- **Source Agnostic**: Functions accept multiple input sources
- **Format Detection**: Automatic format identification from content/extension  
- **Error Handling**: Graceful handling of corrupted or invalid data
- **Performance Optimization**: Parallel processing and caching where beneficial

## Function Relationships

### Batch Operations
- `_load_file()` ↔ `_load_files()`
- `load_image()` ↔ `load_images()`
- `save_image()` ↔ `save_images()`
- `convert_image_file()` ↔ `convert_image_files()`
- `load_json()` ↔ `load_jsons()`
- ... and 6 more

### Multiplexing
- `load_image_from_screenshot()` ↔ `load_image_from_screenshot_via_mss()`

