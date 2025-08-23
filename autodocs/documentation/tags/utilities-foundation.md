# RP Library: Utilities Foundation

Core utility functions that support all other operations: type checking, data structures, helpers.

**Total Functions: 1598**

## Function Inventory

| Function | Line | Description |
|----------|------|-------------|
| `format()` | 10 | Return value.__format__(format_spec).  format_spec defaults to the empty string. See the Format Spec... |
| `entuple()` | 186 | For pesky petty things. Code is simpler than explanation here. Primarily used for allowing functions... |
| `detuple()` | 192 | For pesky petty things. Code is simpler than explanation here. Primarily used for allowing functions... |
| `enlist()` | 245 |  For pesky petty things. Code is simpler than explanation here.  if isinstance(x,list): return x ret... |
| `delist()` | 251 |  For pesky petty things. Code is simpler than explanation here.  try: if len(x) == 1: return x[0] ex... |
| `itc()` | 264 | Function currying utility that creates a parameterless lambda closure.  Enhanced Documentation: Crea... |
| `run_func()` | 273 | Function currying utility that creates a parameterless lambda closure.  Enhanced Documentation: Crea... |
| `fog()` | 276 | Function currying utility that creates a parameterless lambda closure.  Enhanced Documentation: Crea... |
| `scoop()` | 320 | Enhanced Documentation:  RP's functional reduce/fold operation - accumulates values by repeatedly ap... |
| `func()` | 507 | from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED  if num_threads is not None... |
| `wrapper()` | 548 | *(No description)* |
| `new_func()` | 549 | *(No description)* |
| `seq()` | 586 | RP's flagship sequential function composition and pipelining utility.  Chains multiple functions tog... |
| `par()` | 679 | Execute multiple functions in parallel with the same arguments.  This function is the parallel count... |
| `pam()` | 770 | The identity function. ƒ﹙𝓍﹚﹦ 𝓍    where   ƒ ≣ identity Examples: identity(2) == 2 identity('Hello Wo... |
| `identity()` | 776 | The identity function. ƒ﹙𝓍﹚﹦ 𝓍    where   ƒ ≣ identity Examples: identity(2) == 2 identity('Hello Wo... |
| `list_roll()` | 792 | Demo: >>> for _ in range(10): print(list_roll(range(10),_)) [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] [9, 0, 1,... |
| `list_flatten()` | 815 | Example Speed boost over scoop: List size: 21000 Time taken by list comprehension: 0.032008200883865... |
| `product()` | 832 | Removes duplicates but preserves order Works with things that aren't conventionally hashable, like n... |
| `unique()` | 844 | Removes duplicates but preserves order Works with things that aren't conventionally hashable, like n... |
| `helper()` | 858 | *(No description)* |
| `tic()` | 875 | *(No description)* |
| `local_toc()` | 878 | *(No description)* |
| `reset_timer()` | 880 | *(No description)* |
| `toc()` | 885 |  Return seconds since common epoch (rounded to the nearest integer)  return _milli_micro_nano_conver... |
| `ptoc()` | 887 |  Return seconds since common epoch (rounded to the nearest integer)  return _milli_micro_nano_conver... |
| `ptoctic()` | 889 |  Return seconds since common epoch (rounded to the nearest integer)  return _milli_micro_nano_conver... |
| `seconds()` | 900 |  Return seconds since common epoch (rounded to the nearest integer)  return _milli_micro_nano_conver... |
| `millis()` | 903 |  Return milliseconds since common epoch (rounded to the nearest integer)  return _milli_micro_nano_c... |
| `micros()` | 906 |  Return microseconds since common epoch (rounded to the nearest integer)  return _milli_micro_nano_c... |
| `nanos()` | 909 |  Return nanoseconds since common epoch (rounded to the nearest integer)  return _milli_micro_nano_co... |
| `get_process_cwd()` | 915 | Get the result of 'cd' in a shell. This is the current folder where save or load things by default. ... |
| `get_current_directory()` | 922 | Get the result of 'cd' in a shell. This is the current folder where save or load things by default. ... |
| `set_current_directory()` | 987 | Temporarily CD into a directory Example: print(get_current_directory()) with SetCurrentDirectoryTemp... |
| `__init__()` | 1000 | A context manager for temporarily setting attributes on an object.  Usage: with TemporarilySetAttr(o... |
| `__enter__()` | 1003 | A context manager for temporarily setting attributes on an object.  Usage: with TemporarilySetAttr(o... |
| `__exit__()` | 1008 | A context manager for temporarily setting attributes on an object.  Usage: with TemporarilySetAttr(o... |
| `__init__()` | 1060 |  def __init__(self, instance, **kwargs): self.instance = instance self.old_attrs = {} self.new_attrs... |
| `__init__()` | 1078 | A context manager for temporarily setting items in a container (list, dict, etc.).  Usage: with Temp... |
| `__enter__()` | 1083 | A context manager for temporarily setting items in a container (list, dict, etc.).  Usage: with Temp... |
| `__exit__()` | 1089 | A context manager for temporarily setting items in a container (list, dict, etc.).  Usage: with Temp... |
| `__init__()` | 1169 | A context manager to conditionally enter another context based on a given condition.  This utility f... |
| `__enter__()` | 1174 | A context manager to conditionally enter another context based on a given condition.  This utility f... |
| `__exit__()` | 1180 | A context manager to conditionally enter another context based on a given condition.  This utility f... |
| `ConditionalContext()` | 1188 | A context manager to conditionally enter another context based on a given condition.  This utility f... |
| `test_conditional_context()` | 1224 | *(No description)* |
| `sample_context()` | 1229 | *(No description)* |
| `wrapper()` | 1261 |  A context manager that prints the value of an expression or callable before and after execution.  A... |
| `__init__()` | 1309 | *(No description)* |
| `_get_value()` | 1316 | *(No description)* |
| `_get_name()` | 1325 | *(No description)* |
| `__enter__()` | 1333 | *(No description)* |
| `__exit__()` | 1339 | *(No description)* |
| `currently_running_windows()` | 1361 | Enhanced Documentation: Checks if the current Python process is running on a Windows operating syste... |
| `currently_running_posix()` | 1384 | Enhanced Documentation:  Detects whether the current code is running on macOS (Darwin system). Uses ... |
| `currently_running_mac()` | 1387 | Enhanced Documentation:  Detects whether the current code is running on macOS (Darwin system). Uses ... |
| `currently_running_linux()` | 1443 | Enhanced Documentation: Checks if the current terminal supports ANSI escape sequences for colors and... |
| `fansi_is_enabled()` | 1507 |  Returns true IFF fansi is enabled  return not _disable_fansi def fansi_is_disabled(): |
| `fansi_is_disabled()` | 1510 |  Returns true IFF fansi is disabled  return _disable_fansi _disable_fansi=False def disable_fansi():... |
| `is_builtin()` | 2144 | Generate and classify chunks of Python for syntax highlighting. Yields tuples in the form: (category... |
| `combine_range()` | 2147 | Generate and classify chunks of Python for syntax highlighting. Yields tuples in the form: (category... |
| `analyze_python()` | 2154 | Generate and classify chunks of Python for syntax highlighting. Yields tuples in the form: (category... |
| `ansi_highlight()` | 2193 |  Apply syntax highlighting to 'code', a given string of python code. Returns an ANSI-styled string f... |
| `is_builtin()` | 2257 | Generate and classify chunks of Python for syntax highlighting. Yields tuples in the form: (category... |
| `combine_range()` | 2260 | Generate and classify chunks of Python for syntax highlighting. Yields tuples in the form: (category... |
| `analyze_python()` | 2267 | Generate and classify chunks of Python for syntax highlighting. Yields tuples in the form: (category... |
| `ansi_highlight()` | 2306 | *(No description)* |
| `line_number_prefix_generator()` | 2322 | *(No description)* |
| `wrapped_line_tokens()` | 2334 | *(No description)* |
| `f()` | 2502 | ).strip() pip_import('pygments') from pygments.styles import  get_all_styles for style in get_all_st... |
| `_get_local_clipboard_string()` | 2516 | Copies a string to the clipboard so you can paste it later First tries to copy the string to the sys... |
| `_set_local_clipboard_string()` | 2523 | Copies a string to the clipboard so you can paste it later First tries to copy the string to the sys... |
| `get_accumulation_string()` | 2672 | *(No description)* |
| `_rgb_to_grayscale()` | 2714 | Takes an image with multiple color channels Takes a 3d tensor as an input (X,Y,RGB) Outputs a matrix... |
| `grayscale_to_rgb()` | 2737 | Apply Gaussian blur to image. Accepts any image type, returns NumPy array.  Args: image: Any valid i... |
| `gauss_blur()` | 2739 | Apply Gaussian blur to image. Accepts any image type, returns NumPy array.  Args: image: Any valid i... |
| `flat_circle_kernel()` | 2803 |  Returns a binary grayscale image (aka boolean matrix) with a circle in the middle with the given di... |
| `gaussian_kernel()` | 2817 | Returns a normalized 2D Gaussian kernel. Please note that increasing 'size' does NOT increase 'sigma... |
| `get_max_image_dimensions()` | 2841 |  Given a set of images, return the maximum height and width seen across all of them  Enhanced Docume... |
| `get_max_video_dimensions()` | 2876 |  Given a set of videos, return the maximum height and width seen across all of them  images = detupl... |
| `get_min_video_dimensions()` | 2886 |  Given a set of videos, return the minimum height and width seen across all of them  images = detupl... |
| `get_min_image_dimensions()` | 2896 |  Given a set of images, return the minimum height and width seen across all of them  images = detupl... |
| `get_checkerboard_image()` | 3258 | Generate a checkerboard image as a numpy array in HWC form. Default parameters look like an actual g... |
| `with_drop_shadow()` | 3335 | Applies a drop shadow to an image **DEFAULT ARGUMENT VALUES ARE SUBJECT TO CHANGE** |
| `with_drop_shadows()` | 3358 | Applies an alpha mask to round off the corners of an image Radius is, of course, measured in pixels ... |
| `with_corner_radius()` | 3361 | Applies an alpha mask to round off the corners of an image Radius is, of course, measured in pixels ... |
| `with_corner_radii()` | 3467 | You should set inner_radius>0 or outer_radius>0  include_edges (bool): Has an effect when inner_radi... |
| `get_alpha_outline()` | 3472 | You should set inner_radius>0 or outer_radius>0  include_edges (bool): Has an effect when inner_radi... |
| `with_alpha_outline()` | 3499 | Add colored outline around alpha edges of image. Useful for text, logos, sprites.  Args: inner_radiu... |
| `with_alpha_outlines()` | 3524 | Generate a rectangular RGBA progress bar image.  Args: progress (float): Progress value between 0 an... |
| `get_progress_bar_image()` | 3529 | Generate a rectangular RGBA progress bar image.  Args: progress (float): Progress value between 0 an... |
| `helper()` | 3769 | *(No description)* |
| `_get_executable()` | 3794 | Returns the path to the rife-ncnn-vulkan executable or if it doesn't exist in rp downloads it rife_d... |
| `_get_rife_executable()` | 3813 | Returns the path to the rife-ncnn-vulkan executable or if it doesn't exist in rp downloads it rife_d... |
| `_get_esrgan_executable()` | 3824 | Returns the path to the realesrgan-ncnn-vulkan executable or if it doesn't exist in rp downloads it ... |
| `crop_image_at_random_position()` | 3946 | Returns a randomly-positioned cropped version of the input image with the specified height and width... |
| `get_random_crop_bounds()` | 3998 | Generate random bounds for cropping an image or any n-dimensional array.  Parameters: image_dimensio... |
| `get_center_crop_bounds()` | 4058 | Generate bounds for center cropping an image or any n-dimensional array.  Parameters: image_dimensio... |
| `grid2d()` | 4355 | *(No description)* |
| `width()` | 4365 | A private function used by image resizing functions in rp when their interp=='auto'  'area' interpol... |
| `height()` | 4367 | A private function used by image resizing functions in rp when their interp=='auto'  'area' interpol... |
| `xy_torch_matrices()` | 4554 | Sister function of xy_float_images, but this one uses torch tensors  Returns a pair of matrices: x, ... |
| `_is_instance_of_module_class()` | 4616 | Determines if 'x' (object) is an instance of a class (specified by 'class_name') in a module (specif... |
| `is_numpy_array()` | 4637 | Checks if object is NumPy ndarray without requiring numpy import.  Enhanced Documentation: - Used fo... |
| `is_torch_tensor()` | 4657 | Checks if an object is a PyTorch tensor without requiring torch to be imported.  Enhanced Documentat... |
| `is_torch_image()` | 4691 | Enhanced Documentation: Checks if an object is a PyTorch tensor representing an image in CHW format ... |
| `is_torch_module()` | 4722 | Check if input is a PIL Image instance.  PIL images have limited dtype support compared to NumPy. Mo... |
| `_is_pandas_dataframe()` | 4725 | Check if input is a PIL Image instance.  PIL images have limited dtype support compared to NumPy. Mo... |
| `_is_pandas_series()` | 4728 | Check if input is a PIL Image instance.  PIL images have limited dtype support compared to NumPy. Mo... |
| `_is_pandas_iloc_iterable()` | 4731 | Check if input is a PIL Image instance.  PIL images have limited dtype support compared to NumPy. Mo... |
| `is_pil_image()` | 4734 | Check if input is a PIL Image instance.  PIL images have limited dtype support compared to NumPy. Mo... |
| `_is_skia_image()` | 4743 | Returns a random index for a given array or array length.  If the input is a dictionary or a subclas... |
| `_is_easydict()` | 4747 | Returns a random index for a given array or array length.  If the input is a dictionary or a subclas... |
| `random_index()` | 4754 | Returns a random index for a given array or array length.  If the input is a dictionary or a subclas... |
| `random_element()` | 4793 | Returns a random element from an iterable, dictionary-like, or set-like object.  Parameters: x (iter... |
| `random_element()` | 4824 |  from collections.abc import Mapping, Set, Iterable import random  if isinstance(x, Mapping): keys =... |
| `random_choice()` | 4857 | Either n is an integer (as a length) OR n is an iterable |
| `random_permutation()` | 4860 | Either n is an integer (as a length) OR n is an iterable |
| `is_a_permutation()` | 4868 | A permutation is a list of ints ranging from 0 to len(permutation)-1 It's used to specify a reorderi... |
| `inverse_permutation()` | 4875 | Returns the 'undo' of a given permutation EXAMPLE: a=list(range(100)) p=random_permutation(100) asse... |
| `randint()` | 4893 | If both a and b are specified, the range is inclusive, choose from range［a，b] ⋂ ℤ Otherwise, if only... |
| `randints()` | 4902 | Generate N random integers Example: randints(10)   ====   [9, 36, 82, 49, 13, 9, 62, 81, 80, 66] Thi... |
| `randint_complex()` | 4915 | Arguments passed to this function are passed to 'randint' The only difference between this function ... |
| `randints_complex()` | 4934 | Generate N uniformly distributed random floats Example: random_floats(10)   ====   [0.547 0.516 0.42... |
| `random_float()` | 4943 | Generate N uniformly distributed random floats Example: random_floats(10)   ====   [0.547 0.516 0.42... |
| `random_float_complex()` | 4947 | Generate N uniformly distributed random floats Example: random_floats(10)   ====   [0.547 0.516 0.42... |
| `random_floats()` | 4950 | Generate N uniformly distributed random floats Example: random_floats(10)   ====   [0.547 0.516 0.42... |
| `random_floats_complex()` | 4962 | Arguments passed to this function are passed to 'random_floats' The only difference between this fun... |
| `random_chance()` | 4981 | Given an input list, torch tensor, numpy array, dict, etc - get a random subset with a given batch_s... |
| `random_batch()` | 4984 | Given an input list, torch tensor, numpy array, dict, etc - get a random subset with a given batch_s... |
| `random_batch_up_to()` | 5095 | Like random batch, but when batch_size is larger than the full_list, the output will only have the l... |
| `random_batch_with_replacement()` | 5109 | Like random_batch, but it handles batch_size larger than len(full_list) by nicely repeating elements... |
| `random_substring()` | 5170 |  Gets a random substring with a given length  if length is None: #If length isn't given, choose a ra... |
| `shuffled()` | 5182 |  Randomly shuffle a copy of a list and return it  if isinstance(l,str):  # random_permutation("ABCDE... |
| `random_parallel_batch()` | 5188 | *(No description)* |
| `temporary_random_seed()` | 5230 | A context manager that sets the random seed for the duration of the context block using the standard... |
| `temporary_numpy_random_seed()` | 5271 | A context manager that sets the random seed for the duration of the context block using NumPy's rand... |
| `temporary_torch_random_seed()` | 5314 | A context manager that sets PyTorch's random seed for the duration of the context block. If no seed ... |
| `seed_all()` | 5363 | Set random seeds for Python's random, NumPy, and PyTorch.  Parameters: seed (int, optional): The see... |
| `temporary_seed_all()` | 5401 | A context manager that sets all random seeds (Python random, NumPy, and PyTorch) for the duration of... |
| `run_as_new_thread()` | 5431 | Used when we simply don't need/want all the complexities of the threading module. An anonymous threa... |
| `run_as_new_process()` | 5450 | Used when we simply don't need/want all the complexities of the multiprocessing module An anonymous ... |
| `is_valid_url()` | 5470 |  Return true iff the url string is syntactically valid  Enhanced Documentation:  Validates whether a... |
| `progress_func()` | 5607 | *(No description)* |
| `progress_func()` | 5621 | *(No description)* |
| `progress_func()` | 5631 | *(No description)* |
| `__init__()` | 5968 | Simply the plural form of load_image This is much faster than using load_image sequentially because ... |
| `__getitem__()` | 5972 | Simply the plural form of load_image This is much faster than using load_image sequentially because ... |
| `__len__()` | 5975 | Simply the plural form of load_image This is much faster than using load_image sequentially because ... |
| `load_pdf_as_images()` | 6088 |  Given a PDF, returns a list of images - one for each page  return _load_images_via_pdf2image(path) ... |
| `get_pdf_num_pages()` | 6092 |  Given a path to a PDF file, returns the number of pages in it  pip_import("pdf2image") import pdf2i... |
| `load_pdf_as_text()` | 6099 |  Given a PDF, returns the text content as a string  return _load_pdf_as_text_via_pdfminer(path)  def... |
| `_load_pdf_as_text_via_pdfminer()` | 6103 |  Extract text from PDF using pdfminer.six  pip_import('pdfminer') from pdfminer.high_level import ex... |
| `_init_pillow_heif()` | 6155 | *(No description)* |
| `_get_openexr_image_dimensions()` | 6280 | Returns True iff the file path points to an exr file |
| `is_valid_openexr_file()` | 6297 | Returns True iff the file path points to an exr file |
| `get_openexr_channels()` | 6305 | Gets a set of strings indicating what channels are in a given .exr file Note that .exr files are flo... |
| `temp_saved_image()` | 6805 | Return the path of an image, and return the path we saved it to Originally used for google colab to ... |
| `_get_files_from_paths()` | 7154 | Takes a folder, a list of files, or a list of files and folders as input - all of which can be globb... |
| `text_to_speech_via_apple()` | 7393 | Apple macOS text-to-speech backend using the system 'say' command.  Enhanced Documentation: This is ... |
| `text_to_speech_via_google()` | 7566 | Convert text to speech using Google Translate's Text-to-Speech API.  A _via_ variant function implem... |
| `__init__()` | 7671 | *(No description)* |
| `strip()` | 7690 |  Do the Web request and save to `savefile`  with open(savefile,'wb') as f: self.write_to_fp(f) f.clo... |
| `write_to_fp()` | 7705 |  Do the Web request and save to a file-like object  for idx,part in enumerate(self.text_parts): payl... |
| `_tokenize()` | 7733 |  Tokenizer on basic roman punctuation   punc="¡!()[]¿?.,;:—«»\n" punc_list=[re.escape(c) for c in pu... |
| `_minimize()` | 7746 |  Recursive function that splits `thestring` in chunks |
| `text_to_speech_voices_comparison()` | 7785 | Will cycle through different voices so you can choose which one you like best. I selected my favorit... |
| `text_to_speech()` | 7794 | An abstract combination of the other two text-to-speech methods that automatically selects the right... |
| `_fig()` | 7860 | np.set_printoptions is used to format the printed output of arrays. It makes the terminal output muc... |
| `set_numpy_print_options()` | 7870 | np.set_printoptions is used to format the printed output of arrays. It makes the terminal output muc... |
| `read()` | 7899 | MP3 to numpy array a = pydub.AudioSegment.from_mp3(f) y = np.array(a.get_array_of_samples()) if a.ch... |
| `adjust_samplerate()` | 7926 | Used to change the samplerate of an audio clip (for example, from 9600hz to 44100hz) |
| `mp3_to_wav()` | 8119 | This is a audio file converter that converts mp3 files to wav files. You must install 'lame' to use ... |
| `wav_to_mp3()` | 8141 | This is an audio file converter that converts wav files to mp3 files. You must install 'ffmpeg' to u... |
| `add_ipython_kernel()` | 8260 | Add the current Python interpreter as a Jupyter IPython kernel.  Parameters: - kernel_name: The name... |
| `loop_wrapper()` | 8317 | *(No description)* |
| `__init__()` | 8598 | Used for displaying and updating content in Jupyter notebooks. It's analagous to a bunch of televisi... |
| `_update()` | 8711 | Adds a new viewport from IPython.display import display, HTML display(self._converted_content, displ... |
| `clear()` | 8721 | Clears the viewports self.update(None)  def update(self, content): |
| `update()` | 8725 | Updates all viewports spawned from this channel self._update(self._convert_content(content))  def gr... |
| `grid_update()` | 8729 | Updates all viewports spawned from this channel with a grid of content Pass it like [[x0y0, x1y0, x2... |
| `row_update()` | 8737 | A row of content gets displayed self.grid_update([content_row])    _disable_display_image=False #Set... |
| `with_alpha_checkerboard()` | 8840 |  If the given image is RGBA, put a checkerboard pattern behind it and return a new opaque image  che... |
| `with_alpha_checkerboards()` | 8850 |  Plural of rp.with_alpha_checkerboard  images = detuple(images) is_numpy = is_numpy_array(images) ou... |
| `stop_autoplay_on_keypress()` | 9114 | *(No description)* |
| `block()` | 9582 | *(No description)* |
| `handler()` | 9588 | *(No description)* |
| `clf()` | 9641 | Displays a color histogram of an image using OpenCV and Matplotlib.  Args: image (str or numpy.ndarr... |
| `_minmax_indices()` | 9757 | Returns the indices with the minimum-valued elements TODO: Make this work properly with dicts, like ... |
| `min_valued_indices()` | 9766 | Returns the indices with the minimum-valued elements TODO: Make this work properly with dicts, like ... |
| `max_valued_indices()` | 9772 | Returns the indices with the maximum-valued elements TODO: Make this work properly with dicts, like ... |
| `min_valued_elements()` | 9782 |  Returns the elements with the smallest values  return gather(l,min_valued_indices(l,key=key)) def m... |
| `max_valued_elements()` | 9785 |  Returns the elements with the largest values  return gather(l,max_valued_indices(l,key=key))  def m... |
| `max_valued_index()` | 9789 | *(No description)* |
| `min_valued_index()` | 9796 | *(No description)* |
| `interp()` | 9816 | Linearly interpolates between different values with fractional indices. This is written in pure pyth... |
| `linterp()` | 9819 | Linearly interpolates between different values with fractional indices. This is written in pure pyth... |
| `matching_keys()` | 9910 | Retuns a list [x0,x1,...] such that for all xi, d[xi]=x EXAMPLE: matching_keys('a',{3:'c','q':'a',()... |
| `matching_indices()` | 9924 | Retuns a list [x0,x1,...] such that for all xi, l[xi]=x EXAMPLE: matching_indices('a',['a','b','c','... |
| `gather()` | 9946 | TODO: Add skip_missing or strict option (idk which yet but probably skip_missing if following in lin... |
| `pop_gather()` | 9964 | Uses CSE214 definition of 'pop', in the context of popping stacks. It is difficult to simultaneously... |
| `gather_vars()` | 9983 | TODO: Elaborate on frames_back = ... functionality for getting ALL frames back - we want a min_frame... |
| `is_comprehension()` | 10055 | *(No description)* |
| `bundle_vars()` | 10092 | Collect the given variables from the calling scope into an EasyDict.  This function takes any number... |
| `gather_attrs()` | 10158 |  li, si = gather_attrs(rp, 'load_image save_image')  attrs = ' '.join(attrs) attrs = attrs.split()  ... |
| `destructure()` | 10168 | Extracts values from a dictionary based on the variable names in the assignment expression in the ca... |
| `make_color()` | 10209 | *(No description)* |
| `gather_args()` | 10266 | Gathers the necessary positional arguments and keyword arguments to call the given function.  This f... |
| `f()` | 10310 | *(No description)* |
| `g()` | 10314 | *(No description)* |
| `g()` | 10318 | *(No description)* |
| `g()` | 10323 | *(No description)* |
| `g()` | 10327 | *(No description)* |
| `example_func()` | 10331 | *(No description)* |
| `maybe_add_varkw()` | 10450 | *(No description)* |
| `maybe_replace_varargs()` | 10465 | *(No description)* |
| `gather_args_call()` | 10534 | Calls the given function with arguments gathered from the current scope, using rp.gather_args Please... |
| `connect_to_database()` | 10564 | *(No description)* |
| `gather_args_wrap()` | 10594 | Decorates the given function to use arguments gathered from the current scope, using rp.gather_args ... |
| `wrapper()` | 10629 | Like gather_args_wrap, but binds the values in the namespace upon creation. Here's an example to sho... |
| `gather_args_bind()` | 10634 | Like gather_args_wrap, but binds the values in the namespace upon creation. Here's an example to sho... |
| `wrapper()` | 10728 | *(No description)* |
| `get_current_function()` | 10765 | Retrieves the function object from the specified number of frames back in the call stack.  Args: fra... |
| `g()` | 10791 | import inspect  frames_back+=1  if not isinstance(frames_back, int): raise TypeError("frames_back mu... |
| `h()` | 10792 | import inspect  frames_back+=1  if not isinstance(frames_back, int): raise TypeError("frames_back mu... |
| `get_current_function_name()` | 10841 | Enhanced Documentation:  Gets the name of the currently executing function as a string. Useful for l... |
| `gather_args_recursive_call()` | 10872 | TODO: Make this work with older versions of python, using destructure's strategy  Used to replace de... |
| `replace_if_none()` | 10877 | TODO: Make this work with older versions of python, using destructure's strategy  Used to replace de... |
| `squelch_call()` | 10997 | Calls the given function with the provided arguments and keyword arguments, suppressing specified ex... |
| `squelch_wrap()` | 11038 | Wraps a function using squelch_call (can be a decorator) squelch_wrap is to squelch_call as gather_a... |
| `wrapper()` | 11057 | Decorator to change the global environment of functions and classes to another module's namespace. I... |
| `rebind_globals_to_module()` | 11068 | Decorator to change the global environment of functions and classes to another module's namespace. I... |
| `f()` | 11088 |  assert is_a_module(module), 'rebind_globals_to_module is a decorator'  import types import functool... |
| `g()` | 11094 |  assert is_a_module(module), 'rebind_globals_to_module is a decorator'  import types import functool... |
| `decorator()` | 11104 | *(No description)* |
| `globalize_locals()` | 11143 | Decorator that makes a function's local variables available globally, allowing a function to effecti... |
| `wrapper()` | 11241 | *(No description)* |
| `trace_func()` | 11251 | Uses fzf to select a subset of a dict and returns that dict. #Refactored using GPT4 from a mess: htt... |
| `format_string()` | 11279 | *(No description)* |
| `list_to_index_dict()` | 11319 |  ['a','b','c'] ⟶ {0: 'a', 1: 'b', 2: 'c'}  return {i:v for i,v in enumerate(l)}  def invert_dict(d: ... |
| `invert_dict()` | 11323 | Inverts a dictionary, reversing the mapping of keys to values.  Args: d (dict): The dictionary to in... |
| `invert_list_to_dict()` | 11362 |  ['a','b','c'] ⟶ {'c': 2, 'a': 0, 'b': 1}  assert len(set(l)) == len(l),'r.dict_of_values_to_indices... |
| `dict_to_list()` | 11367 |  Assumes keys should be in ascending order  return gather(d,sorted(d.keys()))  def list_set(x): |
| `list_set()` | 11371 | Similar to performing list(set(x)), except that it preserves the original order of the items. You co... |
| `_get_carbon_url()` | 11503 | Generate a Carbon URL to visualize code snippets with syntax highlighting.  code : str The code to d... |
| `_muted_stdout_write()` | 12151 | *(No description)* |
| `suppress_console_output()` | 12155 | *(No description)* |
| `restore_console_output()` | 12160 | *(No description)* |
| `force_suppress_console_output()` | 12165 | *(No description)* |
| `force_restore_console_output()` | 12169 | #     #    This function formats datetimes the way I personally like to read them. # #    EXAMPLE: #... |
| `TemporarilySuppressConsoleOutput()` | 12177 | #     #    This function formats datetimes the way I personally like to read them. # #    EXAMPLE: #... |
| `_translate_timezone()` | 12334 | EXAMPLES: >>> get_current_date() ans = 2024-07-11 01:12:59.200330 >>> print(type(ans))              ... |
| `format_date()` | 12348 | EXAMPLES: >>> get_current_date() ans = 2024-07-11 01:12:59.200330 >>> print(type(ans))              ... |
| `format_current_date()` | 12416 | EXAMPLES: >>> format_current_date()#I'm in California ans = "Thu Jun 27, 2024 at 8:15:24PM" >>> form... |
| `_method_decorator_metaclass()` | 12436 | Factory that creates a metaclass applying decorator to all methods Used to make more compact and rea... |
| `__new__()` | 12442 | Originally inspired by translation funcs such as rp.is_image, rp.as_rgba_image, rp.as_rgb_image, as_... |
| `__init_subclass__()` | 12467 | *(No description)* |
| `get_form()` | 12486 | Contains functions to help translate beteen timezone data formats  human = 'EST', iana = 'America/Ne... |
| `as_form()` | 12492 | Contains functions to help translate beteen timezone data formats  human = 'EST', iana = 'America/Ne... |
| `is_form()` | 12501 | Contains functions to help translate beteen timezone data formats  human = 'EST', iana = 'America/Ne... |
| `human_to_tzinfo()` | 12536 | EXAMPLES: >>> _FilesizeFormTranslator.as_num_bytes('10mb') ans = 10485760 >>> _FilesizeFormTranslato... |
| `tzinfo_to_human()` | 12537 | EXAMPLES: >>> _FilesizeFormTranslator.as_num_bytes('10mb') ans = 10485760 >>> _FilesizeFormTranslato... |
| `is_tzinfo()` | 12542 | EXAMPLES: >>> _FilesizeFormTranslator.as_num_bytes('10mb') ans = 10485760 >>> _FilesizeFormTranslato... |
| `human_to_num_bytes()` | 12559 | EXAMPLE: >>> get_current_timezone() ans = PST |
| `num_bytes_to_human()` | 12560 | EXAMPLE: >>> get_current_timezone() ans = PST |
| `is_num_bytes()` | 12563 | EXAMPLE: >>> get_current_timezone() ans = PST |
| `get_current_timezone()` | 12569 | EXAMPLE: >>> get_current_timezone() ans = PST |
| `add()` | 12625 | Basic addition function that handles various data types and operations.  Enhanced Documentation: - U... |
| `rinsp()` | 12659 | Ryan's comprehensive object inspection tool - shows everything about any Python object.  Enhanced Do... |
| `linerino()` | 12713 | *(No description)* |
| `sorty()` | 12747 | *(No description)* |
| `color()` | 12762 | *(No description)* |
| `is_module()` | 12769 | *(No description)* |
| `is_module()` | 12789 | *(No description)* |
| `parent_class_names()` | 12918 | *(No description)* |
| `get_full_class_name()` | 12930 | *(No description)* |
| `get_parent_hierarchy()` | 12935 | *(No description)* |
| `format_parent_hierarchy()` | 12946 | *(No description)* |
| `is_dictlike()` | 12991 | *(No description)* |
| `append_stat()` | 12999 | *(No description)* |
| `format_signature()` | 13051 | *(No description)* |
| `autoformat_python_via_black()` | 13054 | *(No description)* |
| `indentify_all_but_first_line()` | 13073 | *(No description)* |
| `to_str()` | 13095 | *(No description)* |
| `_cv_initialize_cameras()` | 13193 | Prints available opencv camera properties for a given camera index EXAMPLE: >>> print_cam_info(1) CA... |
| `list_cap_props()` | 13224 | If your camera supports multiple resolutions, input the dimensions in the height and width parameter... |
| `take_photo()` | 13387 | You can count on this method having a delay (between when you call the method and when it actually s... |
| `MIDI_output()` | 13421 | Key: NOTE_OFF = [0x80, note, velocity] NOTE_ON = [0x90, note, velocity] POLYPHONIC_PRESSURE = [0xA0,... |
| `MIDI_control()` | 13473 | *(No description)* |
| `MIDI_control_precisely()` | 13475 | *(No description)* |
| `MIDI_jiggle_control()` | 13480 | *(No description)* |
| `MIDI_note_on()` | 13484 | *(No description)* |
| `MIDI_note_off()` | 13486 | *(No description)* |
| `MIDI_pitch_bend()` | 13490 | *(No description)* |
| `MIDI_all_notes_off()` | 13495 | *(No description)* |
| `MIDI_breath()` | 13498 | From: http://code.activestate.com/recipes/576653-convert-a-cmp-function-to-a-key-function/ Must use ... |
| `cmp_to_key()` | 13516 | From: http://code.activestate.com/recipes/576653-convert-a-cmp-function-to-a-key-function/ Must use ... |
| `__init__()` | 13527 | *(No description)* |
| `__lt__()` | 13528 | *(No description)* |
| `__gt__()` | 13529 | Load a Python object from a pickle file.  Enhanced Documentation: Deserializes Python objects that w... |
| `__eq__()` | 13530 | Load a Python object from a pickle file.  Enhanced Documentation: Deserializes Python objects that w... |
| `__le__()` | 13531 | Load a Python object from a pickle file.  Enhanced Documentation: Deserializes Python objects that w... |
| `__ge__()` | 13532 | Load a Python object from a pickle file.  Enhanced Documentation: Deserializes Python objects that w... |
| `__ne__()` | 13533 | Load a Python object from a pickle file.  Enhanced Documentation: Deserializes Python objects that w... |
| `sign()` | 13538 | Load a Python object from a pickle file.  Enhanced Documentation: Deserializes Python objects that w... |
| `as_easydict()` | 13909 | Converts a dictionary or dict-like object to an EasyDict for attribute-style access.  Enhanced Docum... |
| `as_easydicts()` | 13948 |  Plural of as_easydict  dictlikes = detuple(dictlikes) return [as_easydict(x) for x in dictlikes]  _... |
| `parse_yaml()` | 14342 | This is like DJSON, except for YAML TODO: Migrate this function into its own module. Look at the tes... |
| `parse_dyaml()` | 14349 | This is like DJSON, except for YAML TODO: Migrate this function into its own module. Look at the tes... |
| `__init__()` | 14364 | *(No description)* |
| `__repr__()` | 14368 | *(No description)* |
| `__iter__()` | 14375 | *(No description)* |
| `is_leaf()` | 14380 | *(No description)* |
| `handle_key_colons()` | 14387 | *(No description)* |
| `split_colon_keys()` | 14403 | *(No description)* |
| `parse_dyaml_junctions()` | 14413 | Walk the mapping, recording any duplicate keys.  deep=False mapping=JunctionList() for key_node, val... |
| `expand_comma_keys()` | 14444 | *(No description)* |
| `apply_deltas_from_junctions()` | 14464 | *(No description)* |
| `junctions_to_dict()` | 14474 | code= a: b: c: boochy b,q: c,d: creepy b: c: cri a:b: e: {"Hil":87} |
| `parse_dyaml()` | 14478 | code= a: b: c: boochy b,q: c,d: creepy b: c: cri a:b: e: {"Hil":87} |
| `test_parse_dyaml_junctions()` | 14484 | code= a: b: c: boochy b,q: c,d: creepy b: c: cri a:b: e: {"Hil":87} |
| `is_iterable()` | 14615 | Check if an object is iterable (can be looped over).  A fundamental utility function used throughout... |
| `get_my_local_ip_address()` | 14673 | EXAMPLE: >> get_my_mac_address() ans = 28:cf:e9:17:d9:a5 |
| `get_my_mac_address()` | 14684 | EXAMPLE: >> get_my_mac_address() ans = 28:cf:e9:17:d9:a5 |
| `get_default_iface_name_linux()` | 14694 | *(No description)* |
| `getmac()` | 14706 | Enhanced Documentation: Get the current public IP address visible on the internet.  This function at... |
| `get_my_public_ip_address()` | 14719 | Enhanced Documentation: Get the current public IP address visible on the internet.  This function at... |
| `deepcopy_multiply()` | 14768 | Used for multiplying lists without copying their addresses |
| `assert_equality()` | 14778 | When you have a,b,c,d and e and they're all equal and you just can't choose...when the symmetry is j... |
| `get_nested_value()` | 14796 | Needs to be better documented. ignore_errors will simply stop tunneling through the array if it gets... |
| `get_nested_attr()` | 14812 | Get a nested attribute from an object using dot notation.  Args: obj: The object to get the attribut... |
| `shell_command()` | 14905 | Execute a shell command and return its output.  Args: command (str): The shell command to execute st... |
| `get_system_commands()` | 14973 | Retrieve a list of executable commands available in the system's PATH.  The function returns a list ... |
| `_get_cached_system_commands()` | 15029 | Meant for internal use in pterm! Both kibble and autocomplete. rp.get_system_commands can take .05 s... |
| `update_sys_commands()` | 15038 | Checks if a system command exists; returns True if it does, False otherwise.  Args: command: The sys... |
| `system_command_exists()` | 15052 | Checks if a system command exists; returns True if it does, False otherwise.  Args: command: The sys... |
| `add_to_env_path()` | 15107 | Adds a directory to the system's PATH environment variable.  Appends path to $PATH using ':' for Uni... |
| `get_plt()` | 15149 | Used to be called 'dot', in-case any of my old code breaks... EXAMPLE: for theta in np.linspace(0,ta... |
| `_translate_offline()` | 15177 | This method was made private because right now it only supports russian and nearby countries lol...t... |
| `translate()` | 15199 | Returns the translation using google translate you must shortcut the language you define (French = f... |
| `translate()` | 15270 | *(No description)* |
| `sync_sorted()` | 15335 | Sorts the first list and reorders all other lists to have the same order as the sorted first list.  ... |
| `sync_sorted()` | 15378 |  # Input assertions assert key is None or callable(key) or is_iterable(key) and all(callable(x) or x... |
| `sorting_key()` | 15398 | Used as a key for sorting Example: paths=sorted(paths, key=by_number) |
| `by_number()` | 15416 | Used as a key for sorting Example: paths=sorted(paths, key=by_number) |
| `sorted_by_number()` | 15423 | In python, dicts don't necessarily retain order, though they often do. This sorts a dict's by its ke... |
| `sorted_by_len()` | 15426 | In python, dicts don't necessarily retain order, though they often do. This sorts a dict's by its ke... |
| `sorted_by_attr()` | 15429 | In python, dicts don't necessarily retain order, though they often do. This sorts a dict's by its ke... |
| `new_key()` | 15430 | In python, dicts don't necessarily retain order, though they often do. This sorts a dict's by its ke... |
| `sorted_dict()` | 15437 | In python, dicts don't necessarily retain order, though they often do. This sorts a dict's by its ke... |
| `_string_with_any()` | 15453 | *(No description)* |
| `starts_with_any()` | 15466 | Returns True if x contains any of y.  TODO: Add a return_match=False optional arg, like in starts_wi... |
| `ends_with_any()` | 15470 | Returns True if x contains any of y.  TODO: Add a return_match=False optional arg, like in starts_wi... |
| `_contains_func_y()` | 15475 | Returns True if x contains any of y.  TODO: Add a return_match=False optional arg, like in starts_wi... |
| `contains_any()` | 15485 | Returns True if x contains any of y.  TODO: Add a return_match=False optional arg, like in starts_wi... |
| `contains_all()` | 15512 | Returns True if x contains all of y.  EXAMPLES: assert contains_all('texture','t', 'e', 'x') == True... |
| `in_any()` | 15529 | Returns True if x is in any of y.  TODO: Add a return_match=False optional arg, like in starts_with_... |
| `in_all()` | 15545 | Returns True if x is in all of y.  EXAMPLES: assert in_all('tex','texture', 'textbook') == False ass... |
| `contains_sort()` | 15561 | Sorts a list of strings such that for every pair of indices i, j (i<=j), if S[i] is a substring of S... |
| `cmp()` | 15590 | Shuffles lists in sync with one another EXAMPLE: >>> sync_shuffled([1,2,3,4,5],'abcde') ans = [(1, 3... |
| `sync_shuffled()` | 15603 | Shuffles lists in sync with one another EXAMPLE: >>> sync_shuffled([1,2,3,4,5],'abcde') ans = [(1, 3... |
| `full_range()` | 15614 | *(No description)* |
| `sine_tone_sampler()` | 15641 | *(No description)* |
| `triangle_tone_sampler()` | 15648 | *(No description)* |
| `sawtooth_tone_sampler()` | 15651 | *(No description)* |
| `square_tone_sampler()` | 15658 | Has syntax highlighting. Creates a curses pocket-universe where you can edit text, and then press fn... |
| `play_tone()` | 15664 | Has syntax highlighting. Creates a curses pocket-universe where you can edit text, and then press fn... |
| `play_semitone()` | 15667 | Has syntax highlighting. Creates a curses pocket-universe where you can edit text, and then press fn... |
| `semitone_to_hz()` | 15670 | Has syntax highlighting. Creates a curses pocket-universe where you can edit text, and then press fn... |
| `play_chord()` | 15672 | Has syntax highlighting. Creates a curses pocket-universe where you can edit text, and then press fn... |
| `mini_editor()` | 15676 | Has syntax highlighting. Creates a curses pocket-universe where you can edit text, and then press fn... |
| `main()` | 15706 |  (cursesWindow, str, int, int) -> None Add a string to a curses window with given dimensions. If mod... |
| `addstr_wordwrap()` | 15712 |  (cursesWindow, str, int, int) -> None Add a string to a curses window with given dimensions. If mod... |
| `words_and_spaces()` | 15742 | >>> words_and_spaces('spam eggs ham') ['spam', ' ', 'eggs', ' ', 'ham'] |
| `get_terminal_size()` | 15891 | From http://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python/14422... |
| `ioctl_GWINSZ()` | 15925 | *(No description)* |
| `get_terminal_width()` | 15949 |  Attempts to return the width of the current TTY in characters - otherwise it will return 80 by defa... |
| `get_terminal_height()` | 15952 |  Attempts to return the height of the current TTY in characters - otherwise it will return 25 by def... |
| `is_namespaceable()` | 15956 |  Returns True if the given string can be used as a python variable name  return str.isidentifier(c) ... |
| `is_literal()` | 15968 |  If character can be used as the first of a python variable's name  return c==":" or (is_namespaceab... |
| `clip_string_width()` | 15972 |  clip to terminal size. works with multi lines at once.  max_width=(max_width or get_terminal_width(... |
| `properties_to_xml()` | 15977 | SOURCE: https://www.mkyong.com/java/how-to-store-properties-into-xml-file/ Their code was broken so ... |
| `split_including_delimiters()` | 15998 | Splits an input string, while including the delimiters in the output  Unlike str.split, we can use a... |
| `split_letters_from_digits()` | 16072 | Splits letters from numbers into a list from a string. EXAMPLE: "ads325asd234" -> ['ads', '325', 'as... |
| `split_camel_case()` | 16081 |  Split camel case names into lists. Example: camel_case_split("HelloWorld")==["Hello","World"]  from... |
| `split_python_tokens()` | 16087 | Should return a list of all the individual python tokens, INCLUDING whitespace and newlines etc When... |
| `get_all_pygments_tokens()` | 16097 | *(No description)* |
| `get_all_token_strings()` | 16100 | *(No description)* |
| `clamp()` | 16107 | Takes an exception, mutates it, then returns it Often when writing my repl, tracebacks will contain ... |
| `int_clamp()` | 16110 | Takes an exception, mutates it, then returns it Often when writing my repl, tracebacks will contain ... |
| `float_clamp()` | 16113 | Takes an exception, mutates it, then returns it Often when writing my repl, tracebacks will contain ... |
| `get_current_exception()` | 16120 | Takes an exception, mutates it, then returns it Often when writing my repl, tracebacks will contain ... |
| `pop_exception_traceback()` | 16125 | Takes an exception, mutates it, then returns it Often when writing my repl, tracebacks will contain ... |
| `get_rich_traceback_string()` | 16334 | Get the current execution frame and format it as a pretty ANSI-colored traceback string.  Args: fram... |
| `_get_stack_trace_string()` | 16353 | >>> audio_stretch([1,10],10) ans = [1,2,3,4,5,6,7,8,9,10] |
| `cartesian_to_polar()` | 16374 | Input conditions: x，y ∈ ℝ ⨁ x﹦［x₀，x₁，x₂……］⋀ y﹦［y₀，y₁，y₂……］ |
| `complex_to_polar()` | 16378 | returns: (r, ϴ) where r ≣ radius，ϴ ≣ angle and 0 ≤ ϴ < ϴ_unit. ϴ_unit﹦τ --> ϴ is in radians，ϴ_unit﹦3... |
| `riemann_sum()` | 16384 | Desmos: https://www.desmos.com/calculator/tgyr42ezjq left_to_right_sum_ratio﹦0  --> left hand sum le... |
| `riemann_mean()` | 16395 | *(No description)* |
| `fourier()` | 16398 | *(No description)* |
| `discrete_fourier()` | 16410 | *(No description)* |
| `perpendicular_bisector_function()` | 16426 | My attempt to analyze frequencies by taking the least-squares fit of a bunch of sinusoids to a signa... |
| `linear_function()` | 16429 | My attempt to analyze frequencies by taking the least-squares fit of a bunch of sinusoids to a signa... |
| `harmonic_analysis_via_least_squares()` | 16433 | My attempt to analyze frequencies by taking the least-squares fit of a bunch of sinusoids to a signa... |
| `cluster_by_key()` | 16450 | Iterable is a list of values Key is a function that takes a value from iterable and returns a hashab... |
| `cluster_by_attr()` | 16468 | Divides an iterable into chunks based on the equality of elements, as defined by the compare functio... |
| `chunk_by_attr()` | 16475 | Divides an iterable into chunks based on the equality of elements, as defined by the compare functio... |
| `chunk_by_key()` | 16482 | Divides an iterable into chunks based on the equality of elements, as defined by the compare functio... |
| `mask_clusters()` | 16565 | out=[] s=None  # start for i,val in enumerate(vec): if filter(val): if s is None: s=i elif s is not ... |
| `proportion_to_digits()` | 16591 | *(No description)* |
| `digits_to_proportion()` | 16601 | Can encode a 32-bit float into the 4 channels of an RGBA image The values should be between 0 and 1 ... |
| `is_int_literal()` | 16660 | Removes common leading indentation from a multi-line string. Similar to textwrap.dedent - but allows... |
| `is_string_literal()` | 16665 | Removes common leading indentation from a multi-line string. Similar to textwrap.dedent - but allows... |
| `indentify()` | 16673 | Removes common leading indentation from a multi-line string. Similar to textwrap.dedent - but allows... |
| `unindent()` | 16678 | Removes common leading indentation from a multi-line string. Similar to textwrap.dedent - but allows... |
| `count_leading()` | 16680 | Attempts to make multiple simultaneous string .replace() at the same time WARNING: This method is NO... |
| `lrstrip_all_lines()` | 16692 | Attempts to make multiple simultaneous string .replace() at the same time WARNING: This method is NO... |
| `search_replace_simul()` | 16697 | Attempts to make multiple simultaneous string .replace() at the same time WARNING: This method is NO... |
| `main()` | 17031 | *(No description)* |
| `get_arxiv_bibtex()` | 17059 | Gets the bibtex citation for a given arxiv paper.  OLD VERSION: https://gist.github.com/SqrtRyan/4c3... |
| `random_namespace_hash()` | 17105 | EXAMPLE: >>> random_namespace_hash(10) ans=DZC7B8GV74 |
| `random_passphrase()` | 17116 | Generates an easy-to-spell easy-to-remember passphrase  EXAMPLE: >>> for _ in range(10): print(rando... |
| `formula_as_file()` | 17182 | Uses unicode, and is black-and-white EXAMPLE: while True: display_image_in_terminal(load_image_from_... |
| `stars()` | 17201 | if isinstance(image,str): image=load_image(image) image=as_numpy_image(image,copy=False) def width(i... |
| `zoom()` | 17203 | if isinstance(image,str): image=load_image(image) image=as_numpy_image(image,copy=False) def width(i... |
| `width()` | 17221 | *(No description)* |
| `height()` | 17223 | *(No description)* |
| `_helper()` | 17281 | *(No description)* |
| `auto_canny()` | 17406 |  Takes an image, returns the canny-edges of it (a binary matrix)  pip_import('cv2') cv2=pip_import('... |
| `skeletonize()` | 17428 |  OpenCV function to return a skeletonized version of img, a Mat object cv2=pip_import('cv2') # Found... |
| `_cv_skeletonize()` | 17442 |  OpenCV function to return a skeletonized version of img, a Mat object cv2=pip_import('cv2') # Found... |
| `get_edge_drawing()` | 17465 | Alternative to Canny Edges that's more robust  Extract edges from an image using EdgeDrawing (ED) al... |
| `_get_prompt_style()` | 17592 | *(No description)* |
| `_get_cdh_back_names()` | 17604 | EXAMPLE: >>> ans = /Users/burgert/miniconda3/lib/python3.12/site-packages/rp >>> _user_path_ans(ans)... |
| `_user_path_ans()` | 17617 | EXAMPLE: >>> ans = /Users/burgert/miniconda3/lib/python3.12/site-packages/rp >>> _user_path_ans(ans)... |
| `_cdh_back_query()` | 17633 | *(No description)* |
| `matches()` | 17639 | *(No description)* |
| `_get_cd_history()` | 17683 | *(No description)* |
| `_add_to_cd_history()` | 17691 | *(No description)* |
| `unique()` | 17694 | *(No description)* |
| `task()` | 17707 | *(No description)* |
| `_update_cd_history()` | 17714 | *(No description)* |
| `_cdh_folder_is_protected()` | 17735 | *(No description)* |
| `_clean_cd_history()` | 17738 | *(No description)* |
| `set_prompt_style()` | 17746 | *(No description)* |
| `in_tokens()` | 17789 | If strict: sublist_len MUST evenly divide len(l) It will return a list of tuples, unless l is a stri... |
| `split_into_sublists()` | 17796 | If strict: sublist_len MUST evenly divide len(l) It will return a list of tuples, unless l is a stri... |
| `helper()` | 17826 | *(No description)* |
| `split_into_n_sublists()` | 17852 | Splits the input sequence `l` into `n` sublists as evenly as possible. Supports any sequence `l` tha... |
| `split_into_subdicts()` | 17893 | Splits a dictionary into a list of subdictionaries based on the specified subdict size.  If strict: ... |
| `split_into_n_subdicts()` | 17926 | Splits a dictionary into a list of n subdictionaries as evenly as possible.  Parameters: d (dict): T... |
| `join_with_separator()` | 17962 | Intersperse a separator between elements of an iterable.  Args: iterable (iterable): The iterable to... |
| `generator()` | 17994 | Returns a rotated image by angle_in_degrees, clockwise The output image size is usually not the same... |
| `_eta()` | 18292 | Example: >>> a = eta(2000,title='test') ... for i in range(2000): ...     sleep(.031) ...     a(i)  |
| `out()` | 18361 | Example: >>> a = eta(2000,title='test') ... for i in range(2000): ...     sleep(.031) ...     a(i)  ... |
| `__init__()` | 18384 | *(No description)* |
| `__call__()` | 18400 | Takes a module and returns a list of strings. Example: >>> all_submodule_names(np) ans = ['numpy.cor... |
| `__iter__()` | 18403 | Takes a module and returns a list of strings. Example: >>> all_submodule_names(np) ans = ['numpy.cor... |
| `__len__()` | 18410 | Takes a module and returns a list of strings. Example: >>> all_submodule_names(np) ans = ['numpy.cor... |
| `get_all_submodule_names()` | 18418 | Takes a module and returns a list of strings. Example: >>> all_submodule_names(np) ans = ['numpy.cor... |
| `merged_dicts()` | 18483 | Merge given dictionaries into a new dictionary or mutate the first one. The type of the resulting di... |
| `merged_prefixed_dicts()` | 18545 | Useful for destructuring from multiple dicts EXAMPLE: >>> first_output = dict(a=1,b=2,c=3) >>> secon... |
| `merged_suffixed_dicts()` | 18563 | Useful for destructuring from multiple dicts by using suffixed keys from each dictionary. EXAMPLE: >... |
| `keys_and_values_to_dict()` | 18581 | EXAMPLE: >>> keys_and_values_to_dict([1,2,3,4],['a','b','c','d']) ans = {1: 'a', 2: 'b', 3: 'c', 4: ... |
| `get_source_code()` | 18594 | EXAMPLE: >>> get_source_code(get_source_code) ans = def get_source_code(object): import inspect retu... |
| `get_source_file()` | 18609 | Might throw an exception |
| `edit()` | 18622 | *(No description)* |
| `_static_calldefs()` | 18634 | *(No description)* |
| `_get_object_lineno()` | 18640 | *(No description)* |
| `vim()` | 18669 | Open files or objects in Vim editor with intelligent path resolution.  Enhanced Documentation: Launc... |
| `is_valid_python_syntax()` | 18785 | Returns True if the code is valid python syntax, False otherwise. The 'mode' specifies the type of p... |
| `_is_valid_exeval_python_syntax()` | 18800 | Returns True if the code is valid shell syntax for your default shell. If command is specified (such... |
| `is_valid_shell_syntax()` | 18805 | Returns True if the code is valid shell syntax for your default shell. If command is specified (such... |
| `is_valid_sh_syntax()` | 18835 | Returns True if the code is valid bash syntax, False otherwise. If silent=False, will print out more... |
| `is_valid_bash_syntax()` | 18839 | Returns True if the code is valid bash syntax, False otherwise. If silent=False, will print out more... |
| `is_valid_zsh_syntax()` | 18844 | Returns True if the code is valid bash syntax, False otherwise. If silent=False, will print out more... |
| `get_default_shell()` | 18849 | Returns the path to the user's default shell. return os.environ.get('SHELL', '/bin/sh')  # Fallback ... |
| `_ipython_exeval_maker()` | 18856 | *(No description)* |
| `ipython_exeval()` | 18861 | *(No description)* |
| `__init__()` | 18877 | Validates that all directives are supported by exeval. Currently supported: %return <var namet %priv... |
| `parse()` | 18881 | Validates that all directives are supported by exeval. Currently supported: %return <var namet %priv... |
| `__str__()` | 18911 | Allows checks such as assert 'private_scope' in [_ExevalDirective('private_scope')] To make code mor... |
| `__repr__()` | 18914 | Allows checks such as assert 'private_scope' in [_ExevalDirective('private_scope')] To make code mor... |
| `__eq__()` | 18917 | Allows checks such as assert 'private_scope' in [_ExevalDirective('private_scope')] To make code mor... |
| `_parse_exeval_code()` | 18926 | Used to allow exeval to use python code with lines that start with %, called 'directives'  Directive... |
| `exeval()` | 18983 | Performs either exec(code) or eval(code) and returns the result The code will be patched into the li... |
| `multiply()` | 19053 | >>> result = exeval(code) >>> print(result) 12 |
| `_truncate_string_floats()` | 19119 | Truncate floating point numbers in a string to the specified number of significant figures. Is robus... |
| `replace()` | 19138 | Evaluate or execute within descending hierarchy of dicts merged_dict=merged_dicts(*reversed(dicts))#... |
| `_pterm_exeval()` | 19145 | Evaluate or execute within descending hierarchy of dicts merged_dict=merged_dicts(*reversed(dicts))#... |
| `trace_lines()` | 19174 | *(No description)* |
| `get_last_line_profile_results()` | 19458 | Get the results from the most recent line profiling session global _prev_line_profiler return _prev_... |
| `dec2bin()` | 19471 | Works with fractions SOURCE: http://code.activestate.com/recipes/577488-decimal-to-binary-conversion... |
| `run_until_complete()` | 19497 | *(No description)* |
| `mli()` | 19533 | *(No description)* |
| `_get_pyin_settings()` | 19642 | Get current pyin settings with smart caching try: if _globa_pyin[0] is not None: # Always read from ... |
| `_set_session_title()` | 19695 | *(No description)* |
| `do_when_ready()` | 19700 | *(No description)* |
| `_get_session_title()` | 19713 | *(No description)* |
| `_get_default_session_title()` | 19721 | *(No description)* |
| `_set_default_session_title()` | 19733 | *(No description)* |
| `_set_pterm_theme()` | 19736 | Enhanced interactive Python input with completion and features.  Enhanced Documentation: ===========... |
| `__init__()` | 19897 | TODO: - Does NOT return anything - Can be used like MiniTerminal - But should be able to accept argu... |
| `_dhistory_helper()` | 19917 | *(No description)* |
| `get_all_function_names()` | 19919 | *(No description)* |
| `_get_function_name()` | 19928 | *(No description)* |
| `__init__()` | 19978 | *(No description)* |
| `update()` | 19986 | Reload modified modules for development. Internal helper for pseudo_terminal. #Re-import any modules... |
| `__hash__()` | 20001 | Reload modified modules for development. Internal helper for pseudo_terminal. #Re-import any modules... |
| `launch_xonsh()` | 20017 | EXAMPLES: >>> with_line_numbers('a\nb\nc') ans = 0. a 1. b 2. c >>> with_line_numbers('a\nb\nc', sta... |
| `with_line_numbers()` | 20034 | EXAMPLES: >>> with_line_numbers('a\nb\nc') ans = 0. a 1. b 2. c >>> with_line_numbers('a\nb\nc', sta... |
| `number_of_lines()` | 20111 | Enhanced Documentation: Counts the number of lines in a string by counting newline characters. Uses ... |
| `read_symlink()` | 20217 | Resolves the path of a symlink up to a specified number of levels.  Args: path: Path to the symlink.... |
| `make_symlink_absolute()` | 20243 | Replace the destination of a symlink with an absolute path instead of a relative one destination_pat... |
| `make_symlink_relative()` | 20250 | Replace the destination of a symlink with a relative path instead of an absolute one destination_pat... |
| `read_symlinks()` | 20258 |  Plural of rp.read_symlink  symlink_paths = detuple(symlink_paths) if show_progress == True: show_pr... |
| `make_symlinks_relative()` | 20271 |  Plural of rp.make_symlink_relative  symlink_paths = detuple(symlink_paths) if show_progress == True... |
| `make_symlinks_absolute()` | 20284 |  Plural of rp.make_symlink_absolute  symlink_paths = detuple(symlink_paths) if show_progress == True... |
| `symlink_is_broken()` | 20297 |  Returns True if the symlink points to a path that doesn't exist  assert is_symlink(path) if not pat... |
| `make_hardlink()` | 20307 | *(No description)* |
| `replace_symlink_with_hardlink()` | 20335 | Replaces a symlink with a hardlink assert isinstance(symlink_path,str), 'replace_symlink_with_hardli... |
| `replace_symlinks_with_hardlinks()` | 20345 | Plural of replace_symlink_with_hardlink. TODO: Parallelize this (maybe with load_files), and add str... |
| `make_symlink()` | 20357 | Creates a symbolic link.  Creates a symlink at `symlink_path` pointing to `original_path`.  Args: or... |
| `is_symbolic_link()` | 20401 | Returns whether or not a given path is a symbolic link |
| `symlink_move()` | 20416 | Move a file or folder, but leave a symlink behind so that programs that try to access the original f... |
| `_guess_mimetype()` | 20428 | Check if file path points to an image file based on extension/mimetype.  Checks file extension and m... |
| `is_image_file()` | 20437 | Check if file path points to an image file based on extension/mimetype.  Checks file extension and m... |
| `is_video_file()` | 20482 | Check if a file is a video file based on MIME type detection.  Enhanced Documentation: Determines if... |
| `is_sound_file()` | 20534 | Returns True iff the file path is a UTF-8 file Faster than trying to use text_file_to_string(path), ... |
| `is_utf8_file()` | 20537 | Returns True iff the file path is a UTF-8 file Faster than trying to use text_file_to_string(path), ... |
| `get_stats_string()` | 20665 | *(No description)* |
| `is_hidden_file()` | 20666 | *(No description)* |
| `highlight_child()` | 20749 | *(No description)* |
| `__init__()` | 20756 | *(No description)* |
| `register()` | 20760 | *(No description)* |
| `summary()` | 20766 | *(No description)* |
| `walk()` | 20769 | *(No description)* |
| `_line_numbered_string()` | 20819 | *(No description)* |
| `_vimore()` | 20828 | *(No description)* |
| `localized_path()` | 20840 | *(No description)* |
| `_mv()` | 20893 | *(No description)* |
| `_absolute_path_ans()` | 20906 | *(No description)* |
| `_relative_path_ans()` | 20913 | *(No description)* |
| `_rma()` | 20923 | *(No description)* |
| `_cpah()` | 20944 | *(No description)* |
| `_get_env_info()` | 20954 | *(No description)* |
| `run()` | 20981 | Returns (return-code, stdout, stderr) p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=s... |
| `run_and_read_all()` | 20996 | Runs command using run_lambda; reads and returns entire output if rc is 0 rc, out, _ = run_lambda(co... |
| `run_and_parse_first_match()` | 21004 | Runs command using run_lambda, returns the first regex match if it exists rc, out, _ = run_lambda(co... |
| `get_nvidia_driver_version()` | 21014 | *(No description)* |
| `get_gpu_info()` | 21023 | This will return a list of libcudnn.so; it's hard to tell which one is being used if get_platform() ... |
| `get_running_cuda_version()` | 21037 | This will return a list of libcudnn.so; it's hard to tell which one is being used if get_platform() ... |
| `get_cudnn_version()` | 21041 | This will return a list of libcudnn.so; it's hard to tell which one is being used if get_platform() ... |
| `get_nvidia_smi()` | 21078 | *(No description)* |
| `get_platform()` | 21094 | *(No description)* |
| `get_mac_version()` | 21107 | *(No description)* |
| `get_windows_version()` | 21111 | *(No description)* |
| `get_lsb_version()` | 21118 | *(No description)* |
| `check_release_file()` | 21122 | *(No description)* |
| `get_os()` | 21127 | *(No description)* |
| `squelch()` | 21156 | *(No description)* |
| `get_env_info()` | 21162 | env_info_fmt =  CUDA runtime version: {cuda_runtime_version} GPU models and configuration: {nvidia_g... |
| `_ISM()` | 21252 | Input Select Multi TODO make it for things other than lists of strings, like lists of ints. To do th... |
| `_which()` | 21273 | *(No description)* |
| `update()` | 21281 | *(No description)* |
| `_whiches()` | 21293 | *(No description)* |
| `refresh()` | 21296 | View data interactively using the pyfx terminal-based data explorer.  Enhanced Documentation: ======... |
| `_ism_whiches()` | 21309 | View data interactively using the pyfx terminal-based data explorer.  Enhanced Documentation: ======... |
| `_view_with_pyfx()` | 21315 | View data interactively using the pyfx terminal-based data explorer.  Enhanced Documentation: ======... |
| `_view_json_via_jtree()` | 21378 | View JSON data in an interactive tree viewer using the jtree library.  Enhanced Documentation: This ... |
| `_get_processor_name()` | 21448 | *(No description)* |
| `_autocomplete_lss_name()` | 21571 | If there's an autocomplete thing in prompt-toolkit autocompletions thats a path return it otherwise ... |
| `_pterm_fuzzy_cd()` | 21628 | *(No description)* |
| `is_a_match()` | 21629 | *(No description)* |
| `joined_names()` | 21654 | *(No description)* |
| `_ric_current_candidate_fuzzy_matches()` | 21747 | *(No description)* |
| `get_number_of_github_gists()` | 21763 | Enhanced Documentation: Internal helper for retrieving comprehensive information about all GitHub gi... |
| `_get_all_github_gists_info()` | 21767 | Enhanced Documentation: Internal helper for retrieving comprehensive information about all GitHub gi... |
| `_pterm_cd()` | 21857 | Change directory in pseudo_terminal with history tracking. Internal helper. dir=os.path.expanduser(d... |
| `_get_function_names()` | 21939 | *(No description)* |
| `_write_default_gitignore()` | 21956 | *(No description)* |
| `_add_pterm_prefix_shortcut()` | 21979 | When using pterm, you can type commands like 'pi ' --> 'PIP install ' This lets you add custom ones ... |
| `_add_pterm_command_shortcuts()` | 21990 | EXAMPLE: |
| `_get_pterm_verbose()` | 22003 | *(No description)* |
| `__init__()` | 22009 | *(No description)* |
| `__enter__()` | 22020 | Simple context manager to temporarily disable garbage collection. Thread-safe and supports nested ca... |
| `__exit__()` | 22025 | Simple context manager to temporarily disable garbage collection. Thread-safe and supports nested ca... |
| `no_gc()` | 22035 | Simple context manager to temporarily disable garbage collection. Thread-safe and supports nested ca... |
| `level_label()` | 22171 | *(No description)* |
| `dictify()` | 22179 | *(No description)* |
| `dupdate()` | 22192 | *(No description)* |
| `scope()` | 22199 | *(No description)* |
| `equal()` | 22202 | *(No description)* |
| `__init__()` | 22238 | *(No description)* |
| `can_undo()` | 22243 | *(No description)* |
| `can_redo()` | 22246 | *(No description)* |
| `undo()` | 22249 | *(No description)* |
| `redo()` | 22254 | *(No description)* |
| `do()` | 22259 | *(No description)* |
| `do_if_new()` | 22264 | *(No description)* |
| `deep_dark_dict_copy()` | 22271 | *(No description)* |
| `get_snapshot()` | 22305 | *(No description)* |
| `set_snapshot()` | 22308 | *(No description)* |
| `take_snapshot()` | 22336 | Set the 'ans' variable in pseudo_terminal with history/snapshot support.  Enhanced Documentation: - ... |
| `get_ans()` | 22347 | Set the 'ans' variable in pseudo_terminal with history/snapshot support.  Enhanced Documentation: - ... |
| `set_ans()` | 22354 | Set the 'ans' variable in pseudo_terminal with history/snapshot support.  Enhanced Documentation: - ... |
| `eval_for_rinsp()` | 22415 | *(No description)* |
| `add_to_successful_command_history()` | 22546 | help_commands_string= <Input Modifier> MOD ON MOD OFF MOD SET SMOD SET  <Stack Traces> MORE MMORE |
| `join_command()` | 23525 | *(No description)* |
| `evaluable_part()` | 23545 | *(No description)* |
| `try_eval()` | 23549 | *(No description)* |
| `columnify_strings()` | 23681 | *(No description)* |
| `string_to_modifier()` | 24052 | *(No description)* |
| `repr_string_to_modifier()` | 24068 | *(No description)* |
| `cyan()` | 24151 | *(No description)* |
| `breakify()` | 24929 | *(No description)* |
| `get_name_from_name_error()` | 25274 | *(No description)* |
| `precache_all()` | 25758 | *(No description)* |
| `number_of_leading_spaces()` | 26208 | *(No description)* |
| `set_process_title()` | 26286 | *(No description)* |
| `get_process_title()` | 26289 | *(No description)* |
| `parenthesizer_automator()` | 26298 | *(No description)* |
| `_parenthesizer_automator()` | 26310 | *(No description)* |
| `p()` | 26314 | *(No description)* |
| `timeout()` | 26395 | *(No description)* |
| `timeout_handler()` | 26401 | Save a sequence of images as an animated PNG (APNG) file.  Enhanced Documentation: Creates animated ... |
| `battery_percentage()` | 26491 | *(No description)* |
| `battery_plugged_in()` | 26497 | path can be either a folder or a file; it will detect that for you. Implemented recursively (checks ... |
| `battery_seconds_remaining()` | 26503 | path can be either a folder or a file; it will detect that for you. Implemented recursively (checks ... |
| `total_disc_bytes()` | 26512 | path can be either a folder or a file; it will detect that for you. Implemented recursively (checks ... |
| `get_file_size()` | 26518 | *(No description)* |
| `get_folder_size()` | 26520 | Given a file size in bytes, return a string that represents how large it is in megabytes, gigabytes ... |
| `normalize_unit()` | 26657 | Normalize the unit string to ensure consistency in dictionary lookup. Converts to lowercase and chec... |
| `split_numbers_and_letters()` | 26673 | Splits a string into a number and letter part.  Parameters: input_str (str): Input string containing... |
| `get_file_size()` | 26711 | Gets the filesize of the given path Can also get the size of folders If human_readable is True, it w... |
| `num_args()` | 26786 | *(No description)* |
| `_rich_inspect()` | 26796 | Enhanced Documentation: Internal helper for pretty-printing objects using the Rich library with pagi... |
| `pretty_lines()` | 26858 | *(No description)* |
| `repr_kwargs_dict()` | 26898 | EXAMPLE: >>> x = { ...     "instance_data_root": "/root/CleanCode/Github/CogVideo/finetune/datasets/... |
| `repr_multiline()` | 26956 | Like repr for strings - except it uses multiline strings with triple quotes #TODO: Make sure it work... |
| `repr_vars()` | 26975 | Returns the string representation of specified variables. Imperfectly implemented right now. Still u... |
| `has_len()` | 27057 | Takes code and makes it suitable for using in docstrings EXAMPLE: |
| `as_example_comment()` | 27060 | Takes code and makes it suitable for using in docstrings EXAMPLE: |
| `string_transpose()` | 27087 |  >>> string_transpose("Hello\nWorld") ans = HW eo lr ll od |
| `patch()` | 27114 | Shorthand for print(line_join(args))  EXAMPLE: >>> print_lines(1,2,3,4,5) 1 2 3 4 5 |
| `all_rolls()` | 27189 | TODO: See if this is the same thing as a toeplitz matrix TODO: There might be a faster way of doing ... |
| `circular_diff()` | 27227 | Returns the diff of an array along the axis, taking into account looping unlike numpy's implementati... |
| `circular_quotient()` | 27234 | >>> circular_quotient([1,2,4,8]) ans = [2.    2.    2.    0.125] |
| `circular_convolve()` | 27241 | Convolve vector a with vector b with wrapping on the boundaries Works with any numpy dtype, and retu... |
| `circular_cross_correlate()` | 27262 | TODO let varargs input (because circular_cross_correlate is associative) Let a★b = circular_cross_co... |
| `reverse()` | 27275 | TODO extend to multiple dimenations etc. According to wikipedia, auto-correlation is defined as a ve... |
| `circular_auto_correlate()` | 27282 | TODO extend to multiple dimenations etc. According to wikipedia, auto-correlation is defined as a ve... |
| `circular_gaussian_blur()` | 27292 | >>> circ_gauss_blur([1,0,0,0,0,0]) ans = [0.4   0.095 0.005 0.005 0.095 0.4  ] >>> circ_gauss_blur([... |
| `circular_extrema_indices()` | 27307 | Return the indices of all local extrema, treating the input as cyclic (TODO: perhaps add a non-cycli... |
| `circ_diff_inverse()` | 27330 |  choose r objects from n  from functools import reduce import operator as op r = min(r, n-r) numer =... |
| `gcd()` | 27335 |  choose r objects from n  from functools import reduce import operator as op r = min(r, n-r) numer =... |
| `lcm()` | 27340 |  choose r objects from n  from functools import reduce import operator as op r = min(r, n-r) numer =... |
| `product()` | 27343 |  choose r objects from n  from functools import reduce import operator as op r = min(r, n-r) numer =... |
| `ncr()` | 27347 |  choose r objects from n  from functools import reduce import operator as op r = min(r, n-r) numer =... |
| `get_process_memory()` | 27356 | Returns the username associated with the given process ID (pid). Made by ChatGPT: https://sharegpt.c... |
| `get_process_username()` | 27366 | Returns the username associated with the given process ID (pid). Made by ChatGPT: https://sharegpt.c... |
| `get_username()` | 27385 | Get the username of the current python process |
| `get_process_id()` | 27400 |  Get the current process id, aka pid  import os return os.getpid()  def get_process_exists(pid: int)... |
| `get_process_exists()` | 27405 | *(No description)* |
| `get_process_start_date()` | 27434 | Given a process ID, returns a datetime object of when it started if pid is None: pid=get_process_id(... |
| `regex_match()` | 27589 |  returns true if the regex describes the whole string  import re return bool(re.fullmatch(regex,stri... |
| `regex_replace()` | 27593 |  Regex replacement. Example: regex_replace('from abc import def','from .* import (.*)',r'\1') == 'de... |
| `_pterm()` | 27604 |  This is what gets run when we run rp from the command line  try: pseudo_terminal(locals(),globals()... |
| `set_cursor_to_bar()` | 27616 | Modify the shape of the cursor in a vt100 terminal emulator I'm not sure what the escape codes are f... |
| `set_cursor_to_box()` | 27627 | Modify the shape of the cursor in a vt100 terminal emulator I'm not sure what the escape codes are f... |
| `set_cursor_to_underscore()` | 27638 | Modify the shape of the cursor in a vt100 terminal emulator I'm not sure what the escape codes are f... |
| `line_number()` | 27649 | Return the line number of the caller |
| `is_number()` | 27656 | returns true if x is a number Verified to work with numpy values as well as vanilla Python values Al... |
| `_refresh_autocomplete_module_list()` | 27685 | r Meant to use this command in the pseudoterminal: `print_fix\py Turn all python2 print statements (... |
| `line_join()` | 27689 | r Meant to use this command in the pseudoterminal: `print_fix\py Turn all python2 print statements (... |
| `powerset()` | 27694 | r Meant to use this command in the pseudoterminal: `print_fix\py Turn all python2 print statements (... |
| `remove_all_whitespace()` | 27719 | Works for both images AND video. Mutates the input. Works with RGBA and RGB. If grayscale image, no ... |
| `cv_bgr_rgb_swap()` | 27726 | Works for both images AND video. Mutates the input. Works with RGBA and RGB. If grayscale image, no ... |
| `mouse_callback()` | 27827 | *(No description)* |
| `_cv_helper()` | 27877 |  Used in the output of cv_find_contours - gives extra info, more than a simply numpy array  # __slot... |
| `_init_contour_class()` | 27886 |  Used in the output of cv_find_contours - gives extra info, more than a simply numpy array  # __slot... |
| `is_inner()` | 27892 | *(No description)* |
| `is_outer()` | 27900 | *(No description)* |
| `is_solid_white()` | 27904 | Contours are represented in the form [[x,y],[x,y],[x,y]]. If you want to get rid of the extra, usele... |
| `is_solid_black()` | 27908 | Contours are represented in the form [[x,y],[x,y],[x,y]]. If you want to get rid of the extra, usele... |
| `descendants()` | 27912 | Contours are represented in the form [[x,y],[x,y],[x,y]]. If you want to get rid of the extra, usele... |
| `helper()` | 27916 | Contours are represented in the form [[x,y],[x,y],[x,y]]. If you want to get rid of the extra, usele... |
| `cv_find_contours()` | 27923 | Contours are represented in the form [[x,y],[x,y],[x,y]]. If you want to get rid of the extra, usele... |
| `cv_simplify_contour()` | 27958 | Simplifies a closed contour using the Ramer-Douglas-Peucker algorithm.  Parameters: contour (numpy.n... |
| `cv_distance_to_contour()` | 27979 | Return the distance from x,y to the point on contour closest to x,y |
| `cv_closest_contour_point()` | 27987 | Return the point on contour closest to x,y EXAMPLE: cv_closest_contour_point([[1,1],[2,2],[3,3],[4,4... |
| `cv_closest_contour()` | 28002 | Return the contour with a point closest to x,y |
| `distance()` | 28008 | TODO: Important: This must somehow preserve whether the contour is closed or not?? |
| `cv_draw_contours()` | 28012 | TODO: Important: This must somehow preserve whether the contour is closed or not?? |
| `cv_draw_contour()` | 28026 | Right now rectangles are defined by two (x,y) points (start_point, end_point). They're required keyw... |
| `cv_draw_rectangle()` | 28029 | Right now rectangles are defined by two (x,y) points (start_point, end_point). They're required keyw... |
| `random_coords()` | 28044 |  color=as_rgb_float_color(color) color=float_color_to_byte_color(color)  #Input assertions: assert i... |
| `cv_contour_length()` | 28070 | *(No description)* |
| `cv_contour_area()` | 28075 | *(No description)* |
| `cv_draw_circle()` | 28090 | Draws a filled circle with center x,y on a given image. If copy=False, it *might* mutate the origina... |
| `cv_draw_circles()` | 28169 | Plural of cv_draw_circle x, y, color, antialias are all broadcastable  EXAMPLE: >>> N = 300 ... imag... |
| `cv_draw_arrow()` | 28231 | Draws an arrow from (start_x, start_y) to (end_x, end_y) on a given image. If copy=False, it *might*... |
| `cv_draw_arrows()` | 28360 | Plural of cv_draw_arrow start_x, start_y, end_x, end_y, thickness, color, rim, rim_color, tip_length... |
| `on_mouse_move()` | 28742 | *(No description)* |
| `on_mouse_down()` | 28752 | *(No description)* |
| `on_key_press()` | 28766 | *(No description)* |
| `on_mouse_move()` | 28834 | *(No description)* |
| `on_mouse_down()` | 28844 | *(No description)* |
| `on_key_press()` | 28854 | *(No description)* |
| `cosine_similarity()` | 28940 | *(No description)* |
| `fourier_descriptor()` | 28943 | *(No description)* |
| `complex_descriptors()` | 28949 | *(No description)* |
| `fourier_descriptor_distance()` | 28984 | For guidance on how to use fourier_descriptor_kwargs, see the kwargs of fourier_descriptor |
| `fourier_descriptor_similarity()` | 28991 | For guidance on how to use fourier_descriptor_kwargs, see the kwargs of fourier_descriptor |
| `cv_contour_match()` | 29000 | signal: real 1D array kernel: real 1D array signal and kernel must have same shape/length |
| `conv_circ()` | 29002 | signal: real 1D array kernel: real 1D array signal and kernel must have same shape/length |
| `complex_descriptor()` | 29010 | *(No description)* |
| `ryan_match()` | 29037 | *(No description)* |
| `cv_best_match_contour()` | 29072 | Find the best matching contour from a collection of contours.  Given a target contour and a list of ... |
| `cv_best_match_contours()` | 29106 | Find the n best matching contours from a collection of contours.  Given a target contour and a list ... |
| `_cv_morphological_helper()` | 29144 | Used for erosion, dilation, and other functions. Please see the documentation if you'd like to know ... |
| `cv_dilate()` | 29172 | Dilates image with a box kernel. Runs very quickly because it takes two orthoganal 1-d passes. TODO ... |
| `cv_gauss_blur()` | 29180 | Gauss blur an image with the given radius using opencv  The alpha_weighted option: cv_gauss_blur blu... |
| `is_opaque_image()` | 29225 | If there is a single transparent pixel in the image, return false Equivalent to the slower: return (... |
| `is_transparent_image()` | 29243 | If there is a single transparent pixel in the image, return True Equivalent to the slower: return (a... |
| `loop_direction_2d()` | 29286 | loop is like [(x,y),(x,y)...] Given a list of 2d points, return a negative number if they're clockwi... |
| `is_clockwise()` | 29299 |  loop is like [(x,y),(x,y)...] (two dimensions)  return loop_direction_2d(loop)<0 def is_counter_clo... |
| `is_counter_clockwise()` | 29302 |  loop is like [(x,y),(x,y)...] (two dimensions)  return loop_direction_2d(loop)>0 def cv_make_clockw... |
| `cv_make_clockwise()` | 29305 | Parameters: x and y: There are three ways to give this function points: - One is by specifying x and... |
| `line_split()` | 29353 | I find myself often wishing this function exists for a few seconds before remembering String.splitli... |
| `line_join()` | 29388 |  EXAMPLE: line_join(['hello','world'])=='hello\nworld'  Enhanced Documentation: Joins strings/object... |
| `append_uniform_row()` | 29426 | Adds a row to the bottom of a matrix with a constant value equal to scalar Example: append_uniform_r... |
| `append_zeros_row()` | 29435 | Adds a row of zeros to the bottom of a matrix Example: append_zeros_row([[1,2,3],[4,5,6],[7,8,9]])  ... |
| `append_ones_row()` | 29443 | Adds a row of ones to the bottom of a matrix Example: append_zeros_row([[1,2,3],[4,5,6],[7,8,9]])   ... |
| `append_uniform_column()` | 29452 | Adds a column to the bottom of a matrix with a constant value equal to scalar Example: append_unifor... |
| `append_zeros_column()` | 29461 | Adds a column of zeros to the bottom of a matrix Example: append_zeros_column([[1,2,3],[4,5,6],[7,8,... |
| `append_ones_column()` | 29469 | #Adds a column of ones to the bottom of a matrix #Example: append_zeros_column([[1,2,3],[4,5,6],[7,8... |
| `squared_euclidean_distance()` | 29480 | This function exists so you don't have to use euclidean_distance then square it (which is both ineff... |
| `euclidean_distance()` | 29491 | from_point and to_point are like (x0,y0,...) or [x0,y0,z0,...], or some numpy equivalent Example:   ... |
| `differential_euclidean_distances()` | 29498 | Sequential distances between points, like np.diff except returns a single vector and has options lik... |
| `cumulative_euclidean_distances()` | 29509 | If loop is true, as also add the distance from the last point to the first point at the end (one ext... |
| `evenly_split_path()` | 29520 | Path is a list of points. Can be any number of dimensions. The euclidean distance from each point to... |
| `is_complex_vector()` | 29559 |  Return True iff x is like [1+2j,3+4j,5+6j,...]  x=np.asarray(x) if not len(x):return True#Vaccuous ... |
| `is_points_array()` | 29564 |  Return True iff x is like [[1,2],[3,4],[5,6],...]  x=np.asarray(x) if not len(x):return True#Vaccuo... |
| `is_cv_contour()` | 29569 |  Return True iff x is like [[[1,2]],[[3,4]],[[5,6]],...] and dtype=np.int32  x=np.asarray(x)#TODO th... |
| `_points_array_to_complex_vector()` | 29576 | *(No description)* |
| `_points_array_to_cv_contour()` | 29581 | *(No description)* |
| `_complex_vector_to_points_array()` | 29586 |  Automatically convert path path data  if isinstance(path,set) or isinstance(path,dict):path=list(pa... |
| `_complex_vector_to_cv_contour()` | 29591 |  Automatically convert path path data  if isinstance(path,set) or isinstance(path,dict):path=list(pa... |
| `_cv_contour_to_points_array()` | 29596 |  Automatically convert path path data  if isinstance(path,set) or isinstance(path,dict):path=list(pa... |
| `_cv_contour_to_complex_vector()` | 29599 |  Automatically convert path path data  if isinstance(path,set) or isinstance(path,dict):path=list(pa... |
| `as_complex_vector()` | 29604 |  Automatically convert path path data  if isinstance(path,set) or isinstance(path,dict):path=list(pa... |
| `as_points_array()` | 29611 |  Automatically convert path data  if isinstance(path,set) or isinstance(path,dict):path=list(path) i... |
| `as_cv_contour()` | 29618 |  Automatically convert path data  if isinstance(path,set) or isinstance(path,dict):path=list(path) i... |
| `closest_points()` | 29712 | if to_points is None, it defaults to from_points (returning a symmetric matrix) This function was or... |
| `least_squares_euclidean_affine()` | 29730 | TODO: Inspect this function! Is it right?!?!? It seems to follow This function is strictly limited t... |
| `least_squares_affine()` | 29816 | TODO Clean this function up and make it more like least_squares_euclidean_affine from_points and to_... |
| `translation_affine()` | 29844 | EXAMPLE: CODE: translation_affine([20,30]) RESULT: [[ 1.  0. 20.] [ 0.  1. 30.]] |
| `rotation_affine_2d()` | 29855 | EXAMPLE: CODE: rotation_affine_2d(90,out_of=360) RESULT: [[ 0. -1.  0.] [ 1.  0.  0.]] EXAMPLE: CODE... |
| `inverse_affine()` | 29881 | QUICK AND DIRTY EXAMPLE: >>> A ans = [[11. 62. 90.] [29.  9. 98.]] >>> apply_affine([[2,4],[5,6],[7,... |
| `identity_affine()` | 29900 | EXAMPLE: CODE: identity_affine(2) RESULT: [[1. 0. 0.] [0. 1. 0.]] EXAMPLE: CODE: identity_affine(3) ... |
| `combined_affine()` | 29918 | Return the affine matrix needed to apply all matrices in 'affines' in the order they were given TODO... |
| `apply_affine()` | 29954 | This function applies a given affine transform (specified as a matrix) to a list of points and retur... |
| `icp_least_squares_euclidean_affine()` | 29971 | icp stands for "iterative closest point". It's an algorithm used to match point-clouds. The length o... |
| `point_cloud_angle()` | 29992 | *(No description)* |
| `is_euclidean_affine_matrix()` | 30062 | mx+b in the complex plane corresponds to a euclidean transform This function takes a euclidean affin... |
| `is_affine_matrix()` | 30067 | mx+b in the complex plane corresponds to a euclidean transform This function takes a euclidean affin... |
| `euclidean_affine_to_complex_linear_coeffs()` | 30070 | mx+b in the complex plane corresponds to a euclidean transform This function takes a euclidean affin... |
| `complex_linear_coeffs_to_euclidean_affine()` | 30088 | This is the inverse of euclidean_affine_to_complex_linear_coeffs Where F=complex_linear_coeffs_to_eu... |
| `__init__()` | 30105 | A dict that can use more than just normal keys by using handyhash This class might get more methods ... |
| `__hash__()` | 30108 | A dict that can use more than just normal keys by using handyhash This class might get more methods ... |
| `__eq__()` | 30110 | A dict that can use more than just normal keys by using handyhash This class might get more methods ... |
| `__repr__()` | 30117 | A dict that can use more than just normal keys by using handyhash This class might get more methods ... |
| `__init__()` | 30125 | *(No description)* |
| `__setitem__()` | 30127 | *(No description)* |
| `__delitem__()` | 30129 | *(No description)* |
| `__getitem__()` | 30131 | *(No description)* |
| `__iter__()` | 30133 | This function is really handy! Meant for hashing things that can't normally be hashed, like lists an... |
| `__contains__()` | 30135 | This function is really handy! Meant for hashing things that can't normally be hashed, like lists an... |
| `handy_hash()` | 30151 | This function is really handy! Meant for hashing things that can't normally be hashed, like lists an... |
| `fallback()` | 30160 | *(No description)* |
| `_set_hash()` | 30185 | *(No description)* |
| `_dict_hash()` | 30190 | *(No description)* |
| `_list_hash()` | 30198 | Return the hashed input that would be passed to 'function', using handy_hash. This function is used ... |
| `_tuple_hash()` | 30203 | Return the hashed input that would be passed to 'function', using handy_hash. This function is used ... |
| `_slice_hash()` | 30208 | Return the hashed input that would be passed to 'function', using handy_hash. This function is used ... |
| `args_hash()` | 30216 | Return the hashed input that would be passed to 'function', using handy_hash. This function is used ... |
| `memoized()` | 30296 | TODO: Make this function smarter - use the same arg techniques as in gather_args, so even when we gi... |
| `memoized_function()` | 30310 | This method is meant to be used as a substitute for @property Often, when using @property you'll see... |
| `memoized_property()` | 30320 | This method is meant to be used as a substitute for @property Often, when using @property you'll see... |
| `thing()` | 30326 | assert callable(method) property_name='_'+method.__name__ def memoized_property(self): if not hasatt... |
| `thing()` | 30337 | assert callable(method) property_name='_'+method.__name__ def memoized_property(self): if not hasatt... |
| `memoized_property()` | 30343 |  gif and webp and png can be either a video or image depending on context...  video = load_video(pat... |
| `decorator()` | 30545 | *(No description)* |
| `wrapper()` | 30547 | *(No description)* |
| `clear_cache()` | 30557 | Descriptor (used as a decorator) that creates class-level 'properties' in Python.  This class is a w... |
| `class_data()` | 30587 | def __init__(self, getter): self.getter = getter  def __get__(self, instance, owner): return self.ge... |
| `class_data()` | 30597 | def __init__(self, getter): self.getter = getter  def __get__(self, instance, owner): return self.ge... |
| `__init__()` | 30602 | TODO: Make this function smarter - use the same arg techniques as in gather_args, so even when we gi... |
| `__get__()` | 30605 | TODO: Make this function smarter - use the same arg techniques as in gather_args, so even when we gi... |
| `__init__()` | 30640 | *(No description)* |
| `__init__()` | 30657 | *(No description)* |
| `__init__()` | 30679 | *(No description)* |
| `__init__()` | 30699 | *(No description)* |
| `__new__()` | 30739 | Create a new instance or return an existing one from the cache based on the arguments.  Args: cls (T... |
| `new_init()` | 30772 | Restore the original __init__ method. cls.__init__ = old_init  # Restore the original __init__ metho... |
| `instance_cache()` | 30781 | Return the cache dictionary for instances of the derived class.  Returns: HandyDict: A HandyDict obj... |
| `_get_hash()` | 30804 | Helper function to calculate a hash of the provided data or file contents.  :param source: The data ... |
| `get_md5_hash()` | 30864 | Calculate the MD5 hash of the provided data or the contents of a file specified by its path. It is b... |
| `get_sha256_hash()` | 30891 | Calculate the SHA-256 hash of the provided data or the contents of a file specified by its path. It ... |
| `as_rgba_float_color()` | 31422 | TODO: use this all over RP!  EXAMPLE:  >>> as_rgba_float_color(1) ans = (1, 1, 1, 1) >>> as_rgba_flo... |
| `as_rgb_float_color()` | 31691 |  The RGB counterpart to as_rgba_float_color. See rp.as_rgba_float_color for full documentation!  ret... |
| `as_rgba_float_colors()` | 31696 | *(No description)* |
| `as_rgb_float_colors()` | 31699 | *(No description)* |
| `_get_font_path()` | 31714 | *(No description)* |
| `get_font_supported_chars()` | 31747 | Get supported characters of a given font  EXAMPLE:  >>> font = '/Users/ryan/Library/Fonts/Ubuntu Mon... |
| `_parse_origin_to_pixels()` | 32239 | Converts a proportional or named origin into pixel coordinates. if origin is None: return (0.0, 0.0)... |
| `get_urls()` | 32456 | Parses the css file and retrieves the font urls. Parameters: content (string): The data which needs ... |
| `fetch_data()` | 32482 | Downloads the font files from the `urls` list. Parameters: urls (list): List of urls from which the ... |
| `main()` | 32510 | Main Function for the app. Parameters: method (string): Add link if the `src` is a HTTP/HTTPS link. ... |
| `get_downloaded_fonts()` | 32613 |  Returns a list of font files downloaded by rp  def get(x): try: return _get_all_paths_fast( x, recu... |
| `get()` | 32615 | *(No description)* |
| `_get_file_path()` | 32747 | If given a url, get a file path that can be used for things #TODO: Use this to make strip_file_exten... |
| `get_file_extension()` | 32773 | 'x.png'        --> 'png' 'text.txt'     --> 'txt' 'text'         --> '' 'text.jpg.txt' --> 'txt' 'a/... |
| `get_file_extensions()` | 32813 | Replaces or adds a file extension to a path  If extension is blank, and replace=False, path won't be... |
| `get_path_name()` | 32954 | '/tmp/d/a.dat' --> 'a.dat' For more, see: https://stackoverflow.com/questions/8384737/extract-file-n... |
| `get_path_names()` | 32966 | Take an absolute path, and turn it into a relative path starting from root_directory root_directory'... |
| `get_relative_path()` | 32971 | Take an absolute path, and turn it into a relative path starting from root_directory root_directory'... |
| `get_relative_paths()` | 33037 | Plural of get_relative_path Supports broadcasting (see examples) - it can take multiple paths and/or... |
| `get_absolute_path()` | 33085 | Given a relative path, return its absolute path If physical, expand all symlinks in the path  Enhanc... |
| `_detuple_paths()` | 33132 | Enhanced Documentation: Checks whether a file path has any file extension.  Args: file_path (str): P... |
| `get_absolute_paths()` | 33138 | Enhanced Documentation: Checks whether a file path has any file extension.  Args: file_path (str): P... |
| `has_file_extension()` | 33142 | Enhanced Documentation: Checks whether a file path has any file extension.  Args: file_path (str): P... |
| `date_modified()` | 33172 |  Get the date a path was modified  timestamp=os.path.getmtime(path)#Measured in seconds import datet... |
| `date_created()` | 33178 |  Get the date a path was created  timestamp=os.path.getctime(path)#Measured in seconds import dateti... |
| `date_accessed()` | 33184 |  Get the date a path was accessed  timestamp=os.path.getatime(path)#Measured in seconds import datet... |
| `get_all_paths()` | 33190 | Get all file and/or directory paths in a directory with extensive filtering and sorting options.  En... |
| `recursion_helper()` | 33335 | *(No description)* |
| `is_hidden()` | 33411 | *(No description)* |
| `get_all_files()` | 33442 |  Like get_all_files, but only returns image files. This function is just sugar.   #TODO: Once get_al... |
| `get_all_image_files()` | 33445 |  Like get_all_files, but only returns image files. This function is just sugar.   #TODO: Once get_al... |
| `get_all_runnable_python_files()` | 33459 | Retrieve all runnable Python files from a specified folder.  A runnable Python file is defined as a ... |
| `_has_if_name_main()` | 33501 | *(No description)* |
| `get_all_folders()` | 33530 |  Take a folder, and return a list of all of its subfolders  assert folder_exists(folder),'Folder '+r... |
| `get_subfolders()` | 33535 |  Take a folder, and return a list of all of its subfolders  assert folder_exists(folder),'Folder '+r... |
| `folder_is_empty()` | 33555 | Determines whether a folder is empty or not.  This function uses os.scandir() to iterate over the co... |
| `get_random_file()` | 33601 | Returns the paths of random files in that folder If the folder is None, returns the name of a random... |
| `get_random_files()` | 33612 | Returns the paths of random files in that folder If the folder is None, returns the name of a random... |
| `get_random_folders()` | 33636 | Get a single random folder from the specified directory.  Enhanced Documentation: Utility function f... |
| `get_random_folder()` | 33643 | Get a single random folder from the specified directory.  Enhanced Documentation: Utility function f... |
| `_has_globbing_characters()` | 33685 | Check if a pattern string contains any of the special globbing characters used by Python's glob modu... |
| `rp_iglob()` | 33708 | Generator that recursively yields file paths based on glob-like patterns, multi-line strings, or ite... |
| `rp_glob()` | 33805 |  See rp_iglob's docstring  return list(rp_iglob(*args,**kwargs))    def fractional_integral_in_frequ... |
| `fractional_integral_in_frequency_domain()` | 33811 | WARNING: Make sure to use the right kind of fft (np.fft.rfft vs np.fft.fft) This function integrates... |
| `__init__()` | 33865 | *(No description)* |
| `_settings_hash()` | 33883 | *(No description)* |
| `__getitem__()` | 33887 | *(No description)* |
| `__setitem__()` | 33926 | *(No description)* |
| `__len__()` | 33932 | Match multiple vectors to points in a FlannDict and return the results in sorted order of distance a... |
| `__iter__()` | 33935 | Match multiple vectors to points in a FlannDict and return the results in sorted order of distance a... |
| `_keyify()` | 33937 | Match multiple vectors to points in a FlannDict and return the results in sorted order of distance a... |
| `best_flann_dict_matches()` | 33950 | Match multiple vectors to points in a FlannDict and return the results in sorted order of distance a... |
| `__init__()` | 33960 |  assert isinstance(flann_dict,FlannDict) assert callable(query_to_vector) assert n is None or n>=0 i... |
| `__repr__()` | 33961 |  assert isinstance(flann_dict,FlannDict) assert callable(query_to_vector) assert n is None or n>=0 i... |
| `knn_clusters()` | 33994 | Given a list of vectors, return a list of sets of vectors belonging to each cluster resulting from t... |
| `test()` | 33999 |  spatial_dict=spatial_dict()#If you want to override the default FlannDict paramers, pass a lambda t... |
| `neighbors()` | 34026 | Stands for Ryan-Transform. Used for path matching in my 2019 Zebra summer internship. Removes transl... |
| `helper()` | 34029 | Stands for Ryan-Transform. Used for path matching in my 2019 Zebra summer internship. Removes transl... |
| `heightify()` | 34090 | *(No description)* |
| `least_squares_regression_line_coeffs()` | 34333 | Computes the coefficients for a least squares regression line.  Parameters: - X: List of x-values, l... |
| `magnitude()` | 34404 | *(No description)* |
| `normalized()` | 34408 | *(No description)* |
| `_get_javascript_runtime()` | 34414 | *(No description)* |
| `javascript()` | 34421 | *(No description)* |
| `javascript_console()` | 34427 | *(No description)* |
| `_get_byte_to_binary_grayscale_image_floyd_steinburg_dithering_function()` | 34432 | *(No description)* |
| `minmax()` | 34440 | *(No description)* |
| `dithering_gray()` | 34448 | *(No description)* |
| `_binary_floyd_steinburg_dithering()` | 34488 | Takes an image and returns a dithered binary image I chose not to expose this method right now outsi... |
| `is_image()` | 34513 | An image must be either grayscale (a numpy matrix), rgb (a HWC tensor), or rgba (a HWC tensor) and h... |
| `is_grayscale_image()` | 34541 | Check if image is grayscale (2D array with shape HW).  Returns True for 2-dimensional numpy arrays o... |
| `is_rgb_image()` | 34590 | Check if image is RGB (3D array with shape HW3).  Returns True for arrays with exactly 3 color chann... |
| `is_rgba_image()` | 34642 | Check if image is RGBA (3D array with shape HW4).  Returns True for arrays with exactly 4 channels (... |
| `as_grayscale_image()` | 34727 |  Returns a 2-dimensional numpy array in HW form (height, width)  assert is_image(image),'Error: inpu... |
| `as_rgb_image()` | 34735 |  Returns a 3-dimensional numpy array in HW3 form (height, width, channels)  Enhanced Documentation: ... |
| `as_rgba_image()` | 34777 |  Returns a 3-dimensional numpy array in HW4 form (height, width, channels)  assert is_image(image),'... |
| `is_float_image()` | 34786 | A float image is made with floating-point real values between 0 and 1 https://stackoverflow.com/ques... |
| `is_byte_image()` | 34822 | A byte image is made of unsigned bytes (aka np.uint8) Return true if the datatype is an integer betw... |
| `is_binary_image()` | 34867 | A binary image is made of boolean values (AKA true or false)  Enhanced Documentation: - Used for spe... |
| `as_float_image()` | 34912 |  Returns a numpy array with floating point values (usually between 0 and 1)  Enhanced Documentation:... |
| `as_byte_image()` | 34948 |  Returns a numpy array with dtype np.uint8  Enhanced Documentation:  Converts images to byte format ... |
| `as_binary_image()` | 34994 | Returns a nummpy array with dtype bool EXAMPLE of 'dither': while True: display_image(as_binary_imag... |
| `as_grayscale_images()` | 35141 | Convert list of images to grayscale. See as_grayscale_image for single images. return _images_conver... |
| `random_rgb_byte_color()` | 35165 | *(No description)* |
| `random_rgba_byte_color()` | 35167 | *(No description)* |
| `random_grayscale_byte_color()` | 35169 | *(No description)* |
| `random_rgb_float_color()` | 35172 | *(No description)* |
| `random_rgba_float_color()` | 35174 | *(No description)* |
| `random_grayscale_float_color()` | 35176 | *(No description)* |
| `random_rgb_binary_color()` | 35179 | *(No description)* |
| `random_rgba_binary_color()` | 35181 | *(No description)* |
| `random_grayscale_binary_color()` | 35183 | *(No description)* |
| `random_hex_color()` | 35186 | *(No description)* |
| `random_rgb_byte_colors()` | 35191 | *(No description)* |
| `random_rgba_byte_colors()` | 35193 | *(No description)* |
| `random_grayscale_byte_colors()` | 35195 | *(No description)* |
| `random_rgb_float_colors()` | 35198 | Check if input represents a color value (any numeric format).  General-purpose color validation that... |
| `random_rgba_float_colors()` | 35200 | Check if input represents a color value (any numeric format).  General-purpose color validation that... |
| `random_grayscale_float_colors()` | 35202 | Check if input represents a color value (any numeric format).  General-purpose color validation that... |
| `random_rgb_binary_colors()` | 35205 | Check if input represents a color value (any numeric format).  General-purpose color validation that... |
| `random_rgba_binary_colors()` | 35207 | Check if input represents a color value (any numeric format).  General-purpose color validation that... |
| `random_grayscale_binary_colors()` | 35209 | Check if input represents a color value (any numeric format).  General-purpose color validation that... |
| `random_hex_colors()` | 35212 | Check if input represents a color value (any numeric format).  General-purpose color validation that... |
| `is_color()` | 35216 | Check if input represents a color value (any numeric format).  General-purpose color validation that... |
| `is_binary_color()` | 35259 | Check if input represents a binary color value (boolean values).  Validates that input is an iterabl... |
| `is_byte_color()` | 35301 | Check if input represents a byte/integer color value.  Validates that input is an iterable containin... |
| `is_float_color()` | 35339 | Check if input represents a floating-point color value.  Validates that input is an iterable contain... |
| `hex_color_to_byte_color()` | 35379 | EXAMPLE: >>> hex_color_to_byte_color('#007FFF') ans = (0, 127, 255) |
| `hex_color_to_float_color()` | 35394 | EXAMPLE: >>> hex_color_to_byte_color('#007FFF') ans = (0, .5, 1) |
| `byte_color_to_hex_color()` | 35403 | EXAMPLE: >>> byte_color_to_hex_color((0,255,127)) ans = #00FF7F |
| `byte_color_to_float_color()` | 35416 | Enhanced Documentation:  Converts float color values (0.0-1.0) to byte color values (0-255).  Args: ... |
| `float_color_to_byte_color()` | 35419 | Enhanced Documentation:  Converts float color values (0.0-1.0) to byte color values (0-255).  Args: ... |
| `float_color_to_hex_color()` | 35446 | Enhanced Documentation:  Converts float color values to hex color string representation.  Args: floa... |
| `float_color_to_byte_color()` | 35468 | Convert multiple hex color strings to byte color tuples. Plural version of hex_color_to_byte_color. ... |
| `float_colors_to_byte_colors()` | 35471 | Convert multiple hex color strings to byte color tuples. Plural version of hex_color_to_byte_color. ... |
| `float_colors_to_hex_colors()` | 35474 | Convert multiple hex color strings to byte color tuples. Plural version of hex_color_to_byte_color. ... |
| `byte_colors_to_hex_colors()` | 35477 | Convert multiple hex color strings to byte color tuples. Plural version of hex_color_to_byte_color. ... |
| `byte_colors_to_float_colors()` | 35480 | Convert multiple hex color strings to byte color tuples. Plural version of hex_color_to_byte_color. ... |
| `hex_colors_to_byte_colors()` | 35483 | Convert multiple hex color strings to byte color tuples. Plural version of hex_color_to_byte_color. ... |
| `hex_colors_to_float_colors()` | 35519 | *(No description)* |
| `_altbw()` | 35525 | *(No description)* |
| `_get_rp_color()` | 35567 | Allows mixing of colors, like "blue green", "dark gray" and "light light red" "lightred" is equivale... |
| `color_name_to_float_color()` | 35618 | Given a color name, this function returns an RGB float color EXAMPLE: assert color_name_to_float_col... |
| `color_name_to_byte_color()` | 35652 | *(No description)* |
| `color_name_to_hex_color()` | 35655 | *(No description)* |
| `get_color_hue()` | 35658 |  Return (height,width) of an image  Enhanced Documentation: Gets the dimensions (height, width) of a... |
| `get_color_saturation()` | 35664 |  Return (height,width) of an image  Enhanced Documentation: Gets the dimensions (height, width) of a... |
| `get_color_brightness()` | 35670 |  Return (height,width) of an image  Enhanced Documentation: Gets the dimensions (height, width) of a... |
| `get_image_dimensions()` | 35676 |  Return (height,width) of an image  Enhanced Documentation: Gets the dimensions (height, width) of a... |
| `get_image_height()` | 35731 | Return the image's height measured in pixels  Enhanced Documentation: Gets the height of an image in... |
| `get_image_width()` | 35765 | Return the image's width measured in pixels  Enhanced Documentation: Gets the width of an image in p... |
| `get_video_height()` | 35799 | Get height of video from different formats (THWC NumPy, TCHW torch, or sequence of images).  Example... |
| `get_video_heights()` | 35818 | Get heights from multiple videos. Plural version of get_video_height.  Enhanced Documentation: Appli... |
| `get_video_width()` | 35853 | Get width of video from different formats (THWC NumPy, TCHW torch, or sequence of images).  Examples... |
| `get_video_widths()` | 35872 | Get widths from multiple videos. Plural version of get_video_width.  Enhanced Documentation: Applies... |
| `running_in_ipython()` | 35912 | Overwrite this when subclassing base64_image = rp.encode_image_to_base64(image) return '<img src="da... |
| `__init__()` | 35923 | Overwrite this when subclassing base64_image = rp.encode_image_to_base64(image) return '<img src="da... |
| `_get_html()` | 35929 | Overwrite this when subclassing base64_image = rp.encode_image_to_base64(image) return '<img src="da... |
| `_init_update()` | 35934 | Overwrite this when subclassing self.update(rp.cv_text_to_image(self._display_id, color=rp.random_rg... |
| `update()` | 35944 | Updates the viewport from IPython.display import update_display self._html = HTML(self._get_html(ima... |
| `get_notebook_name()` | 35951 | Assumes we're running in a Jupyter notebook Returns the name of the notebook By default, does not in... |
| `get_notebook_path()` | 35966 | Assumes we're running in a Jupyter notebook Returns an absolute path of the notebook file EXAMPLE: g... |
| `running_in_google_colab()` | 36023 | Return true iff this function is called from google colab |
| `get_cloud_provider()` | 36031 |  WARNING: This can be slow if there's actually no cloud! Like, on a laptop, this can take a while...... |
| `running_in_gcp()` | 36037 | Returns True iff this Python session was started over SSH https://stackoverflow.com/questions/353529... |
| `_is_python_exe_root()` | 36041 | Returns True iff this Python session was started over SSH https://stackoverflow.com/questions/353529... |
| `running_in_ssh()` | 36048 | Returns True iff this Python session was started over SSH https://stackoverflow.com/questions/353529... |
| `running_in_mamba()` | 36055 | *(No description)* |
| `running_in_conda()` | 36059 | *(No description)* |
| `running_in_venv()` | 36067 | *(No description)* |
| `get_conda_name()` | 36075 | Checks if the current process is running inside a tmux session. return 'TMUX' in os.environ  def run... |
| `get_venv_name()` | 36084 | Checks if the current process is running inside a tmux session. return 'TMUX' in os.environ  def run... |
| `running_in_tmux()` | 36093 | Checks if the current process is running inside a tmux session. return 'TMUX' in os.environ  def run... |
| `running_in_docker()` | 36097 | Returns True if we're in docker, False otherwise #https://stackoverflow.com/questions/43878953/how-d... |
| `f()` | 36153 | *(No description)* |
| `get_principle_components()` | 36302 | Returns orthogonal, normalized, sorted-by-eigenvalue-in-descending-order principle components (retai... |
| `demo()` | 36308 | cv2=pip_import('cv2')  tensors=np.asarray(tensors) number_of_tensors=len(tensors) tensor_shape=tenso... |
| `cv_box_blur()` | 36346 | A box blur using opencv. Width and height override diameter. See cv_gauss_blur for examples of alpha... |
| `_highlighted_query_results()` | 36412 | Case insensitive fansi-highlighting of a query in a string Example: print(_highlighted_query_results... |
| `_rinsp_search_helper()` | 36425 | Enhanced Documentation: Internal helper for recursively searching object attributes and nested struc... |
| `match()` | 36460 | *(No description)* |
| `keys()` | 36465 | *(No description)* |
| `get()` | 36473 | *(No description)* |
| `helper()` | 36483 | THIS IS A WORK IN PROGRESS example: trying to find the conv function in torch? Maybe it's nested in ... |
| `rinsp_search()` | 36495 | THIS IS A WORK IN PROGRESS example: trying to find the conv function in torch? Maybe it's nested in ... |
| `as_numpy_array()` | 36579 | Will convert x into type np.ndarray This should convert anything that can be converted into a numpy ... |
| `is_valid_integer_string()` | 36684 | *(No description)* |
| `on_fail()` | 36691 | *(No description)* |
| `condition()` | 36759 | string_pager(More options: - Enter 'p' to use rp.string_pager() to view your choices (this is useful... |
| `_stringify()` | 36862 | *(No description)* |
| `get_youtube_video_url()` | 36888 | Gets the url of a youtube video, given either the url (in which case nothing changes) or its id  Exa... |
| `_is_youtube_video_url()` | 36905 | Returns the captions/subtitles for a YouTube video based on the given URL or video ID.  NOTE: If it ... |
| `get_youtube_video_transcript()` | 36909 | Returns the captions/subtitles for a YouTube video based on the given URL or video ID.  NOTE: If it ... |
| `_get_youtube_video_data_via_embeddify()` | 37095 | See https://pypi.org/project/embeddify/ Uses a specification called 'oembed', which lets us get info... |
| `get_youtube_video_title()` | 37111 | Returns the title of a youtube video, given either its url or video id  Example: >>> get_youtube_vid... |
| `get_youtube_video_thumbnail()` | 37124 | Returns the thumbnail of a youtube video, either as a url or an image EXAMPLE: >>> display_image(get... |
| `_get_video_file_duration_via_moviepy()` | 37162 | Returns the duration of a video file, in seconds https://stackoverflow.com/questions/3844430/how-to-... |
| `get_video_file_duration()` | 37170 |  Returns a float, representing the total video length in seconds  path=get_absolute_path(path) #This... |
| `_get_video_file_framerate_via_moviepy()` | 37180 |  Given a (str) path to a video file, returns a number (framerate)  path = get_absolute_path(path) #I... |
| `_get_video_file_framerate_via_ffprobe()` | 37192 | Slower than _get_video_file_framerate_via_moviepy but no extra python dependencies Given a (str) pat... |
| `get_video_file_framerate()` | 37228 |  Given a (str) path to a video file, returns a number (framerate)  try: pip_import('moviepy')  #Ning... |
| `_get_default_video_path()` | 37501 |  As a bitrate  if video_bitrate in _named_video_bitrates: video_bitrate = _named_video_bitrates[vide... |
| `_as_video_bitrate()` | 37516 |  As a bitrate  if video_bitrate in _named_video_bitrates: video_bitrate = _named_video_bitrates[vide... |
| `_as_video_quality()` | 37521 |  As a percent  if video_quality in _named_video_qualities: video_quality = _named_video_qualities[vi... |
| `__init__()` | 37532 | *(No description)* |
| `write_frame()` | 37562 | *(No description)* |
| `finish()` | 37620 | *(No description)* |
| `set_save_video_mp4_default_backend()` | 37713 | frames: a list of images as defined by rp.is_image(). Saves an .mp4 file at the path - frames can al... |
| `run()` | 37980 | *(No description)* |
| `is_empty_folder()` | 38292 | Check if a path points to an existing file.  Enhanced Documentation: This is a fundamental file syst... |
| `path_exists()` | 38348 | Check if a path points to an existing file or directory.  Enhanced Documentation: This is a comprehe... |
| `rename_path()` | 38398 | EXAMPLE: rename_path("apple/bananna/cherry.jpg","coconut.png") is equivalent to (in bash) mv .apple/... |
| `move_path()` | 38418 | Like the 'mv' command Move a folder or file into a given directory if to_path is a directory, otherw... |
| `swap_paths()` | 38471 | Moves path_a to path_b and vice versa This is an atomic operation that will be undone upon erroring ... |
| `delete_symlink()` | 38595 | permanent exists for safety reasons. It can be False in case you make a stupid mistake like deleting... |
| `delete_path()` | 38601 | permanent exists for safety reasons. It can be False in case you make a stupid mistake like deleting... |
| `_delete_paths_helper()` | 38617 | EXAMPLE:  delete_paths( 'a.jpg','b.jpg' ) EXAMPLE:  delete_paths(['a.jpg','b.jpg']) EXAMPLE:  delete... |
| `delfunc()` | 38629 | *(No description)* |
| `delete_paths()` | 38648 | #Chooses between copy_directory and copy_file, whichever makes more sense. #If extract is True, it w... |
| `copy_path()` | 38658 | #Chooses between copy_directory and copy_file, whichever makes more sense. #If extract is True, it w... |
| `get_home_directory()` | 38780 | Returns the ~ directory - aka the user's home directory. Works cross-platform. |
| `copy_paths()` | 38811 | *(No description)* |
| `do_copy()` | 38846 | *(No description)* |
| `get_path_parent()` | 38866 | Retrieve the parent directory or URL of the given path or URL.  Examples: >>> get_path_parent('oaijs... |
| `get_paths_parents()` | 38946 | Will make a directory if it doesn't allready exist. If it does already exist, it won't throw an erro... |
| `make_directories()` | 39101 | Create multiple directories. Plural version of make_directory.  Enhanced Documentation: Creates all ... |
| `path_join()` | 39147 | Joins given paths, which can be a combination of strings and non-string iterables (like lists, tuple... |
| `is_non_str_iterable()` | 39191 | *(No description)* |
| `path_split()` | 39235 | EXAMPLE: >>> path_split('https://claude.ai/chat/6b1ff843-1c6c-4e34-8c9f-21bd83bc0315') ans = ['https... |
| `get_unique_copy_path()` | 39261 | Generates a new file path that does not conflict with any existing files by appending a suffix to th... |
| `apply_suffix_to_name()` | 39345 | *(No description)* |
| `apply_suffix_to_path()` | 39357 | *(No description)* |
| `get_cutscene_frame_numbers()` | 39377 | Returns a list of ints containing all the framenumers of the cutscenes in a video Confirmed to work ... |
| `remove_duplicate_frames()` | 39445 | Remove duplicate frames from a video represented as a NumPy array in THWC format or from a generator... |
| `sim_score()` | 39490 | *(No description)* |
| `helper()` | 39495 | *(No description)* |
| `send_text_message()` | 39532 | number is a phone number. Can be an int or a string Once this no longer works (which it eventually w... |
| `cv_contour_to_segment()` | 39938 | TODO: provide a visual example The way OpenCV extracts single-pixel-wide non-looping contours is to ... |
| `whiten_points_covariance()` | 39956 | Whiten the covariance matrix of a list of n-dimensional points, and return a list of new points. Als... |
| `visible_string_ljust()` | 39980 | Trying to be as much like str.ljust as possible, with a small tweak: str.ljust doesn't ignore ansi e... |
| `visible_string_rjust()` | 39990 | Trying to be as much like str.rjust as possible, with a small tweak: str.rjust doesn't ignore ansi e... |
| `visible_string_center()` | 40000 | Trying to be as much like str.center as possible, with a small tweak: str.center doesn't ignore ansi... |
| `make_string_rectangular()` | 40024 | EXAMPLES: >>> s='The mathematician\nPlotting his past relations\n"ex" and "why" axis' >>> make_strin... |
| `string_is_rectangular()` | 40053 | The fillchar parameter only matters if rectangularize is True EXAMPLE: >>> horizontally_concatenated... |
| `horizontally_concatenated_strings()` | 40059 | The fillchar parameter only matters if rectangularize is True EXAMPLE: >>> horizontally_concatenated... |
| `vertically_concatenated_strings()` | 40096 | Pretty obvious what this does tbh, I dont see good reason for documenation here |
| `wrap_string_to_width()` | 40103 | TODO: Make this work with visible_string_length so that unicode chars/ansi codes are supported EXAMP... |
| `bordered_string()` | 40121 | NOTE: 99% of the time you should be using a rectangular string, as you can tell with string_is_recta... |
| `simple_boxed_string()` | 40224 | EXAMPLE: >>> s="I don't have any kids\n\nBut I like making dad jokes\n\nI am a faux pa" >>> print(si... |
| `griddify()` | 40237 | return bordered_string(make_string_rectangular(string,align=align), width_fill       =chars[0], heig... |
| `uniform_boxify()` | 40238 | return bordered_string(make_string_rectangular(string,align=align), width_fill       =chars[0], heig... |
| `strip_ansi_escapes()` | 40266 | Undoes anything fansi might do to a string Code from https://www.tutorialspoint.com/How-can-I-remove... |
| `visible_string_length()` | 40280 | Give the visible string length when printed into a terminal. Ignores ansi escape seqences and zero-w... |
| `string_width()` | 40298 | Enhanced Documentation: Calculates the maximum display width across all lines in a multi-line string... |
| `string_height()` | 40331 | Pad a string with the specified extra height at the given origin.  Args: string (str): The input str... |
| `_pad_string_height()` | 40335 | Pad a string with the specified extra height at the given origin.  Args: string (str): The input str... |
| `pad_to_same_number_of_lines()` | 40367 | Pad multiple strings to have the same number of lines with the specified origin.  Args: *strings (st... |
| `pad_string_to_dims()` | 40422 | Returns a generator that returns the sequence of primes If you have numba, it will run very very ver... |
| `prime_number_generator()` | 40433 | Returns a generator that returns the sequence of primes If you have numba, it will run very very ver... |
| `primes()` | 40445 | *(No description)* |
| `primes()` | 40459 | Returns the levenshtein_distance between two strings  There are faster implementations. I just took ... |
| `edit_distance()` | 40468 | Returns the levenshtein_distance between two strings  There are faster implementations. I just took ... |
| `__init__()` | 40524 | A timeout decorator that uses the Timeout class To see documentation for this function's arguments, ... |
| `handle_timeout()` | 40527 | A timeout decorator that uses the Timeout class To see documentation for this function's arguments, ... |
| `__enter__()` | 40529 | A timeout decorator that uses the Timeout class To see documentation for this function's arguments, ... |
| `__exit__()` | 40533 | A timeout decorator that uses the Timeout class To see documentation for this function's arguments, ... |
| `timeout()` | 40539 | A timeout decorator that uses the Timeout class To see documentation for this function's arguments, ... |
| `wrapper()` | 40554 | *(No description)* |
| `wrapped()` | 40555 |  Return True if the given noun is in plural form, and False otherwise  return not is_singular_noun(n... |
| `_get_inflect_engine()` | 40564 |  Return True if the given noun is in plural form, and False otherwise  return not is_singular_noun(n... |
| `is_plural_noun()` | 40574 |  Return True if the given noun is in plural form, and False otherwise  return not is_singular_noun(n... |
| `is_singular_noun()` | 40578 |  Return True if the given noun is in singular form, and False otherwise  return not bool(_get_inflec... |
| `is_singular_noun_of()` | 40582 |  Returns true if singular_word is the signular-form of plural_word  return _get_inflect_engine().com... |
| `is_plural_noun_of()` | 40586 |  Returns true if plural_word is the plural-form of singular_word  return _get_inflect_engine().compa... |
| `plural_noun()` | 40590 | Returns the plural form of a singular word If force is true, it will not check to see if this noun i... |
| `singular_noun()` | 40623 | Returns the singular form of a plural word EXAMPLE: singular_noun('houses')            -> 'house' si... |
| `number_to_words()` | 40644 | Returns the english representation of a number (can be an integer, negative, or even floating point.... |
| `words_to_number()` | 40680 | I did my best to make this the inverse of number_to_words, and it works for most cases Returns eithe... |
| `_get_parts_of_speech_via_nltk()` | 40791 | Given a word, return the parts of speech (adjectives, nouns, verbs etc) that this word belongs to. C... |
| `_nltk_wordnet_is_installed()` | 40819 | *(No description)* |
| `_make_sure_nltk_has_wordnet_installed()` | 40828 | Returns true if the given word is an english noun, false otherwise Please note that this function is... |
| `is_a_verb()` | 40837 | Returns true if the given word is an english noun, false otherwise Please note that this function is... |
| `is_an_adjective()` | 40841 | Returns true if the given word is an english noun, false otherwise Please note that this function is... |
| `is_a_noun()` | 40845 | Returns true if the given word is an english noun, false otherwise Please note that this function is... |
| `get_all_english_words()` | 40854 | Apparently, both Linux and Mac have a file that contains every english word! See https://stackoverfl... |
| `_get_all_english_words_lowercase()` | 40866 | Splits the input text into sentences based on the specified language.  This function uses the Punkt ... |
| `is_an_english_word()` | 40869 | Splits the input text into sentences based on the specified language.  This function uses the Punkt ... |
| `split_sentences()` | 40873 | Splits the input text into sentences based on the specified language.  This function uses the Punkt ... |
| `_get_punkt_languages()` | 40951 | Gets a list of languages supported by nltk's punkt (sentence splitter) Current languages as of writi... |
| `connected_to_internet()` | 40992 | Return True if we're online, else False Code from: https://stackoverflow.com/questions/20913411/test... |
| `_string_pager_via_pypager()` | 41013 |  Uses prompt-toolkit. But this can break if you have the wrong prompt toolkit version.  Also it fail... |
| `_string_pager_via_click()` | 41023 |  A pure-python alternative to less  click=pip_import('click') click.echo_via_pager(string)  def _str... |
| `_string_pager_via_less()` | 41028 | Pipes a string into less, respecting ANSI escape sequences for coloring.  Args: string: The string t... |
| `string_pager()` | 41059 | Uses a python-based pager, similar to the program 'less', where you can scroll and search through th... |
| `_get_pynput_mouse_controller()` | 41082 | Private function to get or create a cached pynput mouse controller instance.  Enhanced Documentation... |
| `get_mouse_position()` | 41116 | Return (x,y) coordinates representing the position of the mouse cursor. (0,0) is the top left corner... |
| `get_mouse_x()` | 41124 | EXAMPLES: set_mouse_position( 23,40 ) #you can specify the coordinates as separate x,y arguments set... |
| `get_mouse_y()` | 41127 | EXAMPLES: set_mouse_position( 23,40 ) #you can specify the coordinates as separate x,y arguments set... |
| `set_mouse_position()` | 41130 | EXAMPLES: set_mouse_position( 23,40 ) #you can specify the coordinates as separate x,y arguments set... |
| `record_mouse_positions()` | 41144 | #Record the mouse position for (duration) seconds, taking (rate) samples per second |
| `playback_mouse_positions()` | 41156 | #Play back a list of mouse positions at (rate) positions per second #EXAMPLE: playback_mouse_positio... |
| `mouse_left_click()` | 41167 | Trigger the mouse's left click button |
| `mouse_right_click()` | 41174 | Trigger the mouse's right click button |
| `mouse_middle_click()` | 41181 | Trigger the mouse's middle click button |
| `mouse_left_press()` | 41188 | Press the mouse's left button EXAMPLE: mouse_left_press();sleep(1);mouse_left_release() |
| `mouse_right_press()` | 41196 | Press the mouse's right button EXAMPLE: mouse_right_press();sleep(1);mouse_right_release() |
| `mouse_middle_press()` | 41204 | Press the mouse's middle button EXAMPLE: mouse_middle_press();sleep(1);mouse_middle_release() |
| `mouse_left_release()` | 41212 | Release the mouse's left button EXAMPLE: mouse_left_release();sleep(1);mouse_left_release() |
| `mouse_right_release()` | 41220 | Release the mouse's right button EXAMPLE: mouse_right_release();sleep(1);mouse_right_release() |
| `mouse_middle_release()` | 41228 | Release the mouse's middle button EXAMPLE: mouse_middle_release();sleep(1);mouse_middle_release() |
| `get_monitor_resolution()` | 41238 | Returns the resolution of the primarty monitor as (height, width) |
| `get_number_of_monitors()` | 41249 | Returns an int: the number of monitors attached to this computer. |
| `get_box_char_bar_graph()` | 41326 | Generate a bar graph using box characters based on the provided values.  Args: values (list): A list... |
| `get_scope()` | 41462 | Get the scope of n levels up from the current stack frame Useful as a substitute for using globals()... |
| `_get_visible_scope()` | 41500 | Treat the output as read-only! Will include all variables that can be seen from that point.  Should ... |
| `get_all_importable_module_names()` | 41583 | Returns a set of all known names that you can use 'import <name>' on |
| `get_module_path_from_name()` | 41602 | Gets the file path of a module or package without importing it, given the module's name.  For packag... |
| `get_module_path()` | 41648 | Returns the file path of a given python module |
| `is_a_module()` | 41675 | Converts a datetime object to seconds since the Unix epoch; aka seconds since January 1st, 1970 at 0... |
| `date_to_epoch_seconds()` | 41679 | Converts a datetime object to seconds since the Unix epoch; aka seconds since January 1st, 1970 at 0... |
| `date_to_epoch_millis()` | 41687 | Converts a datetime object to milliseconds since the Unix epoch; aka millis since January 1st, 1970 ... |
| `epoch_seconds_to_date()` | 41691 | Converts epoch time in seconds to a datetime object; returns a datetime representing the time since ... |
| `epoch_millis_to_date()` | 41698 | Converts epoch time in milliseconds to a datetime object; returns a datetime representing the time s... |
| `get_current_date()` | 41703 | This is annoying to type...so I added this function as a bit of sugar. |
| `string_to_date()` | 41710 | Given a date represented as a string, turn it into a datetime object and return it It can handle man... |
| `mean()` | 41790 | A super basic mean calculator Works with any datatype that supports + and /  EXAMPLES: >>> mean(1,2,... |
| `median()` | 41807 | EXAMPLES: >>> median(1,1,1,5,9,9,9) ans = 5 >>> median([1,1,1,5,9,9,9]) ans = 5 >>> median(['a','b',... |
| `norm_cdf()` | 41821 | normal cumulative distribution function Given a value x, calculate the z-score and return the cumula... |
| `norm_pdf()` | 41834 | normal probability density function Given a value x, calculate the z-score and return the normal dis... |
| `inverse_norm_cdf()` | 41846 | inverse normal cumulative distribution function The inverse of the norm_pdf function (given a probab... |
| `s3_list_objects()` | 41859 | Generator function to list S3 objects at a given S3 URL.  Parameters: - s3url (str): The S3 URL in t... |
| `helper()` | 41900 | *(No description)* |
| `is_s3_url()` | 41977 | Download files from URLs with multi-protocol support and automatic path handling.  Supports HTTP/HTT... |
| `is_gs_url()` | 41981 | Download files from URLs with multi-protocol support and automatic path handling.  Supports HTTP/HTT... |
| `__init__()` | 42207 | *(No description)* |
| `__enter__()` | 42211 | *(No description)* |
| `__exit__()` | 42214 | *(No description)* |
| `__init__()` | 42221 | *(No description)* |
| `__enter__()` | 42228 | *(No description)* |
| `__exit__()` | 42247 | Like download_url, except you only specify the output diectory - the filename will be chosen for you... |
| `get_cache_file_path()` | 42341 | r Computes a cache file path for the provided input It is a pure function, and uses no system calls ... |
| `get_cache_file_paths()` | 42422 | Plural of get_cache_file_path, supporting a `lazy` option func = gather_args_bind(get_cache_file_pat... |
| `is_a_matrix()` | 42470 | Square matrices are of shape (N,N) where N is some integer This function returns N Lets you not have... |
| `is_a_square_matrix()` | 42474 | Square matrices are of shape (N,N) where N is some integer This function returns N Lets you not have... |
| `prime_factors()` | 42489 | EXAMPLES: >>> prime_factors(23) ans = [23] >>> prime_factors(24) ans = [2, 2, 2, 3] >>> prime_factor... |
| `set_os_volume()` | 42525 |  Set your operating system's volume  assert is_number(percent),'Volume percent should be a number, b... |
| `fuzzy_string_match()` | 42534 | >>> fuzzy_string_match('apha','alpha') ans = True >>> fuzzy_string_match('alpha','alpha') ans = True... |
| `get_english_synonyms_via_nltk()` | 42558 | This thing is really crappy...but also really funny xD This thing belongs in death of the mind hones... |
| `get_english_synonyms_via_datamuse()` | 42588 | EXAMPLE: get_english_synonyms_via_datamuse('food') Uses https://www.datamuse.com/api/ |
| `get_english_related_words_via_datamuse()` | 42595 | EXAMPLE: get_english_synonyms_via_datamuse('food') Uses https://www.datamuse.com/api/ |
| `get_english_antonyms_via_datamuse()` | 42602 | EXAMPLE: get_english_synonyms_via_datamuse('good') Uses https://www.datamuse.com/api/ |
| `get_english_rhymes_via_datamuse()` | 42609 | EXAMPLE: get_english_synonyms_via_datamuse('breath')#poppy: what rhymes with breath? Uses https://ww... |
| `get_english_synonyms()` | 42616 | *(No description)* |
| `fibonacci()` | 42625 | Runs in constant time inverse_fibonacci(fibonacci(3415))==3415 inverse_fibonacci(fibonacci(1234))==1... |
| `inverse_fibonacci()` | 42643 | Runs in constant time inverse_fibonacci(fibonacci(3415))==3415 inverse_fibonacci(fibonacci(1234))==1... |
| `graham_scan()` | 42657 | This function is intentionally unoptimized to match my personal intuition of the algorithm most clos... |
| `convex_hull()` | 42770 | Only 2d convex hulls are supported at the moment, sorry... |
| `_point_on_edge()` | 42776 |  Return true if a point is on an edge, including the edge's endpoints  point,=as_complex_vector([poi... |
| `_edges_intersect()` | 42782 | *(No description)* |
| `paths_intersect()` | 42811 | Does NOT assume the paths are loops O(n^2) naive algorithm. Should be full-proof. |
| `_edge_intersection_positions()` | 42841 |  Will return a list of either 0, 1 or 2 points (2 points is a special edge case where one line share... |
| `path_intersections()` | 42873 | TODO: Let this function take varargs paths and return all intersections Returns a list of points whe... |
| `path_intersects_point()` | 42890 |  Return true if a 2d point "point" lies along a path of 2d points "path"  return paths_intersect([po... |
| `add()` | 42910 | import functools @functools.wraps(func) def wrapper(*args): if not args: raise TypeError(func.__name... |
| `wrapper()` | 42920 | Written by Ryan Burgert, 2020. Written for efficiency's sake. Works for strings, lists and tuples (a... |
| `longest_common_prefix()` | 42934 | Written by Ryan Burgert, 2020. Written for efficiency's sake. Works for strings, lists and tuples (a... |
| `longest_common_suffix()` | 42968 | This funcion is analagous to longest_common_prefix. See it for more documentation. EXAMPLES: longest... |
| `longest_common_substring()` | 42986 | https://pypi.org/project/pylcs/ Doesn't seem to be super efficient...would be better if it just retu... |
| `format_path()` | 43156 | *(No description)* |
| `option_to_string()` | 43233 | Returns the path of a temporary, writeable file (No more pesky "don't have permission to write" erro... |
| `temporary_file_path()` | 43250 | Returns the path of a temporary, writeable file (No more pesky "don't have permission to write" erro... |
| `python_2_to_3()` | 43311 | Turns python2 code into python3 code EXAMPLE: python_2_to_3("print raw_input('>>>')") --> "print(inp... |
| `strip_python_docstrings()` | 43329 | This function removes all docstrings from functions and classes in the input Python code. The code i... |
| `strip_python_comments()` | 43358 | Takes a string, and returns a string Removes all python #comments from code with a scalpel (not touc... |
| `strip_trailing_whitespace()` | 43367 | Takes a string, and returns a string Returns a new string, with all trailing whitespace removed from... |
| `delete_empty_lines()` | 43375 | Takes a string, and returns a string Removes all lines of length 0 from the string and returns the r... |
| `propagate_whitespace()` | 43383 | Best used when you pass it a string whose trailing whitespace are stripped, but you can pass it any ... |
| `_get_ryan_rprc_path()` | 43556 | Vim depends on a python executable somewhere on your computer. This function returns the path to tha... |
| `_set_ryan_rprc()` | 43561 | Vim depends on a python executable somewhere on your computer. This function returns the path to tha... |
| `get_vim_python_executable()` | 43567 | Vim depends on a python executable somewhere on your computer. This function returns the path to tha... |
| `_vim_pip_install()` | 43599 |  Package can be like package=='ropevim'  command = get_vim_python_executable()+' -m pip install %s -... |
| `_set_ryan_ranger_config()` | 43604 | Configure ranger file manager with RP-optimized settings. Internal helper. |
| `_set_ryan_vimrc()` | 43616 | ON MAC, Ropevim Is annoying to install: :py3 import os; print(os.__file__)  Prints something like  /... |
| `_set_ryan_xonshrc()` | 43670 | ryan_xonfig= $PROMPT = "{BOLD_CYAN} >> {BOLD_CYAN}{cwd_base}{branch_color}{curr_branch: {}}{NO_COLOR... |
| `_sort_imports_via_isort()` | 43681 | Removes dead imports  EXAMPLE: >>> code = "import numpy\nprint(123)" >>> print(code) import numpy pr... |
| `clean_imports_via_unimport()` | 43687 | Removes dead imports  EXAMPLE: >>> code = "import numpy\nprint(123)" >>> print(code) import numpy pr... |
| `_set_ryan_tmux_conf()` | 43900 | Run a system command, announcing it  EXAMPLE: >>> _run_sys_command('echo hello') SYS COMMAND: echo h... |
| `_run_sys_command()` | 43911 | Run a system command, announcing it  EXAMPLE: >>> _run_sys_command('echo hello') SYS COMMAND: echo h... |
| `_ensure_installed()` | 43931 |  Attempts to install a program on various operating systems   assert isinstance(name,    str) assert... |
| `_brew_install()` | 43965 | _run_sys_command(/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/... |
| `_ensure_brew_installed()` | 43970 | _run_sys_command(/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/... |
| `_ensure_wget_installed()` | 43976 | *(No description)* |
| `_ensure_rclone_installed()` | 43992 | *(No description)* |
| `_ensure_ffmpeg_installed()` | 44000 | *(No description)* |
| `_ensure_gemini_cli_installed()` | 44022 | *(No description)* |
| `_ensure_snap_installed()` | 44031 | *(No description)* |
| `_ensure_nvtop_installed()` | 44040 |  https://ohmyz.sh/#install  _ensure_zsh_installed() _ensure_curl_installed() _run_sys_command('sh -c... |
| `_ensure_zsh_installed()` | 44048 |  https://ohmyz.sh/#install  _ensure_zsh_installed() _ensure_curl_installed() _run_sys_command('sh -c... |
| `_install_oh_my_zsh()` | 44056 |  https://ohmyz.sh/#install  _ensure_zsh_installed() _ensure_curl_installed() _run_sys_command('sh -c... |
| `_ensure_viddy_installed()` | 44062 |  https://github.com/sachaos/viddy  _ensure_installed( 'viddy', mac='brew install viddy', linux='wget... |
| `_ensure_tmux_installed()` | 44071 | *(No description)* |
| `_ensure_npm_installed()` | 44079 | *(No description)* |
| `_ensure_nvm_installed()` | 44088 | *(No description)* |
| `_ensure_node_installed()` | 44097 | *(No description)* |
| `_ensure_git_installed()` | 44106 | *(No description)* |
| `_install_ollama()` | 44115 | *(No description)* |
| `_ensure_ollama_server_running()` | 44125 | *(No description)* |
| `_ensure_cog_installed()` | 44281 | Cog is an open source tool that makes it easy to put a machine learning model in a Docker container.... |
| `_run_bashtop()` | 44292 | _run_sys_command(yes \| sudo add-apt-repository ppa:bashtop-monitor/bashtop sudo apt update |
| `_run_ai_cli_coder()` | 44352 | Given code as either a path or a string, edits that code using a cli-based coder (such as gemini-cli... |
| `_run_claude_code()` | 44442 |  See rp.r._run_ai_cli_coder.__doc__  _ensure_claudecode_installed() return _run_ai_cli_coder(code,'c... |
| `_run_gemini_cli()` | 44447 |  See rp.r._run_ai_cli_coder.__doc__  _ensure_gemini_cli_installed() return _run_ai_cli_coder(code,'g... |
| `get_port_is_taken()` | 44467 | Check if a port is already in use.  Args: port (int): The port number to check.  Returns: bool: True... |
| `get_next_free_port()` | 44492 | Find the next free port starting from a given port. For example, if port=8080 and port 8080 is taken... |
| `get_all_taken_ports()` | 44519 | Returns all ports that are currently taken up global _get_all_taken_ports_cache if use_cache and _ge... |
| `helper()` | 44527 | Gets the process ID (PID) using the specified port.  Args: port: The port number. strict: If True, r... |
| `get_process_using_port()` | 44545 | Gets the process ID (PID) using the specified port.  Args: port: The port number. strict: If True, r... |
| `compress_bytes()` | 44608 | Compress bytes data.  Args: data: The input bytes to compress  Returns: Compressed bytes |
| `decompress_bytes()` | 44621 | Decompress bytes data.  Args: compressed_data: The compressed bytes to decompress  Returns: Original... |
| `_dill_dumps()` | 44642 | Try to somehow turn x into a bytestring. Right now, it supports numpy arrays, lambdas and functions,... |
| `object_to_bytes()` | 44647 | Try to somehow turn x into a bytestring. Right now, it supports numpy arrays, lambdas and functions,... |
| `object_to_base64()` | 44659 |  Inverse of object_to_bytes, see object_to_bytes for more documentation  dill=pip_import('dill') try... |
| `base64_to_object()` | 44662 |  Inverse of object_to_bytes, see object_to_bytes for more documentation  dill=pip_import('dill') try... |
| `bytes_to_object()` | 44665 |  Inverse of object_to_bytes, see object_to_bytes for more documentation  dill=pip_import('dill') try... |
| `__init__()` | 44735 |  Make the request for web-copying. Can also upload arbitrary HTML pages.  assert connected_to_intern... |
| `update()` | 44741 |  Make the request for web-copying. Can also upload arbitrary HTML pages.  assert connected_to_intern... |
| `read()` | 44746 |  Make the request for web-copying. Can also upload arbitrary HTML pages.  assert connected_to_intern... |
| `tmux_copy()` | 44792 |  Copies a string to tmux's clipboard, assuming tmux is running and installed  assert isinstance(stri... |
| `tmux_paste()` | 44802 |  Returns the string from tmux's current clipboard, assuming tmux is running and installed  tmux_clip... |
| `local_copy()` | 44807 | Works just like web_copy, but is local to one's computer This makes copying large python objects bet... |
| `local_paste()` | 44816 | Works just like web_paste, but is local to one's computer This makes copying large python objects be... |
| `_run_tmux_command()` | 44824 | Utility function to run a tmux command.  Enhanced Documentation: ======================== Private he... |
| `tmux_get_current_pane_index()` | 44864 | Returns the index of the current tmux pane. return int(_run_tmux_command("tmux display -p -t '{down-... |
| `tmux_get_current_window_index()` | 44868 | Returns the index of the current tmux window. return int(_run_tmux_command(["tmux", "display-message... |
| `tmux_get_current_window_name()` | 44872 | Returns the name of the current tmux window. return _run_tmux_command(["tmux", "display-message", "-... |
| `tmux_get_current_session_index()` | 44876 | Returns the index of the current tmux session. return int(_run_tmux_command(["tmux", "display-messag... |
| `tmux_get_current_session_name()` | 44880 | Returns: str: The name of the current tmux session.  Raises: AssertionError: If you run this functio... |
| `_get_all_tmux_windows()` | 44896 | Returns a list of all window indexes in the current tmux session. window_indexes = _run_tmux_command... |
| `_tmux_close_windows()` | 44901 | Closes tmux windows based on a filtering condition function, private to this module. current_window ... |
| `tmux_close_windows_to_left()` | 44911 | Closes all tmux windows to the left of the current window. _tmux_close_windows(lambda w, current: w ... |
| `tmux_close_windows_to_right()` | 44915 | Closes all tmux windows to the right of the current window. _tmux_close_windows(lambda w, current: w... |
| `tmux_close_other_windows()` | 44919 | Closes all tmux windows except the current one. _tmux_close_windows(lambda w, current: w != current)... |
| `tmux_close_other_sessions()` | 44923 | Closes all tmux sessions except the current one. current_session = tmux_get_current_session_name() a... |
| `tmux_detach_other_clients()` | 44935 | Detaches all other clients from the current tmux session. current_session = tmux_get_current_session... |
| `_get_current_tmux_client()` | 44946 | Returns the ID of the current tmux client. return _run_tmux_command(['tmux', 'display-message', '-p'... |
| `_get_all_tmux_clients()` | 44950 | Returns a list of all client IDs attached to the specified tmux session. clients = _run_tmux_command... |
| `tmux_get_all_session_names()` | 44955 | Retrieve the names of all active tmux sessions.  Returns: list: A list of strings representing the n... |
| `tmux_get_unique_session_name()` | 44970 |  Given a prefix, will return a new session name that doesn't exist already  existing_sessions=tmux_g... |
| `tmux_get_current_session_name()` | 44982 | Returns: str: The name of the current tmux session.  Raises: AssertionError: If you run this functio... |
| `tmux_session_exists()` | 44998 | Returns True if a session exists, False otherwise. |
| `tmux_kill_session()` | 45006 | Kill a specified tmux session by its name.  Args: session_name (str): The name of the tmux session t... |
| `tmux_kill_sessions()` | 45036 | Plural of tmux_kill_session session_names = detuple(session_names)  #If strict, make sure all sessio... |
| `tmux_type_in_all_panes()` | 45051 | Sends keystrokes to all panes within a specified Tmux session and window. If no session or window is... |
| `tmux_get_scrollback()` | 45108 | Gets the scrollback buffer of the current tmux pane.  Returns: str: The scrollback buffer content. |
| `_tmux_reset_all_panes()` | 45130 | Resets all panes within a specified Tmux session and window. If no session or window is specified, t... |
| `tmuxp_create_session_yaml()` | 45162 | Creates a yaml file to be loaded by tmuxp. See https://github.com/tmux-python/tmuxp It lets you easi... |
| `is_listlike()` | 45328 | *(No description)* |
| `tmuxp_launch_session_from_yaml()` | 45389 | Input can be a yaml string or yaml file path Uses the "tmuxp load <yaml file>" command to spin up a ... |
| `_extract_code_cells_from_ipynb()` | 45465 | Extract code cells from a Jupyter notebook as a list.  Args: notebook_path (str, optional): Path to ... |
| `exec_ipynb()` | 45513 | Run code from a jupyter notebook TODO: Add show_text and show_markdown options too |
| `_announce_cell()` | 45527 | *(No description)* |
| `_get_jupyter_output_widget()` | 45565 | Extract and concatenate code from a Jupyter notebook as a single string.  Args: notebook_path (str, ... |
| `extract_code_from_ipynb()` | 45576 | Extract and concatenate code from a Jupyter notebook as a single string.  Args: notebook_path (str, ... |
| `_get_facebook_client()` | 45594 | TODO: Fix this its too old to work with current facebook APIs |
| `send_facebook_message()` | 45601 | TODO: Fix this its too old to work with current facebook APIs |
| `get_all_facebook_messages()` | 45617 | TODO: Fix this its too old to work with current facebook APIs Returns a list of all messages between... |
| `format()` | 45638 | Lets you explore a pytorch module in a graphical terminal ui. No more wondering what a config does t... |
| `explore_torch_module()` | 45651 | Lets you explore a pytorch module in a graphical terminal ui. No more wondering what a config does t... |
| `record_torch_module_forward_stats()` | 45740 | A context manager to wrap a call of a torch module! Records tons of stats about it Best to use with ... |
| `visualize_pytorch_model()` | 45765 | TODO: integrate code better with _visualize_pytorch_model_via_torchviz: get rid of redundant code Sh... |
| `get_sinusoidal_positional_encodings()` | 45816 | Generate sinusoidal position encodings for transformer models.  Parameters: shape: int or list/tuple... |
| `inverted_color()` | 46072 | >>> inverted_color('#00FF00')      --->  #FF00FF               #If given color is in hex form, keep ... |
| `_extract_archive_via_pyunpack()` | 46265 | This function is used to unpack more than just .zip files. It can unpack .rar files, .tar files, .7z... |
| `get_normal_map()` | 46421 | Turn a bump map aka a height map, into a normal map This is used for 3d graphics, such as in video g... |
| `sobel_edges()` | 46438 | Calculates sobel edges for edge detection Computes it indivisually for each r,g,b channel - Because ... |
| `currently_in_a_tty()` | 46469 | Returns True if we're in a TTY (aka a terminal that can run Prompt-Toolkit) (As opposed to, for exam... |
| `currently_running_desktop()` | 46481 | Determines if a desktop environment is currently running.  Parameters: - verbose (bool): Whether to ... |
| `_fd()` | 46568 | *(No description)* |
| `highlighted()` | 46570 | *(No description)* |
| `get_image_file_dimensions()` | 46607 | Takes the file path of an image, and returns the image's (height, width) It does this without loadin... |
| `get_video_file_shape()` | 46627 | Returns the shape of the numpy tensor we would get with rp.load_video(path)  Args: path (str): Path ... |
| `get_video_file_num_frames()` | 46659 | Returns the number of frames in the video. |
| `get_video_file_height()` | 46666 | Returns the height of the video. |
| `get_video_file_width()` | 46673 | Returns the width of the video. |
| `_hsv_to_rgb_via_numba()` | 46723 | Convert an HSV image to RGB using Numba for optimization. The input HSV values are assumed to be in ... |
| `_rgb_to_hsv_via_numba()` | 46789 | Convert an RGB image to HSV using Numba for optimization. The input RGB values are assumed to be in ... |
| `hsv_to_rgb()` | 46856 | Convert an HSV image to RGB.  Install Numba to get a massive speed boost!  Initially, the conversion... |
| `rgb_to_hsv()` | 46937 | Convert an RGB image to HSV.  Install Numba to get a massive speed boost!  Initially, the conversion... |
| `get_image_hue()` | 47017 | Takes in an image as defined by rp.is_image and returns a matrix assert is_image(image) return rgb_t... |
| `get_image_saturation()` | 47022 | Takes in an image as defined by rp.is_image and returns a matrix assert is_image(image) return rgb_t... |
| `get_image_value()` | 47027 | Takes in an image as defined by rp.is_image and returns a matrix assert is_image(image) return rgb_t... |
| `get_image_red()` | 47034 | Takes in an image as defined by rp.is_image and returns a matrix image=as_numpy_image(image,copy=Fal... |
| `get_image_green()` | 47041 | Takes in an image as defined by rp.is_image and returns a matrix image=as_numpy_image(image,copy=Fal... |
| `get_image_blue()` | 47048 | Takes in an image as defined by rp.is_image and returns a matrix image=as_numpy_image(image,copy=Fal... |
| `hsv_to_rgb_float_color()` | 47202 | Converts a floating point HSV color to an RGB one hsv_to_rgb_float_color(h,s,v) ==== hsv_to_rgb_floa... |
| `float_color_to_ansi256()` | 47213 | Convert RGB values (0.0 to 1.0) to the nearest ANSI 256-color code Returns an integer  float_color_t... |
| `get_rgb_byte_color_identity_mapping_image()` | 47256 | Save this image, and color-grade it. Then the new image can be used as a map! Originally made for co... |
| `zalgo_text()` | 47302 | EXAMPLE: zalgo_text('Hello World',0) == 'Hello World' EXAMPLE: zalgo_text('Hello World',1) == 'H̵ͮe͚... |
| `big_ascii_text()` | 47324 | r Returns big ascii art text! EXAMPLE: ➤ big_ascii_text('Hello World!') ans = _   _        _  _     ... |
| `helper()` | 47424 | Enhanced Documentation:  Reads binary data from a file path or URL, returning raw bytes content. Sup... |
| `bytes_to_base64()` | 47589 | In some circumstances (with exotic args or kwargs) this could be better than the fire.Fire module  E... |
| `base64_to_bytes()` | 47593 | In some circumstances (with exotic args or kwargs) this could be better than the fire.Fire module  E... |
| `bytes_to_base16()` | 47597 | In some circumstances (with exotic args or kwargs) this could be better than the fire.Fire module  E... |
| `base16_to_bytes()` | 47601 | In some circumstances (with exotic args or kwargs) this could be better than the fire.Fire module  E... |
| `func_call_to_shell_command()` | 47605 | In some circumstances (with exotic args or kwargs) this could be better than the fire.Fire module  E... |
| `_call_from_base64_string()` | 47628 | Ranger is a curses-based file manager with Vim keybindings It's really useful for quickly/visually b... |
| `_launch_ranger()` | 47638 | Ranger is a curses-based file manager with Vim keybindings It's really useful for quickly/visually b... |
| `get_computer_name()` | 47713 | Returns the name of the current computer https://stackoverflow.com/questions/799767/getting-name-of-... |
| `random_rotation_matrix()` | 47749 | Also known as a real orthonormal matrix Every vector in the output matrix is orthogonal to every vec... |
| `display_pandas_correlation_heatmap()` | 47796 | This function is used for exploratory analysis with pandas dataframes. It lets you see which variabl... |
| `view_table()` | 47827 | Launches a program that lets you view tabular data Kinda like microsoft excel, but in a terminal Can... |
| `launch_visidata()` | 47871 | Launches VisiData to view and potentially edit a file or data object. Useful for manually editing Da... |
| `_write_to_pterm_hist()` | 47920 | OpenCV is a bit finicky sometimes Apart from just as_float_image, there are some other requirements |
| `_size_to_height_width()` | 48036 | Common helper among image resizing funcs Takes in a size (either a scalar or (height, width) tuple R... |
| `_as_skia_image()` | 48271 | *(No description)* |
| `_get_skia_sampling()` | 48292 | Determines the best Skia SamplingOptions based on the interpolation string and mipmap setting.  inte... |
| `get_identity_uv_map()` | 48685 | Returns an RGB UV-Map image with the form uv_form  EXAMPLE: >>> display_image( ...     with_alpha_ch... |
| `validate_tensor_shapes()` | 48726 | Validates that tensor dimensions match expected shapes and extracts dimension values. Reads the tens... |
| `format_shape()` | 48857 | *(No description)* |
| `_test_validate_tensor_shapes()` | 49073 | Run a test function and report results. print("\n{}\nTEST: {}\n{}".format('='*80, name, '-'*80)) try... |
| `run_test()` | 49076 | Run a test function and report results. print("\n{}\nTEST: {}\n{}".format('='*80, name, '-'*80)) try... |
| `test_manual_dimension()` | 49119 | *(No description)* |
| `test_dim_count_mismatch()` | 49141 | *(No description)* |
| `test_literal_mismatch()` | 49148 |  Works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.ceil(x)... |
| `test_inconsistent_dims()` | 49155 |  Works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.ceil(x)... |
| `_ceil()` | 49164 |  Works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.ceil(x)... |
| `_floor()` | 49170 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.floor(x... |
| `_round()` | 49176 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.round(x... |
| `_sin()` | 49182 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.sin(x) ... |
| `_cos()` | 49188 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.cos(x) ... |
| `_tan()` | 49194 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.tan(x) ... |
| `_exp()` | 49200 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.exp(x) ... |
| `_sqrt()` | 49218 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.sqrt(x)... |
| `_abs()` | 49224 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.abs(x) ... |
| `_pow()` | 49230 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.power(x... |
| `_fft()` | 49236 |  works across libraries - such as numpy, torch  if is_numpy_array (x):return np.fft.fft(x) if is_tor... |
| `_ifft()` | 49242 |  works across libraries - such as numpy, torch  if is_numpy_array (x):return np.fft.ifft(x) if is_to... |
| `_tanh()` | 49248 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.tanh(x)... |
| `_sigmoid()` | 49254 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return 1 / (1 + n... |
| `_relu()` | 49260 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.maximum... |
| `_softmax()` | 49266 |  works across libraries - such as numpy, torch  if is_numpy_array (x): e_x = np.exp(x - np.max(x, ax... |
| `_asin()` | 49280 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.arcsin(... |
| `_acos()` | 49286 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.arccos(... |
| `_atan()` | 49292 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.arctan(... |
| `_clip()` | 49298 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.clip(x,... |
| `_nan_to_num()` | 49304 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.nan_to_... |
| `_clamp()` | 49311 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (y):return np.arctan2... |
| `_atan2()` | 49314 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (y):return np.arctan2... |
| `_sinh()` | 49320 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.sinh(x)... |
| `_cosh()` | 49326 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.cosh(x)... |
| `_sign()` | 49332 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.sign(x)... |
| `_degrees()` | 49338 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.degrees... |
| `_radians()` | 49344 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.radians... |
| `_create_array_like()` | 49350 | Helper function for creating arrays/tensors across libraries target_shape = shape if shape is not No... |
| `_zeros_like()` | 49381 | Works across libraries - such as numpy, torch return _create_array_like(x, func_name='zeros', shape=... |
| `_ones_like()` | 49385 | Works across libraries - such as numpy, torch return _create_array_like(x, func_name='ones', shape=s... |
| `_randn_like()` | 49390 | Works across libraries - such as numpy, torch return _create_array_like(x, func_name='randn', shape=... |
| `_rand_like()` | 49394 | Works across libraries - such as numpy, torch return _create_array_like(x, func_name='rand', shape=s... |
| `_maximum()` | 49398 |  works across libraries - such as numpy, torch  if is_numpy_array (x):return np.maximum(x, y) if is_... |
| `_minimum()` | 49404 |  works across libraries - such as numpy, torch  if is_numpy_array (x):return np.minimum(x, y) if is_... |
| `_max()` | 49410 |  works across libraries - such as numpy, torch  if is_numpy_array (x):return np.max(x, axis=dim, kee... |
| `_min()` | 49420 |  works across libraries - such as numpy, torch  if is_numpy_array (x):return np.min(x, axis=dim, kee... |
| `_sum()` | 49430 |  works across libraries - such as numpy, torch  if is_numpy_array (x):return np.sum(x, axis=dim, kee... |
| `_mean()` | 49437 |  works across libraries - such as numpy, torch  if is_numpy_array (x):return np.mean(x, axis=dim, ke... |
| `get_bilinear_weights()` | 49506 | Calculate bilinear interpolation weights for a set of (x, y) coordinates.  This function takes a set... |
| `accumulate_flows()` | 49840 | Accumulates a sequence of flows into a single flow or a sequence of accumulated flows.  A flow is a ... |
| `_iterfzf()` | 50506 | Inpaint an image using OpenCV's inpainting methods. The inpainting will be super smooth, and does no... |
| `sanitize_string()` | 50510 | Inpaint an image using OpenCV's inpainting methods. The inpainting will be super smooth, and does no... |
| `cv_floodfill_mask()` | 50580 | A wrapper for cv2.floodfill Takes in an image, and returns a binary mask of same dimensions It acts ... |
| `get_path_inode()` | 50637 | Returns the inode number of the file or directory at the given path.  Parameters: path (str): The fi... |
| `_is_dir_entry()` | 50664 | This class is made to be used by functions in rp for efficeintly processing files without calling os... |
| `__init__()` | 50690 | *(No description)* |
| `__repr__()` | 50752 | *(No description)* |
| `__hash__()` | 50755 | *(No description)* |
| `__eq__()` | 50758 | TODO: Make this multi-threaded!!!! Retrieves all paths in the given directory according to the speci... |
| `_get_all_paths_fast()` | 50762 | TODO: Make this multi-threaded!!!! Retrieves all paths in the given directory according to the speci... |
| `should_include()` | 50816 | *(No description)* |
| `should_explore()` | 50825 | *(No description)* |
| `explore()` | 50839 | *(No description)* |
| `generator()` | 50857 | *(No description)* |
| `breadth_first_path_iterator()` | 50897 | As opposed to a depth-first path iterator, this goes through every file and directory from the root ... |
| `gpt3()` | 50942 | Use GPT3 to write some text https://deepai.org/machine-learning-model/text-generator |
| `deepgenx()` | 50963 | *(No description)* |
| `_get_openai_api_key()` | 50990 | *(No description)* |
| `_run_openai_llm()` | 51001 | *(No description)* |
| `minify_python_code()` | 51034 | Takes an image, finds text on it, and returns the text as a string (Optical character recognition) I... |
| `cv_equalize_histogram()` | 51054 | Equalizes the histogram of a given image If by_balue is True, and image is RGB, equalize it's value ... |
| `extract_alpha_channel()` | 51164 |  Gets teh alpha channel of a given image, returned as grayscale image (i.e. numpy matrix)  image=as_... |
| `with_alpha_channel()` | 51184 | Assigns an alpha channel to an image The alpha can either be given as a number between 0 and 1, or a... |
| `config()` | 51270 | *(No description)* |
| `init_colors()` | 51280 | *(No description)* |
| `get_matrix_code_chars()` | 51296 | Make rain forever by choosing a random column from pool and make rain at that column and repeat :par... |
| `random_char()` | 51306 | Make rain forever by choosing a random column from pool and make rain at that column and repeat :par... |
| `random_rain_length()` | 51310 | Make rain forever by choosing a random column from pool and make rain at that column and repeat :par... |
| `rain_forever()` | 51314 | Make rain forever by choosing a random column from pool and make rain at that column and repeat :par... |
| `rain_once()` | 51346 | Make rain once at column x from line begin to line end :param stdscr: curses's screen object :param ... |
| `animate_rain()` | 51362 | A rain consists of 3 parts: head, body, and tail Head: the white leading rain drop Body: the fading ... |
| `get_color()` | 51385 | *(No description)* |
| `update_style()` | 51428 | Cycle thru different styles :return: None |
| `main()` | 51470 | *(No description)* |
| `add_rain()` | 51503 | Helper function for string diff operations Sets up git repo and executes the provided diff command |
| `_string_diff_helper()` | 51510 | Helper function for string diff operations Sets up git repo and executes the provided diff command |
| `dunk_string_diff()` | 51541 | this function asssumes you have git installed lets you view the diff between two strings interactive... |
| `view_string_diff()` | 51550 | this function asssumes you have git installed lets you view the diff between two strings interactive... |
| `vim_string_diff()` | 51559 | Requires the program 'vimdiff' Returns the modified 'before' as a string  How to use vimdiff: https:... |
| `vim_paste()` | 51669 | Gets the string in the 0th register of vim and returns it Looking for a line like \|3,1,0,1,7,0,1613... |
| `is_valid_int()` | 51676 | *(No description)* |
| `is_valid_line()` | 51682 | *(No description)* |
| `get_lines()` | 51697 | *(No description)* |
| `get_timestamp()` | 51710 | *(No description)* |
| `strip_braces()` | 51737 | Gets the string in the 0th register of vim and returns it Writing a line like \|3,1,0,1,7,0,16135933... |
| `vim_copy()` | 51755 | Gets the string in the 0th register of vim and returns it Writing a line like \|3,1,0,1,7,0,16135933... |
| `get_timestamp()` | 51765 | *(No description)* |
| `__init__()` | 51816 |  FP (file paste)  data = web_paste() return gather_args_call(_paste_path_from_bundle, data,path=path... |
| `__repr__()` | 51822 |  FP (file paste)  data = web_paste() return gather_args_call(_paste_path_from_bundle, data,path=path... |
| `_paste_path_from_bundle()` | 51830 | *(No description)* |
| `_copy_path_to_bundle()` | 51880 | Returns a list of all local ip addresses currently in use on your local network Code from: https://s... |
| `get_all_local_ip_addresses()` | 51890 | Returns a list of all local ip addresses currently in use on your local network Code from: https://s... |
| `pinger()` | 51903 | Do Ping :param job_q: :param results_q: :return: |
| `get_my_ip()` | 51926 | Find my IP address :return: |
| `ip_to_mac_address()` | 51979 | EXAMPLE: >>> [ip_to_mac_address(x) for x in get_all_local_ip_addresses()] ans = ['70:4d:7b:e4:c7:b8'... |
| `ip_to_host_name()` | 51991 | Will attempt to get the name of the host computer with the given IP address If no name is returned, ... |
| `get_mac_address_vendor()` | 52008 | EXAMPLE: >>> get_my_mac_address() ans = 30:5a:3a:7a:e4:a8 >>> get_mac_address_vendor(ans) ans = ASUS... |
| `autoimportable_module()` | 52022 | Records mouse and keyboard actions, and allows you to play them back.  Please see a youtube tutorial... |
| `__getattribute__()` | 52024 | Records mouse and keyboard actions, and allows you to play them back.  Please see a youtube tutorial... |
| `PynputCasette()` | 52032 | Records mouse and keyboard actions, and allows you to play them back.  Please see a youtube tutorial... |
| `old_and_new_text()` | 52082 | *(No description)* |
| `get_progress_text()` | 52120 | *(No description)* |
| `_fart()` | 52187 | Useful when you're searching for some keyword in a library, but not every submodule has been importe... |
| `import_all_submodules()` | 52196 | Useful when you're searching for some keyword in a library, but not every submodule has been importe... |
| `try_import()` | 52215 | *(No description)* |
| `helper()` | 52240 | Takes a url, and returns a string with the ip that's found EXAMPLE: >> dns_lookup('google.com') ans ... |
| `dns_lookup()` | 52253 | Takes a url, and returns a string with the ip that's found EXAMPLE: >> dns_lookup('google.com') ans ... |
| `__init__()` | 52271 | *(No description)* |
| `push()` | 52273 | *(No description)* |
| `pop()` | 52278 | *(No description)* |
| `_fdt_for_command_line()` | 52282 | *(No description)* |
| `_fzf_multi_grep()` | 52294 | *(No description)* |
| `should_read()` | 52336 | *(No description)* |
| `text_lines_walk()` | 52356 | *(No description)* |
| `mute()` | 52359 | *(No description)* |
| `unwarped_perspective_contour()` | 52465 | Transform contour points using perspective transformation. The sister function is rp.unwarped_perspe... |
| `_pip_import_depth_pro()` | 52551 | *(No description)* |
| `_get_depth_pro_model()` | 52597 | *(No description)* |
| `run_depth_pro()` | 52627 | Estimate depth from a single RGB image using the DepthPro model.  DepthPro is Apple's monocular dept... |
| `_get_cotracker_model()` | 52688 | Loads and caches the CoTracker model.  Args: device: The torch device to load the model onto. If Non... |
| `run_cotracker()` | 52720 | Runs the CoTracker model on a video for object tracking. CoTracker3 is a transformer-based model tha... |
| `run_tapnet()` | 52847 | Runs the TAPNext/TAPIR model on a video for point tracking. TAPNext is a transformer-based model tha... |
| `_ensure_tapnet_installed()` | 52944 | Gets the code and checkpoints for tapnet models is varargs like "tapir", "bootstapir", or "tapnext" ... |
| `_pip_import_pyflow()` | 52999 | This function attempts to import the 'pyflow' module. If the import fails, it will clone the 'pyflow... |
| `get_optical_flow_via_pyflow()` | 53038 | Returns a [2, H, W] numpy array for dx and dy respectively, measured in pixels  Uses pyflow: https:/... |
| `cv_optical_flow()` | 53148 | Calculate the optical flow between two frames using the specified algorithm.  Args: frame_a (np.ndar... |
| `helper()` | 53384 | *(No description)* |
| `optical_flow_to_arrow_grid()` | 53472 | Visualize optical flow as a grid of arrows on an optional background image.  Args: dx (numpy.ndarray... |
| `_get_apriltag_detector()` | 53601 | *(No description)* |
| `__init__()` | 53609 | Apriltags are a particular type of AR Marker, which looks like a QR Code Apriltags are lower resolut... |
| `__hash__()` | 53613 | Apriltags are a particular type of AR Marker, which looks like a QR Code Apriltags are lower resolut... |
| `__eq__()` | 53615 | Apriltags are a particular type of AR Marker, which looks like a QR Code Apriltags are lower resolut... |
| `center()` | 53618 | Apriltags are a particular type of AR Marker, which looks like a QR Code Apriltags are lower resolut... |
| `__repr__()` | 53620 | Apriltags are a particular type of AR Marker, which looks like a QR Code Apriltags are lower resolut... |
| `detect_apriltags()` | 53623 | Apriltags are a particular type of AR Marker, which looks like a QR Code Apriltags are lower resolut... |
| `get_apriltag_image()` | 53680 | Returns an image with the apriltag corresponding to the given value Please note: the output images a... |
| `get_apriltag_images()` | 53722 | Generate multiple AprilTag images. Plural version of get_apriltag_image.  Enhanced Documentation: Cr... |
| `_nbca()` | 53852 | This clears all outputs of a jupyter notebook file This is useful when the file gets so large it cra... |
| `do_path()` | 53855 | This clears all outputs of a jupyter notebook file This is useful when the file gets so large it cra... |
| `clear_jupyter_notebook_outputs()` | 53869 | This clears all outputs of a jupyter notebook file This is useful when the file gets so large it cra... |
| `_initialize_bokeh()` | 53899 | *(No description)* |
| `histogram_via_bokeh()` | 54028 | Uses the Bokeh library to display an interactive histogram in an IPython notebook Only works in IPyt... |
| `get_git_branch()` | 54105 | Gets the current git branch name.  Args: path (str): The path to the git repository. Defaults to the... |
| `get_git_is_dirty()` | 54123 | Checks if the git repository has uncommitted changes.  Args: path (str): The path to the git reposit... |
| `get_git_remote_url()` | 54141 | *(No description)* |
| `get_current_git_hash()` | 54158 | *(No description)* |
| `get_git_commit_message()` | 54168 | Returns the datetime of the latest commit in a Git repository.  Args: path: The path to the Git repo... |
| `get_git_commit_date()` | 54180 | Returns the datetime of the latest commit in a Git repository.  Args: path: The path to the Git repo... |
| `is_a_git_repo()` | 54206 | Returns False if it's not in a git repo, returns the root .git folder if it is pip_import('git') imp... |
| `get_git_repo_root()` | 54218 | Distills a GitHub URL to its base repository URL.  https://github.com/fperazzi/davis-2017/tree/main ... |
| `_get_repo_name_from_url()` | 54240 | Url should look like: https://github.com/gabrielloye/RNN-walkthrough/ https://github.com/gabrielloye... |
| `git_clone()` | 54280 | Git clones the repo at the given url to the specified path.  :param url: URL of the Git repository t... |
| `git_pull()` | 54312 | Git pulls the latest changes from the remote repository. _ensure_git_installed()  assert connected_t... |
| `get_git_info()` | 54329 | *(No description)* |
| `get_git_date_modified()` | 54355 | Retrieves the date when a file was last modified according to git, returning a datetime object. Rais... |
| `_autoformat_python_code_via_black()` | 54485 | Format a Python code snippet using the black macchiato tool.  Args: python_code_snippet (str): A str... |
| `autoformat_python_via_black_macchiato()` | 54493 | Format a Python code snippet using the black macchiato tool.  Args: python_code_snippet (str): A str... |
| `f()` | 54511 | *(No description)* |
| `f()` | 54518 | *(No description)* |
| `f()` | 54521 | *(No description)* |
| `f()` | 54526 | pip_import('macchiato') import macchiato import io  black_args = []  if max_line_length is not None:... |
| `autoformat_html_via_bs4()` | 54576 | Given a string of HTML, autoformats it pip_import('bs4') from bs4 import BeautifulSoup  soup = Beaut... |
| `add_trailing_commas()` | 54589 | https://github.com/asottile/add-trailing-comma  |
| `autoformat_json()` | 54600 | Formats a JSON string with specified indentation.  Parameters: - data (str, object): The JSON string... |
| `as_numpy_images()` | 54628 |  Will convert an array of images to BHWC np.ndarray form if it isn't already - supports BCHW torch t... |
| `as_pil_image()` | 54650 |  Will convert an a PIL images if it isn't already - supports BCHW torch tensors, numpy images, etc  ... |
| `as_pil_images()` | 54718 |  Will convert an array of images to PIL images if it isn't already - supports BCHW torch tensors, PI... |
| `as_numpy_image()` | 54722 |  Will convert an image to HWC np.ndarray form if it isn't already - supports CHW torch tensors, PIL ... |
| `as_numpy_video()` | 54751 | Convert video to NumPy THWC format from various input formats.  Enhanced Documentation: - Handles to... |
| `as_numpy_videos()` | 54777 | Convert batch of videos to NumPy BTHWC format.  Handles torch BTCHW → numpy BTHWC conversion for bat... |
| `as_torch_videos()` | 54801 |  Plural of rp.as_torch_video  import torch videos = [gather_args_call(as_torch_video, video) for vid... |
| `as_torch_images()` | 54809 |  Plural of rp.as_torch_image AKA rp.as_torch_video  import torch  if _is_numpy_array(images) or all(... |
| `as_torch_image()` | 54849 |  Converts an image to a floating point torch tensor in CHW form  if is_torch_tensor(image): return i... |
| `__init__()` | 55006 | *(No description)* |
| `__len__()` | 55019 | Returns the appropriate PyTorch device based on the available hardware and system configuration.  Th... |
| `__getitem__()` | 55022 | Returns the appropriate PyTorch device based on the available hardware and system configuration.  Th... |
| `_get_select_torch_device_lock_file()` | 55029 | Returns the appropriate PyTorch device based on the available hardware and system configuration.  Th... |
| `_torch_device_to_index()` | 55215 | Convert a given device specifier into its corresponding index.  The function handles multiple format... |
| `_waste_gpu()` | 55265 | *(No description)* |
| `waste_gpus()` | 55286 | Keeps all GPU's busy on a system, using as much VRAM as possible. Used for stress-testing. Should ta... |
| `set_cuda_visible_devices()` | 55305 | Sets the CUDA_VISIBLE_DEVICES environment variable.  This configuration restricts which GPUs are vis... |
| `get_cuda_visible_devices()` | 55371 |  Returns a list of ints  import ast key = 'CUDA_VISIBLE_DEVICES' if key in os.environ: out = os.envi... |
| `run_removestar()` | 55388 | Takes something like: from numpy import * from rp import * asarray([1,2,3]) display_image(x) And tur... |
| `qualify_imports()` | 55484 | EXAMPLE: |
| `_qualify_imports()` | 55530 | *(No description)* |
| `__init__()` | 55537 | *(No description)* |
| `get_full_module_name()` | 55541 | *(No description)* |
| `leave_ImportFrom()` | 55550 | *(No description)* |
| `leave_Call()` | 55570 | Handle function calls - this is where we want to qualify star import names. # Only process if the fu... |
| `leave_Name()` | 55591 | Determine if a name is likely a function from a module (not a built-in). # Don't qualify obvious bui... |
| `_is_likely_module_function()` | 55603 | Determine if a name is likely a function from a module (not a built-in). # Don't qualify obvious bui... |
| `get_star_modules()` | 55627 | EXAMPLE: |
| `remove_fstrings()` | 55642 | Removes f-strings, using str.format notation instead. This is good for making code backwards-compati... |
| `refactor_flynt()` | 55696 | Refactor Python code using flynt to convert to f-strings.  Args: code: Python source code to refacto... |
| `__init__()` | 55831 |  Returns a list of paths to all fonts of specified types on this computer.  Enhanced Documentation: ... |
| `__iter__()` | 55835 |  Returns a list of paths to all fonts of specified types on this computer.  Enhanced Documentation: ... |
| `__next__()` | 55838 |  Returns a list of paths to all fonts of specified types on this computer.  Enhanced Documentation: ... |
| `__len__()` | 55841 |  Returns a list of paths to all fonts of specified types on this computer.  Enhanced Documentation: ... |
| `__repr__()` | 55844 |  Returns a list of paths to all fonts of specified types on this computer.  Enhanced Documentation: ... |
| `get_system_fonts()` | 55848 |  Returns a list of paths to all fonts of specified types on this computer.  Enhanced Documentation: ... |
| `__init__()` | 55965 | *(No description)* |
| `__contains__()` | 55969 | *(No description)* |
| `__iter__()` | 55972 | *(No description)* |
| `__len__()` | 55975 | *(No description)* |
| `add()` | 55978 | *(No description)* |
| `discard()` | 55981 | *(No description)* |
| `__getitem__()` | 55985 | Allows `my_set.item = True` assignments for new items, but raises an error if the attribute or metho... |
| `__setitem__()` | 55988 | Allows `my_set.item = True` assignments for new items, but raises an error if the attribute or metho... |
| `__getattr__()` | 55998 | Allows `my_set.item = True` assignments for new items, but raises an error if the attribute or metho... |
| `__delattr__()` | 56001 | Allows `my_set.item = True` assignments for new items, but raises an error if the attribute or metho... |
| `__setattr__()` | 56004 | Allows `my_set.item = True` assignments for new items, but raises an error if the attribute or metho... |
| `__repr__()` | 56025 |  Like a read-only EasyDict - with a super simple implementation  #Note: This class is similar in fun... |
| `__init__()` | 56034 | *(No description)* |
| `__getattr__()` | 56047 | *(No description)* |
| `__dir__()` | 56055 | This function stretches or compresses a list to a given length using nearest-neighbor interpolation.... |
| `__contains__()` | 56059 | This function stretches or compresses a list to a given length using nearest-neighbor interpolation.... |
| `__repr__()` | 56062 | This function stretches or compresses a list to a given length using nearest-neighbor interpolation.... |
| `__getitem__()` | 56065 | This function stretches or compresses a list to a given length using nearest-neighbor interpolation.... |
| `list_transpose()` | 56204 | EXAMPLE: >>> list_transpose([[1,2,3],[4,5,6]]) ans = [[1, 4], [2, 5], [3, 6]]  TODO: Fix this behavi... |
| `dict_transpose()` | 56228 | Transposes a nested dictionary, reversing the roles of keys and sub-keys. Skips keys that do not exi... |
| `list_dict_transpose()` | 56289 | Transpose a list of dictionaries or a dictionary of lists.  If the input is a dictionary of lists, t... |
| `broadcast_lists()` | 56417 | Broadcasts multiple lists to the same length, and turns non-lists into lists  Args: *lists: The sequ... |
| `broadcast_kwargs()` | 56485 | Broadcasts a dict of lists to the same length, and turns non-lists into lists. Closely related to rp... |
| `dict_walk()` | 56559 | Recursively yield paths and values from a dictionary, including paths to empty dictionaries.  This f... |
| `should_traverse()` | 56614 | *(No description)* |
| `walk()` | 56617 | *(No description)* |
| `monkey_patch()` | 56638 | A decorator used to add a method to an object.  :param target: The object to which the method should... |
| `__repr__()` | 56652 | def patcher(func): |
| `patcher()` | 56657 | Adds the `func` method to the `target` object with the specified `name`. |
| `_inline_rp_code()` | 56664 | Extracts imports from Python code and returns them as a dictionary.  The dictionary has two top-leve... |
| `extract_imports()` | 56672 | Extracts imports from Python code and returns them as a dictionary.  The dictionary has two top-leve... |
| `remove_first_import_line()` | 56749 | *(No description)* |
| `get_code()` | 56760 | *(No description)* |
| `unarpy()` | 56779 | *(No description)* |
| `get_free_ram()` | 56800 | Get the amount of RAM currently free.  :return: The amount of free RAM in bytes. |
| `get_total_ram()` | 56810 | Get the total amount of RAM.  :return: The total amount of RAM in bytes. |
| `get_used_ram()` | 56820 | Get the amount of RAM currently in use.  :return: The amount of used RAM in bytes. |
| `_init_nvml()` | 56832 | *(No description)* |
| `_get_gpu_memory_info()` | 56839 | Returns the UUID of a GPU given its ID. If gpu_id is None, returns a list of UUIDs for all GPUs. Thi... |
| `_get_gpu_handle()` | 56847 | Returns the UUID of a GPU given its ID. If gpu_id is None, returns a list of UUIDs for all GPUs. Thi... |
| `get_gpu_uuid()` | 56853 | Returns the UUID of a GPU given its ID. If gpu_id is None, returns a list of UUIDs for all GPUs. Thi... |
| `get_gpu_count()` | 56878 | Returns the number of available GPUs.  Example: >>> get_gpu_count() 4 |
| `get_visible_gpu_ids()` | 56893 | Return all GPU's that are intended to be available to this process. If cuda_visible_devices is set, ... |
| `get_all_gpu_ids()` | 56909 |  If you are on a device with GPU's, returns [0, 1, 2, ... (num gpus - 1) ]   #If the CUDA_VISIBLE_DE... |
| `get_gpu_ids_used_by_process()` | 56921 | Get a list of all GPU's used by a given process. Defaults to the current process. if pid is None: pi... |
| `get_gpu_pids()` | 56931 | Returns a list of process IDs running on the given GPU.  Args: gpu_id (int): The ID of the GPU. exis... |
| `get_free_vram()` | 56979 | Returns the amount of free VRAM for a GPU given its ID. The returned value is in bytes. If gpu_id is... |
| `get_total_vram()` | 57001 | Returns the total amount of VRAM for a GPU given its ID. The returned value is in bytes. If gpu_id i... |
| `get_used_vram()` | 57022 | Returns the amount of used VRAM for a GPU given its ID or for a specific process ID. If a process ID... |
| `none_to_zero()` | 57042 | *(No description)* |
| `get_gpu_with_most_free_vram()` | 57071 | Returns the GPU ID with the nth most free VRAM. If there is a tie, the function will prioritize GPUs... |
| `get_gpu_name()` | 57090 | Returns the name of a GPU given its ID. The returned value is a string. If gpu_id is None, returns a... |
| `get_vram_used_by_current_process()` | 57114 | Returns the amount of VRAM used by the current process for each GPU or a specific GPU.  Args: gpu_id... |
| `get_gpu_temperature()` | 57134 | Returns the temperature of a GPU in celcius given its ID. If gpu_id is None, returns a list of tempe... |
| `get_gpu_utilization()` | 57157 | Returns a % of how busy a GPU is.  Returns the utilization of a GPU in percentage given its ID. If g... |
| `ram_to_string()` | 57326 | *(No description)* |
| `_get_kernel_to_pid_mapping()` | 57385 | *(No description)* |
| `get_all_pids_and_their_commands()` | 57387 | *(No description)* |
| `_get_all_notebook_sessions_via_ipybname()` | 57431 | Gets a ton of information about all running Jupyter notebook instances  Took about .02 seconds to ex... |
| `delaunay_interpolation_weights()` | 57598 | This function calculates the interpolation weights for each query point based on the Delaunay triang... |
| `get_total_disk_space()` | 57683 | Returns the total size of your hard drive in bytes import shutil total, used, free = shutil.disk_usa... |
| `get_used_disk_space()` | 57689 | Returns the amount of your hard drive that holds data in bytes import shutil total, used, free = shu... |
| `get_free_disk_space()` | 57695 | Returns the amount of your hard drive that doesnt hold data in bytes import shutil total, used, free... |
| `_ensure_uv_installed()` | 57701 |  Clone of pip that's much faster  try: import uv except ImportError: pip_install("uv", backend="pip"... |
| `pip_install()` | 57710 |  Try to install a python package   assert isinstance(pip_args,str),'pip_args must be a string like "... |
| `update_rp()` | 57741 |  Update this package  if input_yes_no("Are you sure you'd like to try updating rp? (You will need to... |
| `module_exists()` | 57747 | Check if a Python module exists without importing it.  Args: module_name (str): The name of the modu... |
| `pip_install_multiple()` | 57772 | Install multiple packages via pip.  If shotgun is True: Try to install each package individually. If... |
| `fix_package()` | 57802 | *(No description)* |
| `__init__()` | 58056 | TODO: Make this function only request sudo if we need it. Otherwise it's a nuisance. TODO: Add an "a... |
| `add()` | 58060 | TODO: Make this function only request sudo if we need it. Otherwise it's a nuisance. TODO: Add an "a... |
| `__contains__()` | 58063 | TODO: Make this function only request sudo if we need it. Otherwise it's a nuisance. TODO: Add an "a... |
| `delete()` | 58066 | TODO: Make this function only request sudo if we need it. Otherwise it's a nuisance. TODO: Add an "a... |
| `pip_import()` | 58074 | TODO: Make this function only request sudo if we need it. Otherwise it's a nuisance. TODO: Add an "a... |
| `offer_to_blacklist()` | 58142 | *(No description)* |
| `_import_module()` | 58171 |  Can import a module name with multiple .'s in it, like rp.git.CommonSource. __import__ can't do tha... |
| `git_import()` | 58176 | Attempts to import a module from rp.git.some_module_name If it doesn't exist, it will try to clone i... |
| `check_pip_requirements()` | 58228 | Test availability of required packages from given requirements file.  Args: file (str, optional): Pa... |
| `get_mask_iou()` | 58332 | Calculates the IOU (intersection over union) of multiple binary masks masks=detuple(masks) assert al... |
| `fuzzy_match()` | 58352 | Returns True if each element in array can be found in sequence (though not necessarily consecutively... |
| `get_only()` | 58432 | Return the sole item of the collection. assert len(collection) == 1, "Expected length of 1" return n... |
| `killport()` | 58438 | *(No description)* |

## Architectural Analysis

### Utilities Foundation Architecture

The utilities form RP's architectural foundation, providing:

1. **Type System**: Comprehensive `is_*` and `as_*` functions for type checking/conversion
2. **Data Structures**: Enhanced operations on lists, dicts, tuples
3. **Functional Primitives**: Core functional programming building blocks
4. **Random Operations**: Complete random number and selection utilities
5. **Validation Layer**: Input validation and sanitization functions

### Key Patterns  
- **Universal Converters**: `as_*` functions handle any reasonable input
- **Type Validators**: `is_*` functions provide reliable type checking
- **Data Transformers**: Functions that reshape, filter, and transform data
- **Helper Utilities**: Small, focused functions that support larger operations

## Function Relationships

### Batch Operations
- `with_drop_shadow()` ↔ `with_drop_shadows()`
- `with_alpha_outline()` ↔ `with_alpha_outlines()`
- `randint()` ↔ `randints()`
- `random_float()` ↔ `random_floats()`
- `with_alpha_checkerboard()` ↔ `with_alpha_checkerboards()`
- ... and 38 more

### Multiplexing
- `text_to_speech()` ↔ `text_to_speech_via_apple()`
- `text_to_speech()` ↔ `text_to_speech_via_google()`
- `get_english_synonyms()` ↔ `get_english_synonyms_via_nltk()`
- `get_english_synonyms()` ↔ `get_english_synonyms_via_datamuse()`

### Type Conversion
- `is_form()` ↔ `as_form()`
- `is_complex_vector()` ↔ `as_complex_vector()`
- `is_points_array()` ↔ `as_points_array()`
- `is_cv_contour()` ↔ `as_cv_contour()`
- `is_grayscale_image()` ↔ `as_grayscale_image()`
- ... and 8 more

