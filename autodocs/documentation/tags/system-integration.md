# RP Library: System Integration

Interface layer between Python and the operating system: files, terminals, processes, and external tools.

**Total Functions: 193**

## Function Inventory

| Function | Line | Description |
|----------|------|-------------|
| `get_process_cwd()` | 915 | Get the result of 'cd' in a shell. This is the current folder where save or load things by default. ... |
| `get_current_directory()` | 922 | Get the result of 'cd' in a shell. This is the current folder where save or load things by default. ... |
| `set_current_directory()` | 987 | Temporarily CD into a directory Example: print(get_current_directory()) with SetCurrentDirectoryTemp... |
| `terminal_supports_ansi()` | 1448 | Enhanced Documentation: Checks if the current terminal supports ANSI escape sequences for colors and... |
| `terminal_supports_unicode()` | 1477 | Enhanced Documentation: Checks if the current terminal supports Unicode characters for display. On W... |
| `_get_local_clipboard_string()` | 2516 | Copies a string to the clipboard so you can paste it later First tries to copy the string to the sys... |
| `_set_local_clipboard_string()` | 2523 | Copies a string to the clipboard so you can paste it later First tries to copy the string to the sys... |
| `string_to_clipboard()` | 2527 | Copies a string to the clipboard so you can paste it later First tries to copy the string to the sys... |
| `_copy_text_over_terminal()` | 2580 | Encodes a given string in base64 and sends it to the terminal to be copied to the clipboard via OSC ... |
| `string_from_clipboard()` | 2617 | Pastes the string from the clipboard and returns that value First tries to paste the string from the... |
| `accumulate_clipboard_text()` | 2632 | Automatically accumulates and combines text copied to the clipboard.  This function continuously mon... |
| `run_as_new_thread()` | 5431 | Used when we simply don't need/want all the complexities of the threading module. An anonymous threa... |
| `run_as_new_process()` | 5450 | Used when we simply don't need/want all the complexities of the multiprocessing module An anonymous ... |
| `_erase_terminal_line()` | 5525 |  erase and go to beginning of line https://stackoverflow.com/questions/5290994/remove-and-replace-pr... |
| `load_files()` | 5529 | Load a list of files with optional multithreading.  - load_file (function): A function to load a sin... |
| `_load_files()` | 5574 | *(No description)* |
| `_load_file()` | 5635 | *(No description)* |
| `load_image_from_clipboard()` | 5790 |  #Grab an image copied from your clipboard  #TODO: Use the "copykitten" library to paste images pip_... |
| `_paste_from_clipboard()` | 5813 | Auto-detect clipboard contents and return appropriate type. Returns string for text content, image o... |
| `_copy_image_to_clipboard_via_pyjpgclipboard()` | 5834 | (This function works fine! But it didnt support RGBA images so it's obsolete now)  Takes an image or... |
| `_copy_image_to_clipboard_via_copykitten()` | 5861 | Copies an image to the system clipboard Can handle RGBA images https://github.com/Klavionik/copykitt... |
| `copy_image_to_clipboard()` | 5876 | Copies an image to the system clipboard  EXAMPLE:  >>> ans = get_youtube_video_thumbnail('https://ww... |
| `load_image_from_file()` | 6130 |  Can try opencv as a fallback if this ever breaks  assert file_exists(file_name),'No such image file... |
| `_load_image_from_file_via_PIL()` | 6165 | NOTE if this method fails try the following function: imageio.plugins.freeimage.download() #https://... |
| `_load_image_from_file_via_imageio()` | 6175 | NOTE if this method fails try the following function: imageio.plugins.freeimage.download() #https://... |
| `_load_image_from_file_via_scipy()` | 6185 | *(No description)* |
| `_load_image_from_file_via_opencv()` | 6189 | Url should either be like http://website.com/image.png or like data:image/png;base64,iVBORw0KGgoAAAA... |
| `is_valid_openexr_file()` | 6297 | Returns True iff the file path points to an exr file |
| `_get_files_from_paths()` | 7154 | Takes a folder, a list of files, or a list of files and folders as input - all of which can be globb... |
| `convert_image_file()` | 7173 | Converts an image file to a specified format and saves it to the provided output folder. It can also... |
| `convert_image_files()` | 7249 | Converts multiple image files to a specified format and saves them to the provided output folder. Th... |
| `load_mp3_file()` | 7888 | Takes an mp3 file path, and returns a bunch of samples as a numpy array Returns floating-point sampl... |
| `load_wav_file()` | 7912 | Takes a wav file path, and returns a bunch of samples as a numpy array Returns floating-point sample... |
| `load_sound_file()` | 7937 | Returns the contents of a sound file at file_path as a numpy array of floats in the range [-1, 1] sa... |
| `play_sound_file()` | 8036 | THIS Function is an abstraction of playing sound files. Just plug in whatever method works on your c... |
| `play_sound_file_via_afplay()` | 8058 | Use stop_sound to stop it. If parallel==False, the code will pause until the song is finished playin... |
| `play_sound_file_via_pygame()` | 8080 | Old because it uses the pygame.mixer.sound instead of pygame.mixer.music, which accepts more file ty... |
| `convert_audio_file()` | 8166 | Convert an audio file to a different format using FFmpeg.  Args: input_file (str): Path to the input... |
| `display_qr_code_in_terminal()` | 8941 | EXAMPLE: #Done in Alacritty or the default Mac Terminal display_qr_code_in_terminal('https://google.... |
| `display_website_in_terminal()` | 8961 | Enhanced Documentation:  Fetches and displays a website's content as formatted text in the terminal.... |
| `histogram_in_terminal()` | 9258 | Right now this function is very simple (it doesnt let you specify the number of bins, for example) I... |
| `line_graph_in_terminal()` | 9438 | This is mainly here as a simple reference for how to create a line-graph with matplotlib.pyplot. The... |
| `process_data()` | 10572 | out_args, out_kwargs = gather_args(func, *args, frames_back=frames_back+1, **kwargs) return func(*ou... |
| `load_image_from_webcam()` | 13232 | If your camera supports multiple resolutions, input the dimensions in the height and width parameter... |
| `load_webcam_stream()` | 13289 | Grabs a screenshot from the main monitor using the Multiple Screen Shots (MSS) Library Returns it as... |
| `load_image_from_screenshot_via_mss()` | 13293 | Grabs a screenshot from the main monitor using the Multiple Screen Shots (MSS) Library Returns it as... |
| `load_image_from_screenshot()` | 13319 | Grabs a screenshot from the main monitor Returns it as a RGB byte image  EXAMPLE:  >>> while True: .... |
| `load_screenshot_stream()` | 13334 |  EXAMPLE:  >>> while True: ...     display_video(cv_resize_images(load_screenshot_stream(), size=.25... |
| `_load_image_from_screenshot_via_pyscreenshot()` | 13346 | REPLACED BY load_image_from_screenshot WHICH IS MUCH FASTER (This still works as a slow version thou... |
| `_load_image_from_webcam_in_jupyter_notebook()` | 13359 | VIDEO_HTML =  <video autoplay width=800 height=600></video> <script> var video = document.querySelec... |
| `string_to_text_file()` | 13653 | string_to_text_file(file_path, string) writes text file  Enhanced Documentation: Writes a string to ... |
| `save_text_file()` | 13710 | text_file_to_string(file_path) reads text file  Enhanced Documentation: This is RP's primary text fi... |
| `text_file_to_string()` | 13716 | text_file_to_string(file_path) reads text file  Enhanced Documentation: This is RP's primary text fi... |
| `load_file_lines()` | 13800 |  Returns all the lines in a file  return line_split(text_file_to_string(file_path, use_cache))  def ... |
| `save_file_lines()` | 13804 | Save an iterable of lines to a text file.  Convenient function for saving lists/collections of text ... |
| `load_text_files()` | 13843 | Plural of text_file_to_string Please see load_files and rp_iglob for more information Yields the str... |
| `append_line_to_file()` | 13856 | Adds a line to the end of a text file, or creates a new text file if none exists.  Enhanced Document... |
| `load_yaml_file()` | 14314 | EXAMPLE: >>> load_yaml_file('alphablock_without_ssim_256.yaml') ans = {'max_iter': 300000, 'batch_si... |
| `load_yaml_files()` | 14331 | Plural of load_yaml_file Please see load_files and rp_iglob for more information Yields the jsons as... |
| `load_dyaml_file()` | 14554 |  Load a dyaml file (a yaml file with some additional syntax features I added). Stands for "Delta Yam... |
| `touch_file()` | 14560 | Equivalent to the 'touch' command - creates a file if it doesnt exist and if it does updates its dat... |
| `get_terminal_size()` | 15891 | From http://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python/14422... |
| `get_terminal_width()` | 15949 |  Attempts to return the width of the current TTY in characters - otherwise it will return 80 by defa... |
| `get_terminal_height()` | 15952 |  Attempts to return the height of the current TTY in characters - otherwise it will return 25 by def... |
| `formula_as_file()` | 17182 | Uses unicode, and is black-and-white EXAMPLE: while True: display_image_in_terminal(load_image_from_... |
| `display_image_in_terminal()` | 17195 | Uses unicode, and is black-and-white EXAMPLE: while True: display_image_in_terminal(load_image_from_... |
| `display_image_in_terminal_color()` | 17249 | Will attempt to draw a color image in the terminal This is slower than display_image_in_terminal, an... |
| `display_image_in_terminal_imgcat()` | 17320 | Can display images in some terminals as actual images  Works in: iterm2 wezterm tmux (if configured ... |
| `display_video_in_terminal_color()` | 17360 | Display a video in the terminal with a progress bar.  Args: frames (list): List of frames to display... |
| `get_source_file()` | 18609 | Might throw an exception |
| `_rp_show_custom_line_profile()` | 19322 | Display custom line profiler results with visual enhancements TODO: This is a work in progress. Curr... |
| `get_last_line_profile_results()` | 19458 | Get the results from the most recent line profiling session global _prev_line_profiler return _prev_... |
| `_load_pyin_settings_file()` | 19664 | *(No description)* |
| `_save_pyin_settings_file()` | 19688 | *(No description)* |
| `_delete_pyin_settings_file()` | 19692 | *(No description)* |
| `number_of_lines_in_terminal()` | 20144 | Gets the number of lines a string would appear to have when printed in a terminal, assuming the term... |
| `number_of_lines_in_file()` | 20160 | Quickly count the nubmer of lines in a given file. It's 5-10x faster than text_file_to_string(filena... |
| `_all_files_listed_in_exception_traceback()` | 20174 | *(No description)* |
| `process_line()` | 20184 | *(No description)* |
| `is_image_file()` | 20437 | Check if file path points to an image file based on extension/mimetype.  Checks file extension and m... |
| `is_video_file()` | 20482 | Check if a file is a video file based on MIME type detection.  Enhanced Documentation: Determines if... |
| `is_sound_file()` | 20534 | Returns True iff the file path is a UTF-8 file Faster than trying to use text_file_to_string(path), ... |
| `is_utf8_file()` | 20537 | Returns True iff the file path is a UTF-8 file Faster than trying to use text_file_to_string(path), ... |
| `display_file_tree()` | 20612 | Display a visual tree structure of files and directories, similar to the Unix 'tree' command.  Enhan... |
| `is_hidden_file()` | 20666 | *(No description)* |
| `_load_text_from_file_or_url()` | 20867 | *(No description)* |
| `check_release_file()` | 21122 | *(No description)* |
| `_get_processor_name()` | 21448 | *(No description)* |
| `process_paragraph()` | 21477 | *(No description)* |
| `_profile_vim_startup_plugins()` | 21868 | Profile Vim startup plugins to identify performance bottlenecks.  Enhanced Documentation: ==========... |
| `_view_markdown_in_terminal()` | 21920 | *(No description)* |
| `_convert_powerpoint_file()` | 21949 | *(No description)* |
| `pseudo_terminal()` | 22071 | An interactive terminal session, powered by RP  Enhanced Documentation: RP's flagship interactive te... |
| `file_size_key()` | 24657 | *(No description)* |
| `set_process_title()` | 26286 | *(No description)* |
| `get_process_title()` | 26289 | *(No description)* |
| `get_file_size()` | 26518 | *(No description)* |
| `human_readable_file_size()` | 26539 | Given a file size in bytes, return a string that represents how large it is in megabytes, gigabytes ... |
| `string_to_file_size()` | 26572 | Converts a human-readable file size string back to the number of bytes, handling various units and t... |
| `postprocess()` | 26645 |  Expands the condensed dictionary of file size units.  expanded_units = {} for key, value in units_d... |
| `get_file_size()` | 26711 | Gets the filesize of the given path Can also get the size of folders If human_readable is True, it w... |
| `get_process_memory()` | 27356 | Returns the username associated with the given process ID (pid). Made by ChatGPT: https://sharegpt.c... |
| `get_process_username()` | 27366 | Returns the username associated with the given process ID (pid). Made by ChatGPT: https://sharegpt.c... |
| `get_process_id()` | 27400 |  Get the current process id, aka pid  import os return os.getpid()  def get_process_exists(pid: int)... |
| `get_process_exists()` | 27405 | *(No description)* |
| `get_process_start_date()` | 27434 | Given a process ID, returns a datetime object of when it started if pid is None: pid=get_process_id(... |
| `kill_process()` | 27456 | Send a signal to a process identified by its PID.  Args: pid (int): Process ID to which the signal i... |
| `kill_processes()` | 27500 | Plural of rp.kill_process pids = detuple(pids) for pid in pids: try: kill_process(pid) except Except... |
| `search_processes()` | 27511 | Search for processes containing pattern in their command.  Args: pattern: String to search for in pr... |
| `ring_terminal_bell()` | 27598 |  Lets the terminal make a little noise. You've probably heard this sound at least once before on you... |
| `clear_terminal_screen()` | 27612 |  Will clear the screen of a tty  print(end="\033[0;0H\033[2J")#https://www.csie.ntu.edu.tw/~r92094/c... |
| `file_cache_call()` | 30458 | Caches the result of a function call to a file. If the file exists, return its contents. Otherwise, ... |
| `file_cache_wrap()` | 30520 | Decorator that wraps a function with file_cached_call.  Notes: For intermediate math results, consid... |
| `_get_file_path()` | 32747 | If given a url, get a file path that can be used for things #TODO: Use this to make strip_file_exten... |
| `strip_file_extension()` | 32757 | 'x.png'        --> 'x' 'text.txt'     --> 'text' 'text'         --> 'text' 'text.jpg.txt' --> 'text.... |
| `strip_file_extensions()` | 32769 | 'x.png'        --> 'png' 'text.txt'     --> 'txt' 'text'         --> '' 'text.jpg.txt' --> 'txt' 'a/... |
| `get_file_extension()` | 32773 | 'x.png'        --> 'png' 'text.txt'     --> 'txt' 'text'         --> '' 'text.jpg.txt' --> 'txt' 'a/... |
| `get_file_extensions()` | 32813 | Replaces or adds a file extension to a path  If extension is blank, and replace=False, path won't be... |
| `with_file_extension()` | 32816 | Replaces or adds a file extension to a path  If extension is blank, and replace=False, path won't be... |
| `with_file_extensions()` | 32895 | Returns the path with a new file name, keeping the old file extension If the file extension in 'name... |
| `with_file_name()` | 32907 | Returns the path with a new file name, keeping the old file extension If the file extension in 'name... |
| `has_file_extension()` | 33142 | Enhanced Documentation: Checks whether a file path has any file extension.  Args: file_path (str): P... |
| `get_all_files()` | 33442 |  Like get_all_files, but only returns image files. This function is just sugar.   #TODO: Once get_al... |
| `get_all_image_files()` | 33445 |  Like get_all_files, but only returns image files. This function is just sugar.   #TODO: Once get_al... |
| `get_all_runnable_python_files()` | 33459 | Retrieve all runnable Python files from a specified folder.  A runnable Python file is defined as a ... |
| `_os_listdir_files()` | 33541 | like get_all_files, but returns only file names and is a little faster https://stackoverflow.com/que... |
| `get_random_file()` | 33601 | Returns the paths of random files in that folder If the folder is None, returns the name of a random... |
| `get_random_files()` | 33612 | Returns the paths of random files in that folder If the folder is None, returns the name of a random... |
| `launch_terminal_in_colab()` | 35996 | Launches a full terminal right inside of google colab, right in the notebook itself! Note: You might... |
| `_moviepy_VideoFileClip()` | 37144 |  Moviepy 2 has breaking changes! They moved a class. See https://zulko.github.io/moviepy/getting_sta... |
| `_get_video_file_duration_via_moviepy()` | 37162 | Returns the duration of a video file, in seconds https://stackoverflow.com/questions/3844430/how-to-... |
| `get_video_file_duration()` | 37170 |  Returns a float, representing the total video length in seconds  path=get_absolute_path(path) #This... |
| `_get_video_file_framerate_via_moviepy()` | 37180 |  Given a (str) path to a video file, returns a number (framerate)  path = get_absolute_path(path) #I... |
| `_get_video_file_framerate_via_ffprobe()` | 37192 | Slower than _get_video_file_framerate_via_moviepy but no extra python dependencies Given a (str) pat... |
| `get_video_file_framerate()` | 37228 |  Given a (str) path to a video file, returns a number (framerate)  try: pip_import('moviepy')  #Ning... |
| `add_audio_to_video_file()` | 38077 | Add audio to a video file without recompressing the video.  This function uses FFmpeg to add audio f... |
| `change_video_file_framerate()` | 38157 | Change the framerate of a video without recompressing or changing the audio. This function uses FFmp... |
| `change_video_file_framerates()` | 38214 | Concatenate multiple MP4 files with zero degradation (no recompression).  Args: input_files (list): ... |
| `concat_mp4_files()` | 38218 | Concatenate multiple MP4 files with zero degradation (no recompression).  Args: input_files (list): ... |
| `directory_exists()` | 38286 | Check if a path points to an existing file.  Enhanced Documentation: This is a fundamental file syst... |
| `file_exists()` | 38298 | Check if a path points to an existing file.  Enhanced Documentation: This is a fundamental file syst... |
| `delete_file()` | 38508 | Deletes a file at a given path.  Args: path (str): Path to the file. permanent (bool, optional): If ... |
| `delete_files()` | 38651 | #Chooses between copy_directory and copy_file, whichever makes more sense. #If extract is True, it w... |
| `copy_directory()` | 38718 | Recursively copy a directory.  If extract is True, it will copy only the contents of the folder to t... |
| `get_home_directory()` | 38780 | Returns the ~ directory - aka the user's home directory. Works cross-platform. |
| `copy_file()` | 38801 | *(No description)* |
| `make_directory()` | 38950 | Will make a directory if it doesn't allready exist. If it does already exist, it won't throw an erro... |
| `make_parent_directory()` | 39034 | Enhanced Documentation:  Creates the parent directory of the specified file or directory path. Usefu... |
| `take_directory()` | 39095 | Create multiple directories. Plural version of make_directory.  Enhanced Documentation: Creates all ... |
| `delete_all_paths_in_directory()` | 39136 | Joins given paths, which can be a combination of strings and non-string iterables (like lists, tuple... |
| `delete_all_files_in_directory()` | 39141 | Joins given paths, which can be a combination of strings and non-string iterables (like lists, tuple... |
| `preprocess_frame()` | 39477 | *(No description)* |
| `edit_image_in_terminal()` | 40488 | Silly (but really fun) function that launches mspaint on an image in the terminal Not very practical... |
| `open_file_with_default_application()` | 41769 | Open a file or folder with the OS's default application EXAMPLE: open_file_with_default_application(... |
| `get_cache_file_path()` | 42341 | r Computes a cache file path for the provided input It is a pure function, and uses no system calls ... |
| `get_cache_file_paths()` | 42422 | Plural of get_cache_file_path, supporting a `lazy` option func = gather_args_bind(get_cache_file_pat... |
| `input_select_file()` | 43207 | I use this to select arduinos when I want to connect to one with a serial port After this, I general... |
| `temporary_file_path()` | 43250 | Returns the path of a temporary, writeable file (No more pesky "don't have permission to write" erro... |
| `_ensure_filebrowser_installed()` | 44262 | https://filebrowser.org/installation  system_commands = get_system_commands()  if "filebrowser" in s... |
| `_disable_terminal_mouse_reporting()` | 44312 | Disables terminal mouse reporting/tracking modes that can cause unwanted output like [200~[<64;106;4... |
| `_terminal_move_cursor_to_top_left()` | 44332 | Prints ANSI escape sequence to move cursor to the top-left position of the terminal. |
| `_terminal_move_cursor_to_bottom_left()` | 44340 | Prints ANSI escape sequence to move cursor to the bottom row and creates a new line. |
| `_terminal_move_cursor_to_bottom_and_new_line()` | 44344 | Prints ANSI escape sequence to move cursor to the bottom row and creates a new line. |
| `commit_process()` | 44412 | *(No description)* |
| `_configure_filebrowser()` | 44453 | Check if a port is already in use.  Args: port (int): The port number to check.  Returns: bool: True... |
| `_run_filebrowser()` | 44457 | Check if a port is already in use.  Args: port (int): The port number to check.  Returns: bool: True... |
| `get_process_using_port()` | 44545 | Gets the process ID (PID) using the specified port.  Args: port: The port number. strict: If True, r... |
| `process_command()` | 45341 | *(No description)* |
| `make_zip_file_from_folder()` | 46174 | Creates a .zip file on your hard drive. Zip the contents of some src_folder and return the output zi... |
| `extract_zip_file()` | 46206 | Extracts a zip or tar file to a specified folder. If the folder doesn't exist, it is created.  Param... |
| `get_image_file_dimensions()` | 46607 | Takes the file path of an image, and returns the image's (height, width) It does this without loadin... |
| `get_video_file_shape()` | 46627 | Returns the shape of the numpy tensor we would get with rp.load_video(path)  Args: path (str): Path ... |
| `get_video_file_num_frames()` | 46659 | Returns the number of frames in the video. |
| `get_video_file_height()` | 46666 | Returns the height of the video. |
| `get_video_file_width()` | 46673 | Returns the width of the video. |
| `bytes_to_file()` | 47366 | Enhanced Documentation:  Saves bytes data to a file at the specified path or a temporary location. A... |
| `file_to_bytes()` | 47438 | Enhanced Documentation:  Reads binary data from a file path or URL, returning raw bytes content. Sup... |
| `file_to_base64()` | 47513 | Load any Python object from a binary file using RP's object serialization.  Enhanced Documentation: ... |
| `file_to_object()` | 47517 | Load any Python object from a binary file using RP's object serialization.  Enhanced Documentation: ... |
| `object_to_file()` | 47586 | In some circumstances (with exotic args or kwargs) this could be better than the fire.Fire module  E... |
| `postprocess_path()` | 50833 | *(No description)* |
| `find_and_replace_text_files()` | 52047 |  Search and Replace text in files This function searches for all text files within the given paths a... |
| `file_will_change()` | 52087 | *(No description)* |
| `files_walk()` | 52312 | *(No description)* |
| `text_files_walk()` | 52344 | *(No description)* |
| `_display_filetype_size_histogram()` | 53766 | Enhanced Documentation: Displays a histogram showing total disk usage by file type (extension) in a ... |
| `_get_select_torch_device_lock_file()` | 55029 | Returns the appropriate PyTorch device based on the available hardware and system configuration.  Th... |
| `file_line_iterator()` | 55749 | Opens a file and iterates through its lines.  This function requires a better name. The purpose of t... |
| `_file_line_gen()` | 55784 | Generator that yields lines from a file in reverse order using mmap for efficiency. import mmap impo... |
| `_reverse_file_line_gen()` | 55796 | Generator that yields lines from a file in reverse order using mmap for efficiency. import mmap impo... |
| `get_gpu_ids_used_by_process()` | 56921 | Get a list of all GPU's used by a given process. Defaults to the current process. if pid is None: pi... |
| `get_vram_used_by_current_process()` | 57114 | Returns the amount of VRAM used by the current process for each GPU or a specific GPU.  Args: gpu_id... |
| `print_process_info()` | 57502 | *(No description)* |

## Architectural Analysis

### System Integration Architecture

RP's system integration layer provides:

1. **File System**: Complete file/directory operations with path handling
2. **Process Management**: Thread/process creation and management
3. **Terminal Integration**: ANSI colors, terminal detection, pseudo-terminals
4. **Clipboard Operations**: Cross-platform clipboard access
5. **External Tools**: Integration with system commands and executables

### Key Patterns
- **Cross-Platform**: Automatic platform detection and adaptation
- **Error Resilience**: Graceful fallbacks when system features unavailable  
- **Process Abstractions**: High-level interfaces to low-level system operations
- **Context Managers**: Proper resource cleanup and state management

## Function Relationships

### Batch Operations
- `_load_file()` ↔ `_load_files()`
- `convert_image_file()` ↔ `convert_image_files()`
- `load_yaml_file()` ↔ `load_yaml_files()`
- `strip_file_extension()` ↔ `strip_file_extensions()`
- `get_file_extension()` ↔ `get_file_extensions()`
- ... and 5 more

### Multiplexing
- `play_sound_file()` ↔ `play_sound_file_via_afplay()`
- `play_sound_file()` ↔ `play_sound_file_via_pygame()`
- `load_image_from_screenshot()` ↔ `load_image_from_screenshot_via_mss()`

