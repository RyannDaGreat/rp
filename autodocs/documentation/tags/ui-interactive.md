# RP Library: Ui Interactive

User interface and visualization functions: displays, plots, interactive selection, and terminal interfaces.

**Total Functions: 92**

## Function Inventory

| Function | Line | Description |
|----------|------|-------------|
| `load_image_from_matplotlib()` | 6227 | Return matplotlib's current display as an image You can increase the DPI to get a higher resolution.... |
| `_display_image_in_notebook_via_ipyplot()` | 8236 | Private function to display images in Jupyter notebooks using ipyplot.  Internal implementation for ... |
| `_display_image_in_notebook_via_ipython()` | 8256 | Add the current Python interpreter as a Jupyter IPython kernel.  Parameters: - kernel_name: The name... |
| `display_video()` | 8310 | Video can either be a string, or a video (aka a 4d tensor or iterable of images) Example: display_vi... |
| `_display_video_via_mediapy()` | 8410 |  Use mediapy to display a video in a Jupyter notebook  rp.pip_import('mediapy') import mediapy  #Pre... |
| `display_video_in_notebook()` | 8423 | Display a video or image in a Jupyter notebook.  Args: video: The video object to display. - Can be ... |
| `_display_video_in_notebook()` | 8446 | *(No description)* |
| `display_video_in_notebook_webp()` | 8504 | Displays an animated webp in a Jupyter notebook with a specified quality and framerate See rp.displa... |
| `_display_downloadable_image_in_notebook_via_ipython()` | 8550 |  Display an image at full resolution in a jupyter notebook. Returns an updatable channel.   channel ... |
| `display_image_in_notebook()` | 8561 |  Display an image at full resolution in a jupyter notebook. Returns an updatable channel.   channel ... |
| `display()` | 8716 | Adds a new viewport from IPython.display import display, HTML display(self._converted_content, displ... |
| `display_image()` | 8745 | Very simple to understand: this function displays an image. At first, it tries to use matplotlib and... |
| `display_alpha_image()` | 8871 | Display image with checkerboard background to visualize transparency.  Shows transparent areas as ch... |
| `_display_image_slideshow_animated()` | 8885 | This works best on Jupyter notebooks right now It technically works without a jupyter notebook...but... |
| `display_qr_code_in_terminal()` | 8941 | EXAMPLE: #Done in Alacritty or the default Mac Terminal display_qr_code_in_terminal('https://google.... |
| `display_website_in_terminal()` | 8961 | Enhanced Documentation:  Fetches and displays a website's content as formatted text in the terminal.... |
| `display_image_slideshow()` | 9015 | Enters an interactive image slideshow Useful for exploring large folders/lists of images images: ima... |
| `display()` | 9056 | *(No description)* |
| `display_help()` | 9074 | *(No description)* |
| `display_color_255()` | 9213 |  Example: display_color_255(255,0,0)# ⟵ Displays Red  # noinspection PyUnresolvedReferences display_... |
| `display_float_color()` | 9218 | Create a bar graph with the given y-values The 'values'     parameter is a list of bar heights. They... |
| `bar_graph()` | 9223 | Create a bar graph with the given y-values The 'values'     parameter is a list of bar heights. They... |
| `line_graph_via_plotille()` | 9276 | Draws a line graph in the terminal using Plotille with the given values and colors.  Args: y_values ... |
| `line_graph_live()` | 9350 | Continuously update and display a line graph based on values returned by a given function.  This fun... |
| `line_graph_in_terminal()` | 9438 | This is mainly here as a simple reference for how to create a line-graph with matplotlib.pyplot. The... |
| `line_graph()` | 9444 | This is mainly here as a simple reference for how to create a line-graph with matplotlib.pyplot. The... |
| `plot()` | 9467 | *(No description)* |
| `display_polygon()` | 9509 | Uses matplotlib Parameters: line_width: The width of the border around the polygon (set to 0 for no ... |
| `display_update()` | 9619 | This should be preferred over the older block() function shown above Note: If time is too low, you c... |
| `display_clear()` | 9635 | Displays a color histogram of an image using OpenCV and Matplotlib.  Args: image (str or numpy.ndarr... |
| `display_cv_color_histogram()` | 9646 | Displays a color histogram of an image using OpenCV and Matplotlib.  Args: image (str or numpy.ndarr... |
| `display_cv_color_histograms()` | 9710 | Plots color histograms of two images side by side for comparison using OpenCV and Matplotlib.  Args:... |
| `display_dict()` | 11390 | Made by Ryan Burgert for the purpose of visualizing large dictionaries. EXAMPLE DISPLAY: >>> display... |
| `display_list()` | 11411 | Display markdown text in both Jupyter notebook and terminal environments.  markdown : str Markdown t... |
| `display_markdown()` | 11419 | Display markdown text in both Jupyter notebook and terminal environments.  markdown : str Markdown t... |
| `display_code_cell()` | 11523 | Print code cell with formatting, line numbers, and syntax highlighting. In a terminal, it displays a... |
| `MIDI_input()` | 13502 | From: http://code.activestate.com/recipes/576653-convert-a-cmp-function-to-a-key-function/ Must use ... |
| `display_dot()` | 15156 | Used to be called 'dot', in-case any of my old code breaks... EXAMPLE: for theta in np.linspace(0,ta... |
| `display_path()` | 15167 | Displays a 'path' aka a series of 2d vectors If color is None, will plot as a different color every ... |
| `display_image_in_terminal()` | 17195 | Uses unicode, and is black-and-white EXAMPLE: while True: display_image_in_terminal(load_image_from_... |
| `display_image_in_terminal_color()` | 17249 | Will attempt to draw a color image in the terminal This is slower than display_image_in_terminal, an... |
| `display_image_in_terminal_imgcat()` | 17320 | Can display images in some terminals as actual images  Works in: iterm2 wezterm tmux (if configured ... |
| `display_video_in_terminal_color()` | 17360 | Display a video in the terminal with a progress bar.  Args: frames (list): List of frames to display... |
| `display_eta()` | 18315 | *(No description)* |
| `_display_pterm_flamechart()` | 19095 | *(No description)* |
| `_rp_show_custom_line_profile()` | 19322 | Display custom line profiler results with visual enhancements TODO: This is a work in progress. Curr... |
| `_multi_line_python_input()` | 19531 | *(No description)* |
| `python_input()` | 19754 | Enhanced interactive Python input with completion and features.  Enhanced Documentation: ===========... |
| `display_file_tree()` | 20612 | Display a visual tree structure of files and directories, similar to the Unix 'tree' command.  Enhan... |
| `_view_interactive_json()` | 21436 | *(No description)* |
| `_display_columns()` | 21466 | *(No description)* |
| `_input_select_multiple_history_multiline()` | 21473 | *(No description)* |
| `process_paragraph()` | 21477 | *(No description)* |
| `_input_select_multiple_paragraphs()` | 21485 | *(No description)* |
| `_input_select_multiple_history()` | 21603 | *(No description)* |
| `_input_select_rp_gists()` | 21844 | Change directory in pseudo_terminal with history tracking. Internal helper. dir=os.path.expanduser(d... |
| `show_error()` | 22439 | fansi_print(Sorry, but that command caused an error that pseudo_terminal couldn't fix! Command abort... |
| `_display_pterm_image()` | 22495 | *(No description)* |
| `cv_imshow()` | 27753 | Display image using OpenCV with interactive capabilities.  Enhanced cross-platform image display fun... |
| `cv_line_graph()` | 28435 | Draws a line graph using OpenCV with the given values and colors.  Args: y_values (list or numpy.nda... |
| `cv_manually_selected_contours()` | 28716 | Let the user manually pick out a set of contours by clicking them, then hitting the enter key to con... |
| `cv_manually_selected_contour()` | 28809 | TODO Merge cv_manually_selected_contours with cv_manually_selected_contour to eliminate redundancy L... |
| `scatter_plot()` | 29310 | Parameters: x and y: There are three ways to give this function points: - One is by specifying x and... |
| `display()` | 35938 | Adds a new viewport from IPython.display import display, HTML display(self._html, display_id=self._d... |
| `input_multiline()` | 36643 | Keeps asking the user for a console input until they satisfy the condition with their answer. Exampl... |
| `input_conditional()` | 36653 | Keeps asking the user for a console input until they satisfy the condition with their answer. Exampl... |
| `input_yes_no()` | 36670 | A boolean function of the user's console input The user must say y, ye, yes, n or no to continue Exa... |
| `input_integer()` | 36679 | *(No description)* |
| `input_default()` | 36717 | Like input(), but it has a default value that you can edit From https://stackoverflow.com/questions/... |
| `input_select()` | 36733 | Example: Try running 'input_select_option(options=['Hello','Goodbye','Bonjour'])'  TODO: In order to... |
| `display_more_options()` | 36772 | string_pager(More options: - Enter 'p' to use rp.string_pager() to view your choices (this is useful... |
| `display_query_options()` | 36782 | *(No description)* |
| `display_options_with_pager()` | 36798 | *(No description)* |
| `input_select_multiple()` | 36846 | EXAMPLE: input_select_multiple("Please select some letters:",'abcdefg') |
| `get_box_char_bar_graph()` | 41326 | Generate a bar graph using box characters based on the provided values.  Args: values (list): A list... |
| `input_keypress()` | 42997 | If handle_keyboard_interrupt is True, when you press control+c, it will return the control+c charact... |
| `input_select_path()` | 43071 | Asks the user to select a file or folder If reverse. put option 0 on the bottom instead of the top (... |
| `input_select_folder()` | 43204 | I use this to select arduinos when I want to connect to one with a serial port After this, I general... |
| `input_select_file()` | 43207 | I use this to select arduinos when I want to connect to one with a serial port After this, I general... |
| `input_select_serial_device_id()` | 43211 | I use this to select arduinos when I want to connect to one with a serial port After this, I general... |
| `_maybe_display_string_in_pager()` | 46553 | *(No description)* |
| `display_pandas_correlation_heatmap()` | 47796 | This function is used for exploratory analysis with pandas dataframes. It lets you see which variabl... |
| `show_head()` | 51381 | *(No description)* |
| `show_body()` | 51391 | *(No description)* |
| `show_tail()` | 51404 | *(No description)* |
| `input_option()` | 52123 | *(No description)* |
| `_display_filetype_size_histogram()` | 53766 | Enhanced Documentation: Displays a histogram showing total disk usage by file type (extension) in a ... |
| `line_graph_via_bokeh()` | 53913 | Uses the Bokeh library to display an interactive line graph in an IPython notebook Only works in IPy... |
| `select_git_commit()` | 54409 | Let user select a git commit using input_select  Returns: Selected commit hash  EXAMPLE:  >>>   4: a... |
| `_get_select_torch_device_lock_file()` | 55029 | Returns the appropriate PyTorch device based on the available hardware and system configuration.  Th... |
| `select_torch_device()` | 55033 | Returns the appropriate PyTorch device based on the available hardware and system configuration.  Th... |
| `type_string_with_keyboard()` | 57574 | *(No description)* |

## Architectural Analysis


## Function Relationships

### Multiplexing
- `line_graph()` ↔ `line_graph_via_plotille()`
- `line_graph()` ↔ `line_graph_via_bokeh()`

### Batch Operations
- `display_cv_color_histogram()` ↔ `display_cv_color_histograms()`
- `cv_manually_selected_contour()` ↔ `cv_manually_selected_contours()`

