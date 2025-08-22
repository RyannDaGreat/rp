# RP Library: Media Processing

Comprehensive media processing pipeline: image manipulation, video processing, audio handling, and computer vision.

**Total Functions: 331**

## Function Inventory

| Function | Line | Description |
|----------|------|-------------|
| `get_max_image_dimensions()` | 2841 |  Given a set of images, return the maximum height and width seen across all of them  Enhanced Docume... |
| `get_max_video_dimensions()` | 2876 |  Given a set of videos, return the maximum height and width seen across all of them  images = detupl... |
| `get_min_video_dimensions()` | 2886 |  Given a set of videos, return the minimum height and width seen across all of them  images = detupl... |
| `get_min_image_dimensions()` | 2896 |  Given a set of images, return the minimum height and width seen across all of them  images = detupl... |
| `uniform_float_color_image()` | 2908 | Returns an image with the given height and width, where all pixels are the given color If the given ... |
| `blend_images()` | 2940 | Blends two images together using various blending modes.  Args: bot (Union[numpy.ndarray, float, Tup... |
| `overlay_images()` | 3142 | Blends all the given images on top of one another; the last one being on top It takes into considera... |
| `laplacian_blend()` | 3163 | Uses laplacian pyramid blending on two images with a given alpha mask. Note: Right now only RGB imag... |
| `get_checkerboard_image()` | 3258 | Generate a checkerboard image as a numpy array in HWC form. Default parameters look like an actual g... |
| `with_image_glow()` | 3410 | Adds a bloom effect to an image with a given blur and strength. The default values are subject to ch... |
| `with_image_glows()` | 3460 | Plural of with_image_glow images=detuple(images) return [with_image_glow(image,blur=blur,strength=st... |
| `get_progress_bar_image()` | 3529 | Generate a rectangular RGBA progress bar image.  Args: progress (float): Progress value between 0 an... |
| `image_with_progress_bar()` | 3585 | Adds a progress bar to an image. See rp.get_progress_bar_image for further documentation.  EXAMPLE: ... |
| `video_with_progress_bar()` | 3670 | Adds a progress bar to the top of a video to see how far into it you are. See rp.get_progress_bar_im... |
| `boomerang_video()` | 3786 | *(No description)* |
| `slowmo_video_via_rife()` | 3835 |  Doubles the framerate of a given video. Can be a list of images as defined by rp.is_image, or a num... |
| `_crop_images_to_max_or_min_size()` | 3854 | *(No description)* |
| `crop_images_to_max_size()` | 3875 | Makes sure all images have the same height and width Does this by adding additional black space arou... |
| `crop_images_to_min_size()` | 3889 | Makes sure all images have the same height and width Does this by cropping out the edges of the imag... |
| `crop_images_to_max_height()` | 3903 |  Crop all given images to the maximum height of all given images using the same extra args as seen i... |
| `crop_images_to_max_width()` | 3907 |  Crop all given images to the maximum width of all given images using the same extra args as seen in... |
| `crop_images_to_min_height()` | 3911 |  Crop all given images to the minimum height of all given images using the same extra args as seen i... |
| `crop_images_to_min_width()` | 3915 |  Crop all given images to the minimum width of all given images using the same extra args as seen in... |
| `crop_image_to_square()` | 3919 | Crops an image so that it becomes square. If grow==True, the image can become larger instead of smal... |
| `crop_images_to_square()` | 3937 | TODO: Optimize me! |
| `crop_image_at_random_position()` | 3946 | Returns a randomly-positioned cropped version of the input image with the specified height and width... |
| `get_random_crop_bounds()` | 3998 | Generate random bounds for cropping an image or any n-dimensional array.  Parameters: image_dimensio... |
| `get_center_crop_bounds()` | 4058 | Generate bounds for center cropping an image or any n-dimensional array.  Parameters: image_dimensio... |
| `trim_video()` | 4134 | This function takes a video and a length, and returns a video with that length If the desired length... |
| `trim_videos()` | 4179 | Plural of rp.trim_video videos = detuple(videos)  output = [] for video in videos: video = trim_vide... |
| `_trim_videos_to_same_length()` | 4190 | If mode = max, adds blank frames to the end of videos to make sure they're all the same number of fr... |
| `trim_videos_to_max_length()` | 4213 | *(No description)* |
| `trim_videos_to_min_length()` | 4216 | *(No description)* |
| `_concatenated_videos()` | 4219 | *(No description)* |
| `horizontally_concatenated_videos()` | 4227 | *(No description)* |
| `vertically_concatenated_videos()` | 4231 | *(No description)* |
| `max_filter()` | 4235 | *(No description)* |
| `min_filter()` | 4274 | *(No description)* |
| `med_filter()` | 4313 | *(No description)* |
| `range_filter()` | 4352 | *(No description)* |
| `_auto_interp_for_resize_image()` | 4377 | A private function used by image resizing functions in rp when their interp=='auto'  'area' interpol... |
| `_resize_image_via_skimage()` | 4456 | Resize using scikit-image (slower but handles more cases). assert is_image(image) pip_import("skimag... |
| `resize_image()` | 4478 | resize_image resizes images. Who woulda thunk it? Stretchy-squishy image resizing! Now uses cv_resiz... |
| `xy_float_images()` | 4514 | Returns a pair of grayscale images: x, y Where they increase from 0 to 1 on that axis  Args: height ... |
| `is_torch_image()` | 4691 | Enhanced Documentation: Checks if an object is a PyTorch tensor representing an image in CHW format ... |
| `is_pil_image()` | 4734 | Check if input is a PIL Image instance.  PIL images have limited dtype support compared to NumPy. Mo... |
| `_is_skia_image()` | 4743 | Returns a random index for a given array or array length.  If the input is a dictionary or a subclas... |
| `skip_filter()` | 5657 | *(No description)* |
| `load_image_from_clipboard()` | 5790 |  #Grab an image copied from your clipboard  #TODO: Use the "copykitten" library to paste images pip_... |
| `_copy_image_to_clipboard_via_pyjpgclipboard()` | 5834 | (This function works fine! But it didnt support RGBA images so it's obsolete now)  Takes an image or... |
| `_copy_image_to_clipboard_via_copykitten()` | 5861 | Copies an image to the system clipboard Can handle RGBA images https://github.com/Klavionik/copykitt... |
| `copy_image_to_clipboard()` | 5876 | Copies an image to the system clipboard  EXAMPLE:  >>> ans = get_youtube_video_thumbnail('https://ww... |
| `load_image()` | 5894 |  Automatically detect if location is a URL or a file path and try to smartly choose the appropriate ... |
| `load_rgb_image()` | 5960 | Like load_image, but makes sure there's no alpha channel This function is really only here to save y... |
| `load_images()` | 5978 | Simply the plural form of load_image This is much faster than using load_image sequentially because ... |
| `_load_image()` | 6017 | *(No description)* |
| `_load_images_via_pdf2image()` | 6069 |  Given a PDF, returns a list of images - one for each page  return _load_images_via_pdf2image(path) ... |
| `load_pdf_as_images()` | 6088 |  Given a PDF, returns a list of images - one for each page  return _load_images_via_pdf2image(path) ... |
| `load_image_from_file()` | 6130 |  Can try opencv as a fallback if this ever breaks  assert file_exists(file_name),'No such image file... |
| `_load_image_from_file_via_PIL()` | 6165 | NOTE if this method fails try the following function: imageio.plugins.freeimage.download() #https://... |
| `_load_image_from_file_via_imageio()` | 6175 | NOTE if this method fails try the following function: imageio.plugins.freeimage.download() #https://... |
| `_load_image_from_file_via_scipy()` | 6185 | *(No description)* |
| `_load_image_from_file_via_opencv()` | 6189 | Url should either be like http://website.com/image.png or like data:image/png;base64,iVBORw0KGgoAAAA... |
| `load_image_from_url()` | 6208 | Url should either be like http://website.com/image.png or like data:image/png;base64,iVBORw0KGgoAAAA... |
| `load_image_from_matplotlib()` | 6227 | Return matplotlib's current display as an image You can increase the DPI to get a higher resolution.... |
| `_get_openexr_image_dimensions()` | 6280 | Returns True iff the file path points to an exr file |
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
| `save_openexr_image()` | 7113 | Counterpart to load_openexr_image TODO: Add support for custom channels This code is based on https:... |
| `convert_image_file()` | 7173 | Converts an image file to a specified format and saves it to the provided output folder. It can also... |
| `convert_image_files()` | 7249 | Converts multiple image files to a specified format and saves them to the provided output folder. Th... |
| `_convert_image()` | 7327 | *(No description)* |
| `load_sound_file()` | 7937 | Returns the contents of a sound file at file_path as a numpy array of floats in the range [-1, 1] sa... |
| `play_sound_from_samples()` | 8011 | For stereo, use a np matrix Example: psfs((x%100)/100 for x in range(100000)) Each sample should ∈ [... |
| `play_sound_file()` | 8036 | THIS Function is an abstraction of playing sound files. Just plug in whatever method works on your c... |
| `play_sound_file_via_afplay()` | 8058 | Use stop_sound to stop it. If parallel==False, the code will pause until the song is finished playin... |
| `play_sound_file_via_pygame()` | 8080 | Old because it uses the pygame.mixer.sound instead of pygame.mixer.music, which accepts more file ty... |
| `stop_sound()` | 8097 | Stop sounds from all sources I know of that the 'r' module can make. So far I have been unsuccessful... |
| `convert_audio_file()` | 8166 | Convert an audio file to a different format using FFmpeg.  Args: input_file (str): Path to the input... |
| `_display_image_in_notebook_via_ipyplot()` | 8236 | Private function to display images in Jupyter notebooks using ipyplot.  Internal implementation for ... |
| `_display_image_in_notebook_via_ipython()` | 8256 | Add the current Python interpreter as a Jupyter IPython kernel.  Parameters: - kernel_name: The name... |
| `display_video()` | 8310 | Video can either be a string, or a video (aka a 4d tensor or iterable of images) Example: display_vi... |
| `_make_video_dimensions_even()` | 8394 | Make the video have an even height and width. Used for saving MP4's. Without this, if a video with o... |
| `_display_video_via_mediapy()` | 8410 |  Use mediapy to display a video in a Jupyter notebook  rp.pip_import('mediapy') import mediapy  #Pre... |
| `display_video_in_notebook()` | 8423 | Display a video or image in a Jupyter notebook.  Args: video: The video object to display. - Can be ... |
| `_display_video_in_notebook()` | 8446 | *(No description)* |
| `display_video_in_notebook_webp()` | 8504 | Displays an animated webp in a Jupyter notebook with a specified quality and framerate See rp.displa... |
| `save_video()` | 8519 | #      #     This will embed a video into the jupyter notebook you're using #     Warning: This func... |
| `_display_downloadable_image_in_notebook_via_ipython()` | 8550 |  Display an image at full resolution in a jupyter notebook. Returns an updatable channel.   channel ... |
| `display_image_in_notebook()` | 8561 |  Display an image at full resolution in a jupyter notebook. Returns an updatable channel.   channel ... |
| `_image_to_html()` | 8592 | Used for displaying and updating content in Jupyter notebooks. It's analagous to a bunch of televisi... |
| `display_image()` | 8745 | Very simple to understand: this function displays an image. At first, it tries to use matplotlib and... |
| `display_alpha_image()` | 8871 | Display image with checkerboard background to visualize transparency.  Shows transparent areas as ch... |
| `_display_image_slideshow_animated()` | 8885 | This works best on Jupyter notebooks right now It technically works without a jupyter notebook...but... |
| `display_image_slideshow()` | 9015 | Enters an interactive image slideshow Useful for exploring large folders/lists of images images: ima... |
| `zoom_crop_origin()` | 9099 | *(No description)* |
| `blend()` | 9805 | Linearly interpolates between different values with fractional indices. This is written in pure pyth... |
| `iblend()` | 9807 | Linearly interpolates between different values with fractional indices. This is written in pure pyth... |
| `_filter_dict_via_fzf()` | 11266 | Uses fzf to select a subset of a dict and returns that dict. #Refactored using GPT4 from a mess: htt... |
| `load_image_from_webcam()` | 13232 | If your camera supports multiple resolutions, input the dimensions in the height and width parameter... |
| `load_image_from_screenshot_via_mss()` | 13293 | Grabs a screenshot from the main monitor using the Multiple Screen Shots (MSS) Library Returns it as... |
| `load_image_from_screenshot()` | 13319 | Grabs a screenshot from the main monitor Returns it as a RGB byte image  EXAMPLE:  >>> while True: .... |
| `_load_image_from_screenshot_via_pyscreenshot()` | 13346 | REPLACED BY load_image_from_screenshot WHICH IS MUCH FASTER (This still works as a slow version thou... |
| `_load_image_from_webcam_in_jupyter_notebook()` | 13359 | VIDEO_HTML =  <video autoplay width=800 height=600></video> <script> var video = document.querySelec... |
| `record_mono_audio()` | 13399 | You can count on this method having a delay (between when you call the method and when it actually s... |
| `audio_stretch()` | 16367 | >>> audio_stretch([1,10],10) ans = [1,2,3,4,5,6,7,8,9,10] |
| `cluster_filter()` | 16561 | EXAMPLE: cluster_filter([2,3,5,9,4,6,1,2,3,4],lambda x:x%2==1) --> [[3, 5, 9], [1], [3]]  <---- It s... |
| `encode_float_matrix_to_rgba_byte_image()` | 16615 | Can encode a 32-bit float into the 4 channels of an RGBA image The values should be between 0 and 1 ... |
| `decode_float_matrix_from_rgba_byte_image()` | 16635 | This function is the inverse of encode_float_matrix_to_rgba_image Takes an rgba byte-image (that was... |
| `latex_image()` | 17177 | Returns an rgba image with the rendered latex string on it in numpy form |
| `display_image_in_terminal()` | 17195 | Uses unicode, and is black-and-white EXAMPLE: while True: display_image_in_terminal(load_image_from_... |
| `display_image_in_terminal_color()` | 17249 | Will attempt to draw a color image in the terminal This is slower than display_image_in_terminal, an... |
| `display_image_in_terminal_imgcat()` | 17320 | Can display images in some terminals as actual images  Works in: iterm2 wezterm tmux (if configured ... |
| `display_video_in_terminal_color()` | 17360 | Display a video in the terminal with a progress bar.  Args: frames (list): List of frames to display... |
| `_skimage_skeletonize()` | 17435 |  OpenCV function to return a skeletonized version of img, a Mat object cv2=pip_import('cv2') # Found... |
| `print_latex_image()` | 17517 | r >>> print_latex_image("\sum_{n=3}^7x^2") ⠀⠀⠀⠀⠠⠟⢉⠟ ⠀⠀⠀⠀⠀⠀⡏ ⠀⠀⠀⠀⠀⠀⠃ ⢀⢀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡀ ⠀⠙⠄⠀⠀⠀⠀⠀⠀... |
| `rotate_image()` | 18010 | Returns a rotated image by angle_in_degrees, clockwise The output image size is usually not the same... |
| `rotate_images()` | 18090 | Plural of rotate_image. Arguments are broadcastable. Angles are measured in degrees!  EXAMPLE:  >>> ... |
| `_rotate_rgb_image()` | 18136 | Will return an RGB image, not an RGBA one |
| `blend_rgb()` | 19426 | *(No description)* |
| `is_image_file()` | 20437 | Check if file path points to an image file based on extension/mimetype.  Checks file extension and m... |
| `is_video_file()` | 20482 | Check if a file is a video file based on MIME type detection.  Enhanced Documentation: Determines if... |
| `is_sound_file()` | 20534 | Returns True iff the file path is a UTF-8 file Faster than trying to use text_file_to_string(path), ... |
| `_view_image_via_textual_imageview()` | 21186 | Views image in a terminal using textual-imageview.  Enhanced Documentation: ========================... |
| `_display_pterm_image()` | 22495 | *(No description)* |
| `rgb_histogram_image()` | 28605 | Takes an image, or its color histograms Returns an image with RGB graphs of the colors in that image... |
| `byte_image_histogram()` | 28676 | Given an image, returns a matrix with shape (num_channels, 256) |
| `cv_apply_affine_to_image()` | 28698 | Warps an image to the affine matrix provided (of shape 2,3) output_resolution is to speed things up ... |
| `is_opaque_image()` | 29225 | If there is a single transparent pixel in the image, return false Equivalent to the slower: return (... |
| `is_transparent_image()` | 29243 | If there is a single transparent pixel in the image, return True Equivalent to the slower: return (a... |
| `_alpha_weighted_rgba_image_func()` | 29251 | Func is a function that looks like func(image, *args, **kwargs) and operates on RGBA images as defin... |
| `contours_to_image()` | 29651 | Returns a grayscale binary image of dtype bool This function draws the given path onto a blank, blac... |
| `contour_to_image()` | 29681 |  The singular form of contours_to_image (just give it one contour instead of a list of contours)  re... |
| `_omni_load_animated_image()` | 30351 |  gif and webp and png can be either a video or image depending on context...  video = load_video(pat... |
| `_omni_save_animated_image()` | 30358 |  gif and webp and png can be either a video or image depending on context...  if is_image(video): re... |
| `_labeled_image_text_to_image()` | 30919 | *(No description)* |
| `labeled_image()` | 30931 | Adds a label to an image and returns an image 'size' is either measured in pixels (int), or is in pr... |
| `_images_are_all_same_size()` | 31152 |  TODO: Use this for video processing functions instead of using for loops to check if image sizes ar... |
| `labeled_images()` | 31161 | The plural of labeled_image See rp.labeled_image's documentation TODO: Optimize this when video is n... |
| `labeled_videos()` | 31216 | The plural of labeled_images See rp.labeled_image's documentation TODO: Optimize this when videos ar... |
| `_cv_char_to_image()` | 31245 | Right now this is approx 2x slower than non-monospace, even with the optimizations. I could probably... |
| `_cv_text_to_image_monospace()` | 31253 | Right now this is approx 2x slower than non-monospace, even with the optimizations. I could probably... |
| `horizontally_concatenated_images()` | 31263 | *(No description)* |
| `cv_text_to_image()` | 31288 | Uses OpenCV to write words on an image, and returns that image  EXAMPLE DEMO (Shows all fonts): >>> ... |
| `_single_line_cv_text_to_image()` | 31346 | EXAMPLE: display_image(cv_text_to_image('HELLO WORLD! ')) This is a helper function for cv_text_to_i... |
| `_slow_pil_text_to_image()` | 31370 | Works well! But is SO FUCKING SLOW on its own...by putting characters together and concating them we... |
| `pil_text_to_image()` | 31797 | r Uses PIL as an alternative backend to cv_text_to_image Returns an image with the given text and si... |
| `skia_text_to_image()` | 31901 | Renders multiline text via python-skia - a very fast graphics library that powers Google Chrome. Sup... |
| `skia_stamp_image()` | 32139 | Stamps a sprite onto a canvas using the high-performance Skia library. Signature based on rp.stamp_t... |
| `get_all_image_files()` | 33445 |  Like get_all_files, but only returns image files. This function is just sugar.   #TODO: Once get_al... |
| `horizontally_concatenated_images()` | 34064 | First image in image_list goes on the left TODO: Handle non-RGB images (include RGBA, grayscale, etc... |
| `vertically_concatenated_images()` | 34112 | First image in image_list goes on the top  EXAMPLE (Demo origin): >>> for origin in 'left center rig... |
| `grid_concatenated_images()` | 34145 | Given a list of lists of images, like [[image1, image2],[image3,image4]], join them all together int... |
| `tiled_images()` | 34216 | EXAMPLE: display_image_in_terminal_color(tiled_images([load_image('https://i.pinimg.com/236x/36/69/3... |
| `tiled_videos()` | 34273 | Tiles videos together. Uses same args and kwargs as rp.tiled_images - see its docstring for what the... |
| `vertically_flipped_image()` | 34317 | Flips (aka mirrors) an image vertically. if is_pil_image(image): from PIL import Image return image.... |
| `horizontally_flipped_image()` | 34325 | Flips (aka mirrors) an image horizontally. if is_pil_image(image): from PIL import Image return imag... |
| `_get_byte_to_binary_grayscale_image_floyd_steinburg_dithering_function()` | 34432 | *(No description)* |
| `is_image()` | 34513 | An image must be either grayscale (a numpy matrix), rgb (a HWC tensor), or rgba (a HWC tensor) and h... |
| `is_grayscale_image()` | 34541 | Check if image is grayscale (2D array with shape HW).  Returns True for 2-dimensional numpy arrays o... |
| `is_rgb_image()` | 34590 | Check if image is RGB (3D array with shape HW3).  Returns True for arrays with exactly 3 color chann... |
| `is_rgba_image()` | 34642 | Check if image is RGBA (3D array with shape HW4).  Returns True for arrays with exactly 4 channels (... |
| `_grayscale_image_to_grayscale_image()` | 34694 | Convert grayscale to RGB by duplicating channels. Internal helper for as_rgb_image(). return graysca... |
| `_grayscale_image_to_rgb_image()` | 34695 | Convert grayscale to RGB by duplicating channels. Internal helper for as_rgb_image(). return graysca... |
| `_rgb_image_to_rgb_image()` | 34701 | Copy RGB image unchanged. Internal helper for as_rgb_image() copy=True. return as_numpy_array(image)... |
| `_rgba_image_to_rgb_image()` | 34722 | Convert RGBA to RGB by dropping alpha channel. Internal helper for as_rgb_image(). return as_numpy_a... |
| `as_grayscale_image()` | 34727 |  Returns a 2-dimensional numpy array in HW form (height, width)  assert is_image(image),'Error: inpu... |
| `as_rgb_image()` | 34735 |  Returns a 3-dimensional numpy array in HW3 form (height, width, channels)  Enhanced Documentation: ... |
| `as_rgba_image()` | 34777 |  Returns a 3-dimensional numpy array in HW4 form (height, width, channels)  assert is_image(image),'... |
| `is_float_image()` | 34786 | A float image is made with floating-point real values between 0 and 1 https://stackoverflow.com/ques... |
| `is_byte_image()` | 34822 | A byte image is made of unsigned bytes (aka np.uint8) Return true if the datatype is an integer betw... |
| `is_binary_image()` | 34867 | A binary image is made of boolean values (AKA true or false)  Enhanced Documentation: - Used for spe... |
| `_clamp_float_image()` | 34884 | Take some floating image and make sure that it has no negative numbers or numbers >1 |
| `_float_image_dtype()` | 34897 |  Returns a numpy array with floating point values (usually between 0 and 1)  Enhanced Documentation:... |
| `_binary_image_to_binary_image()` | 34907 |  Returns a numpy array with floating point values (usually between 0 and 1)  Enhanced Documentation:... |
| `as_float_image()` | 34912 |  Returns a numpy array with floating point values (usually between 0 and 1)  Enhanced Documentation:... |
| `as_byte_image()` | 34948 |  Returns a numpy array with dtype np.uint8  Enhanced Documentation:  Converts images to byte format ... |
| `as_binary_image()` | 34994 | Returns a nummpy array with dtype bool EXAMPLE of 'dither': while True: display_image(as_binary_imag... |
| `_images_conversion()` | 35010 | Private helper function for batch image format conversion with optimization.  Used internally by RP'... |
| `as_grayscale_images()` | 35141 | Convert list of images to grayscale. See as_grayscale_image for single images. return _images_conver... |
| `_common_image_channel_converter()` | 35145 | Given a list of images, choose the cheapest as_*_image function that preserves as much data as possi... |
| `_common_image_dtype_converter()` | 35151 | Given a list of images, choose the cheapest as_*_image function that preserves as much data as possi... |
| `_common_image_converter()` | 35157 | *(No description)* |
| `blend_colors()` | 35577 | *(No description)* |
| `get_image_dimensions()` | 35676 |  Return (height,width) of an image  Enhanced Documentation: Gets the dimensions (height, width) of a... |
| `get_image_height()` | 35731 | Return the image's height measured in pixels  Enhanced Documentation: Gets the height of an image in... |
| `get_image_width()` | 35765 | Return the image's width measured in pixels  Enhanced Documentation: Gets the width of an image in p... |
| `get_video_height()` | 35799 | Get height of video from different formats (THWC NumPy, TCHW torch, or sequence of images).  Example... |
| `get_video_heights()` | 35818 | Get heights from multiple videos. Plural version of get_video_height.  Enhanced Documentation: Appli... |
| `get_video_width()` | 35853 | Get width of video from different formats (THWC NumPy, TCHW torch, or sequence of images).  Examples... |
| `get_video_widths()` | 35872 | Get widths from multiple videos. Plural version of get_video_width.  Enhanced Documentation: Applies... |
| `bordered_image_solid_color()` | 36234 | Add a pixel border of color around the image with a solid color Currently converts the input image i... |
| `bordered_images_solid_color()` | 36297 |  Plural of rp.bordered_image_solid_color  images=detuple(images) return [bordered_image_solid_color(... |
| `get_youtube_video_url()` | 36888 | Gets the url of a youtube video, given either the url (in which case nothing changes) or its id  Exa... |
| `_is_youtube_video_url()` | 36905 | Returns the captions/subtitles for a YouTube video based on the given URL or video ID.  NOTE: If it ... |
| `get_youtube_video_transcript()` | 36909 | Returns the captions/subtitles for a YouTube video based on the given URL or video ID.  NOTE: If it ... |
| `download_youtube_video()` | 36954 | Downloads a YouTube video based on the given URL or video ID. The function can selectively download ... |
| `_get_youtube_video_data_via_embeddify()` | 37095 | See https://pypi.org/project/embeddify/ Uses a specification called 'oembed', which lets us get info... |
| `get_youtube_video_title()` | 37111 | Returns the title of a youtube video, given either its url or video id  Example: >>> get_youtube_vid... |
| `get_youtube_video_thumbnail()` | 37124 | Returns the thumbnail of a youtube video, either as a url or an image EXAMPLE: >>> display_image(get... |
| `_moviepy_VideoFileClip()` | 37144 |  Moviepy 2 has breaking changes! They moved a class. See https://zulko.github.io/moviepy/getting_sta... |
| `_get_video_file_duration_via_moviepy()` | 37162 | Returns the duration of a video file, in seconds https://stackoverflow.com/questions/3844430/how-to-... |
| `get_video_file_duration()` | 37170 |  Returns a float, representing the total video length in seconds  path=get_absolute_path(path) #This... |
| `_get_video_file_framerate_via_moviepy()` | 37180 |  Given a (str) path to a video file, returns a number (framerate)  path = get_absolute_path(path) #I... |
| `_get_video_file_framerate_via_ffprobe()` | 37192 | Slower than _get_video_file_framerate_via_moviepy but no extra python dependencies Given a (str) pat... |
| `get_video_file_framerate()` | 37228 |  Given a (str) path to a video file, returns a number (framerate)  try: pip_import('moviepy')  #Ning... |
| `_load_video_stream()` | 37248 | *(No description)* |
| `load_video_stream()` | 37268 | Much faster than load_video, which loads all the frames into a numpy array. This means load_video ha... |
| `load_video_streams()` | 37308 |  Plural of load_video_stream. If transpose==True, returns a single iterator that returns tuples of f... |
| `load_video()` | 37350 | This function does not take into account framerates or audio. It just returns a numpy array full of ... |
| `load_videos()` | 37429 | Plural of load_video Loads many videos.  Args: See load_video for documentation on the paths, start_... |
| `save_video_avi()` | 37468 | Saves the frames of the video to an .avi file |
| `_get_default_video_path()` | 37501 |  As a bitrate  if video_bitrate in _named_video_bitrates: video_bitrate = _named_video_bitrates[vide... |
| `_as_video_bitrate()` | 37516 |  As a bitrate  if video_bitrate in _named_video_bitrates: video_bitrate = _named_video_bitrates[vide... |
| `_as_video_quality()` | 37521 |  As a percent  if video_quality in _named_video_qualities: video_quality = _named_video_qualities[vi... |
| `_cv_save_video_mp4()` | 37627 | *(No description)* |
| `_cv_save_video_mp4()` | 37661 | Uses quality instead of bitrate because of how opencv works: https://docs.opencv.org/3.4/d4/d15/grou... |
| `set_save_video_mp4_default_backend()` | 37713 | frames: a list of images as defined by rp.is_image(). Saves an .mp4 file at the path - frames can al... |
| `save_video_mp4()` | 37718 | frames: a list of images as defined by rp.is_image(). Saves an .mp4 file at the path - frames can al... |
| `save_video_gif_via_pil()` | 37809 | Save a video to a GIF with given path and framerate. Returns the path of the new GIF.  TODO: Support... |
| `save_video()` | 38010 | #TODO: add options for sound and framerate. Possibly quality options but probably not (that should b... |
| `encode_video_to_bytes()` | 38050 | Encode video to bytes without saving to disk. |
| `decode_video_from_bytes()` | 38064 | Decode bytes back to video array. |
| `add_audio_to_video_file()` | 38077 | Add audio to a video file without recompressing the video.  This function uses FFmpeg to add audio f... |
| `change_video_file_framerate()` | 38157 | Change the framerate of a video without recompressing or changing the audio. This function uses FFmp... |
| `change_video_file_framerates()` | 38214 | Concatenate multiple MP4 files with zero degradation (no recompression).  Args: input_files (list): ... |
| `shift_image()` | 39555 | Shifts an image on the x and y axes, in image coordinates  As y increases the image moves down As x ... |
| `roll_image()` | 39640 | Shifts/rolls an image by the specified displacement in x and y directions.  NOTE: It uses image coor... |
| `crop_image()` | 39767 | Returns a cropped image to the specified width and height If either hieght or width aren't specified... |
| `crop_images()` | 39856 | Batch crop multiple images to specified dimensions. See crop_image for single images. output = (crop... |
| `crop_videos()` | 39866 | Given some big image that is surrounded by black, or 0-alpha transparency, crop out that excess regi... |
| `crop_videos_to_min_size()` | 39875 | Given some big image that is surrounded by black, or 0-alpha transparency, crop out that excess regi... |
| `crop_videos_to_max_size()` | 39879 | Given some big image that is surrounded by black, or 0-alpha transparency, crop out that excess regi... |
| `crop_image_zeros()` | 39883 | Given some big image that is surrounded by black, or 0-alpha transparency, crop out that excess regi... |
| `edit_image_in_terminal()` | 40488 | Silly (but really fun) function that launches mspaint on an image in the terminal Not very practical... |
| `encode_bytes_to_image()` | 44673 | Encode binary data into a numpy array representing an RGB image.  The function packs the data length... |
| `decode_image_to_bytes()` | 44706 | Decode a numpy array image back to the original binary data.  Extracts the data length from the firs... |
| `inverted_image()` | 46104 |  Inverts the colors of an image. By default, it doesn't touch the alpha channel (if one exists)  ass... |
| `inverted_images()` | 46125 | Batch invert colors of multiple images. See inverted_image for single images.  Enhanced Documentatio... |
| `get_image_file_dimensions()` | 46607 | Takes the file path of an image, and returns the image's (height, width) It does this without loadin... |
| `get_video_file_shape()` | 46627 | Returns the shape of the numpy tensor we would get with rp.load_video(path)  Args: path (str): Path ... |
| `get_video_file_num_frames()` | 46659 | Returns the number of frames in the video. |
| `get_video_file_height()` | 46666 | Returns the height of the video. |
| `get_video_file_width()` | 46673 | Returns the width of the video. |
| `get_image_hue()` | 47017 | Takes in an image as defined by rp.is_image and returns a matrix assert is_image(image) return rgb_t... |
| `get_image_saturation()` | 47022 | Takes in an image as defined by rp.is_image and returns a matrix assert is_image(image) return rgb_t... |
| `get_image_value()` | 47027 | Takes in an image as defined by rp.is_image and returns a matrix assert is_image(image) return rgb_t... |
| `get_image_red()` | 47034 | Takes in an image as defined by rp.is_image and returns a matrix image=as_numpy_image(image,copy=Fal... |
| `get_image_green()` | 47041 | Takes in an image as defined by rp.is_image and returns a matrix image=as_numpy_image(image,copy=Fal... |
| `get_image_blue()` | 47048 | Takes in an image as defined by rp.is_image and returns a matrix image=as_numpy_image(image,copy=Fal... |
| `_with_image_channel()` | 47056 | Helper function to apply a color image or value to a given channel in the main image. :param image: ... |
| `with_image_red()` | 47089 | Modify the red channel of the image with the given red image or value. Returns a float image. |
| `with_image_green()` | 47096 | Modify the green channel of the image with the given green image or value. Returns a float image. |
| `with_image_blue()` | 47103 | Modify the blue channel of the image with the given blue image or value. Returns a float image. |
| `with_image_hue()` | 47110 | Sets the image hue. The hue can either be given as an image, or as a number. alpha=extract_alpha_cha... |
| `shift_image_hue()` | 47136 | EXAMPLE: >>> while True: >>> display_image( >>>     shift_image_hue( >>>         resize_image_to_fit... |
| `with_image_saturation()` | 47151 | Sets the image saturation. The saturation can either be given as an image, or as a number. alpha=ext... |
| `with_image_brightness()` | 47176 | Sets the image brightness. The brightness can either be given as an image, or as a number. alpha=ext... |
| `get_rgb_byte_color_identity_mapping_image()` | 47256 | Save this image, and color-grade it. Then the new image can be used as a map! Originally made for co... |
| `apply_colormap_to_image()` | 47281 | https://stackoverflow.com/questions/52498777/apply-matplotlib-or-custom-colormap-to-opencv-image/526... |
| `cv_image_filter()` | 47722 | Convolves an image with a custom kernel matrix on a per-channel basis  EXAMPLE: img=load_image('http... |
| `wordcloud_image()` | 47774 | EXAMPLE: display_image(wordcloud_image(get_source_code(r))) |
| `_prepare_cv_image()` | 47932 | OpenCV is a bit finicky sometimes Apart from just as_float_image, there are some other requirements |
| `cv_resize_image()` | 47947 | This function is similar to r.resize_image (which uses scipy), except this uses OpenCV and is much f... |
| `cv_resize_images()` | 48056 | Batch resize images using OpenCV. Faster than resize_image for multiple images. |
| `resize_videos()` | 48090 | Resize multiple videos to specified size by resizing each frame.  Wraps resize_images for each video... |
| `skia_resize_image()` | 48150 | Resizes a 4-channel (RGBA) uint8 NumPy array using Skia's high-level resize method, which supports m... |
| `_as_skia_image()` | 48271 | *(No description)* |
| `torch_resize_image()` | 48348 | The given image should be a CHW torch tensor.  Valid sizes: - A single number: Will scale the entire... |
| `torch_resize_images()` | 48407 | Batch resize images using PyTorch. GPU-accelerated when available. |
| `torch_remap_image()` | 48419 | Remap an image tensor using the given x and y coordinate tensors. Out-of-bounds regions will be give... |
| `torch_scatter_add_image()` | 49563 | Scatter add an image tensor using the given x and y coordinate tensors. Pixels warped out-of-bounds ... |
| `resize_image_to_hold()` | 50192 | Resizes an image so that the specified bounding box can fit entirely inside the image, while maintai... |
| `resize_image_to_fit()` | 50246 | Scale image on both axes evenly to fit in this bounding box If not allow_growth, it won't modify the... |
| `resize_images_to_hold()` | 50287 |  Plural of resize_image_to_hold  images = detuple(images)  output = ( resize_image_to_hold( x, heigh... |
| `resize_images_to_fit()` | 50320 |  Plural of resize_image_to_fit  images = detuple(images)  output = ( resize_image_to_fit( x, height,... |
| `resize_video_to_hold()` | 50354 |  Almost the same as resize_images_to_hold - but height and width and interp can be args and returns ... |
| `resize_video_to_fit()` | 50374 |  Almost the same as resize_images_to_fit - but height and width and interp can be args and returns n... |
| `resize_videos_to_fit()` | 50393 |  Plural of resize_image_to_fit  #CODE IS NEAR DUPLICATE OF RESIZE_IMAGES TO FIT!!! videos = detuple(... |
| `resize_videos_to_hold()` | 50429 |  Plural of resize_image_to_hold  #CODE IS NEAR DUPLICATE OF RESIZE_IMAGES TO FIT!!! videos = detuple... |
| `resize_images_to_max_size()` | 50465 | Makes sure all images have the same height and width Does this by stretching all images to the max s... |
| `resize_images_to_min_size()` | 50482 | Makes sure all images have the same height and width Does this by stretching all images to the min s... |
| `resize_videos_to_min_size()` | 50494 | *(No description)* |
| `resize_videos_to_max_size()` | 50500 | Inpaint an image using OpenCV's inpainting methods. The inpainting will be super smooth, and does no... |
| `cv_inpaint_image()` | 50518 | Inpaint an image using OpenCV's inpainting methods. The inpainting will be super smooth, and does no... |
| `image_to_text()` | 51039 | Takes an image, finds text on it, and returns the text as a string (Optical character recognition) I... |
| `compose_rgb_image()` | 51111 |  Create an RGB image from three separate channels  r=as_grayscale_image(r) g=as_grayscale_image(g) b... |
| `compose_rgba_image()` | 51125 |  Create an RGBA image from four separate channels  r=as_grayscale_image(r) g=as_grayscale_image(g) b... |
| `compose_image_from_channels()` | 51142 |  Create an RGB or RGBA image from three or four separate channels  assert len(channels) in (3,4),'Ca... |
| `extract_image_channels()` | 51150 | Given an RGB image of shape (height,width,3) return a tensor of (3,height,width) This function is th... |
| `apply_image_function_per_channel()` | 51171 | Apply a grayscale function on every image channel individually Calls the function with any additiona... |
| `with_image_rgb()` | 51214 |  Counterpart to with_alpha_channel - sets the RGB channels of a potentially RGBA image and returns t... |
| `unwarped_perspective_image()` | 52395 | Takes an image, and two corresponding lists of four points, and returns an unwarped image If you don... |
| `optical_flow_to_image()` | 53405 | Visualize optical flow as an RGB image - and return the image.  The hue represents the angle of the ... |
| `cv_remap_image()` | 53551 | If image is RGBA, then out-of-bounds regions will have 0-alpha This is like a UV mapping - where x a... |
| `get_apriltag_image()` | 53680 | Returns an image with the apriltag corresponding to the given value Please note: the output images a... |
| `get_apriltag_images()` | 53722 | Generate multiple AprilTag images. Plural version of get_apriltag_image.  Enhanced Documentation: Cr... |
| `as_numpy_images()` | 54628 |  Will convert an array of images to BHWC np.ndarray form if it isn't already - supports BCHW torch t... |
| `as_pil_image()` | 54650 |  Will convert an a PIL images if it isn't already - supports BCHW torch tensors, numpy images, etc  ... |
| `as_pil_images()` | 54718 |  Will convert an array of images to PIL images if it isn't already - supports BCHW torch tensors, PI... |
| `as_numpy_image()` | 54722 |  Will convert an image to HWC np.ndarray form if it isn't already - supports CHW torch tensors, PIL ... |
| `as_numpy_video()` | 54751 | Convert video to NumPy THWC format from various input formats.  Enhanced Documentation: - Handles to... |
| `as_numpy_videos()` | 54777 | Convert batch of videos to NumPy BTHWC format.  Handles torch BTCHW → numpy BTHWC conversion for bat... |
| `as_torch_videos()` | 54801 |  Plural of rp.as_torch_video  import torch videos = [gather_args_call(as_torch_video, video) for vid... |
| `as_torch_images()` | 54809 |  Plural of rp.as_torch_image AKA rp.as_torch_video  import torch  if _is_numpy_array(images) or all(... |
| `as_torch_image()` | 54849 |  Converts an image to a floating point torch tensor in CHW form  if is_torch_tensor(image): return i... |
| `filter_by_extension()` | 55915 | *(No description)* |
| `resize_list()` | 56073 | This function stretches or compresses a list to a given length using nearest-neighbor interpolation.... |
| `resize_lists()` | 56134 |  Plural of rp.resize_list  arrays = detuple(arrays) as_numpy = is_numpy_array(arrays)  output = [res... |
| `resize_lists_to_max_len()` | 56144 | Resize multiple lists to match the longest one's length.  Uses resize_list() with nearest-neighbor i... |
| `resize_lists_to_min_len()` | 56162 | Resize multiple lists to match the shortest one's length.  Uses resize_list() with nearest-neighbor ... |
| `resize_list_to_fit()` | 56181 | Will squeeze the input array to fit in the given max_length if it has to. If the array is already sm... |
| `resize_lists_to_fit()` | 56201 | EXAMPLE: >>> list_transpose([[1,2,3],[4,5,6]]) ans = [[1, 4], [2, 5], [3, 6]]  TODO: Fix this behavi... |
| `filter_pids_exist()` | 56965 | Returns the amount of free VRAM for a GPU given its ID. The returned value is in bytes. If gpu_id is... |

## Architectural Analysis

### Media Processing Architecture

RP's media processing system follows a sophisticated pipeline architecture:

1. **Universal Input Handling**: Functions accept numpy arrays, PIL images, file paths, or URLs
2. **Format Agnostic**: Automatic format detection and conversion  
3. **Batch Operations**: Most operations have plural variants for processing multiple items
4. **Backend Multiplexing**: Choice between OpenCV, PIL, scikit-image, etc.
5. **Memory Efficient**: Lazy loading and streaming support for large media files

### Key Patterns
- **Load → Process → Save**: Clear data flow through the pipeline
- **Format Conversion**: Automatic handling of different image/video formats
- **Dimension Handling**: Automatic resizing and cropping for consistency
- **Effect Stacking**: Composable effects like shadows, glows, outlines

## Function Relationships

### Batch Operations
- `with_image_glow()` ↔ `with_image_glows()`
- `trim_video()` ↔ `trim_videos()`
- `load_image()` ↔ `load_images()`
- `save_image()` ↔ `save_images()`
- `convert_image_file()` ↔ `convert_image_files()`
- ... and 18 more

### Multiplexing
- `play_sound_file()` ↔ `play_sound_file_via_afplay()`
- `play_sound_file()` ↔ `play_sound_file_via_pygame()`
- `load_image_from_screenshot()` ↔ `load_image_from_screenshot_via_mss()`

### Type Conversion
- `is_grayscale_image()` ↔ `as_grayscale_image()`
- `is_rgb_image()` ↔ `as_rgb_image()`
- `is_rgba_image()` ↔ `as_rgba_image()`
- `is_float_image()` ↔ `as_float_image()`
- `is_byte_image()` ↔ `as_byte_image()`
- ... and 3 more

