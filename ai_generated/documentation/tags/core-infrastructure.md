# RP Library: Core Infrastructure

Foundation functions that enable all other operations: printing, debugging, ANSI formatting, and basic infrastructure.

**Total Functions: 65**

## Function Inventory

| Function | Line | Description |
|----------|------|-------------|
| `fansi_is_enabled()` | 1507 |  Returns true IFF fansi is enabled  return not _disable_fansi def fansi_is_disabled(): |
| `fansi_is_disabled()` | 1510 |  Returns true IFF fansi is disabled  return _disable_fansi _disable_fansi=False def disable_fansi():... |
| `disable_fansi()` | 1514 | Context to run a block of code without using fansi. Example: f=lambda:fansi_print("Hello World",'cya... |
| `enable_fansi()` | 1517 | Context to run a block of code without using fansi. Example: f=lambda:fansi_print("Hello World",'cya... |
| `without_fansi()` | 1522 | Context to run a block of code without using fansi. Example: f=lambda:fansi_print("Hello World",'cya... |
| `_transform_fansi_arg()` | 1560 |  Allow for 'yellow green underlined on blue bold'  style_keywords = style_keywords or _fansi_styles ... |
| `fansi()` | 1585 | 'fansi' is a pun, referring to ANSI and fancy Uses ANSI formatting to give the terminal styled color... |
| `_fansi_fix()` | 1894 | Fixes nested ANSI formatting issues in a string by restoring outer formatting after inner resets.  W... |
| `_legacy_fansi()` | 1957 | TODO: Fix bug: PROBLEM is that '\n' not in fansi('Hello\n','gray') This function uses ANSI escape se... |
| `fansi_print()` | 2029 | This function prints colored text in a terminal. It can also print bolded, underlined, or highlighte... |
| `fansi_printed()` | 2097 | prints table of formatted text format options for fansi. For reference |
| `print_fansi_reference_table()` | 2102 | prints table of formatted text format options for fansi. For reference |
| `_old_fansi_syntax_highlighting()` | 2118 | PLEASE NOTE THAT I DID NOT WRITE SOME OF THIS CODE!!! IT CAME FROM https://github.com/akheron/cpytho... |
| `fansi_syntax_highlighting()` | 2205 |  Apply syntax highlighting to 'code', a given string of python code. Returns an ANSI-styled string f... |
| `fansi_highlight_path()` | 2422 |  Syntax-highlights a path like "/path/to/thing/" - it colors the /'s differently from the rest. Retu... |
| `fansi_pygments()` | 2433 | Highlight code using pygments and return a string with ANSI escape codes for colors. If language is ... |
| `fansi_pygments_demo()` | 2497 |  Displays all themes for fansi_pygments  if code is None: |
| `_disable_insecure_request_warning()` | 6199 | Url should either be like http://website.com/image.png or like data:image/png;base64,iVBORw0KGgoAAAA... |
| `set_numpy_print_options()` | 7870 | np.set_printoptions is used to format the printed output of arrays. It makes the terminal output muc... |
| `force_suppress_warnings()` | 12173 | #     #    This function formats datetimes the way I personally like to read them. # #    EXAMPLE: #... |
| `force_restore_warnings()` | 12175 | #     #    This function formats datetimes the way I personally like to read them. # #    EXAMPLE: #... |
| `print()` | 12698 | rinsp report (aka Ryan's Inspection): OBJECT: rinsp(object, show_source_code=False, max_str_lines:in... |
| `errortext()` | 13025 | *(No description)* |
| `_cv_print_cam_props()` | 13210 | Prints available opencv camera properties for a given camera index EXAMPLE: >>> print_cam_info(1) CA... |
| `printed()` | 15140 | Print a message and return a value. Useful for inline debugging.  Example: result = some_function(pr... |
| `print_fansi_colors_in_curses()` | 15841 | *(No description)* |
| `print_verbose_stack_trace()` | 16151 | *(No description)* |
| `print_stack_trace()` | 16166 | Uses pygments to print a stack trace with syntax highlighting |
| `print_highlighted_stack_trace()` | 16179 | Uses pygments to print a stack trace with syntax highlighting |
| `print_rich_stack_trace()` | 16194 | Use the 'rich' library to print or return a stack trace.  This function can handle both exceptions a... |
| `print_all_git_paths()` | 16650 | *(No description)* |
| `_fix_CERTIFICATE_VERIFY_FAILED_errors()` | 17017 | *(No description)* |
| `print_latex_image()` | 17517 | r >>> print_latex_image("\sum_{n=3}^7x^2") ⠀⠀⠀⠀⠠⠟⢉⠟ ⠀⠀⠀⠀⠀⠀⡏ ⠀⠀⠀⠀⠀⠀⠃ ⢀⢀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡀ ⠀⠙⠄⠀⠀⠀⠀⠀⠀... |
| `_print_status()` | 18275 |  Print a single line in such a way that it will be overwritten if we call _print_status again  globa... |
| `fansi_progress()` | 18309 |  Used to show a progress bar under the ETA text!  string = string.expandtabs() #Jupyter doesn't rend... |
| `print_line()` | 20661 | *(No description)* |
| `_warnings_on()` | 20881 | *(No description)* |
| `_warnings_off()` | 20884 | *(No description)* |
| `_warnings_are_off()` | 20887 | *(No description)* |
| `print_history()` | 22422 | *(No description)* |
| `fansify()` | 22426 | *(No description)* |
| `show_error()` | 22439 | fansi_print(Sorry, but that command caused an error that pseudo_terminal couldn't fix! Command abort... |
| `pterm_pretty_print()` | 22492 | *(No description)* |
| `print_code()` | 24600 | *(No description)* |
| `print_line()` | 24602 | *(No description)* |
| `print_line()` | 24645 | *(No description)* |
| `get_name_from_name_error()` | 25274 | *(No description)* |
| `_rich_print()` | 26812 | Enhanced Documentation: Internal helper for pretty-printing objects using the Rich library with pagi... |
| `pretty_print()` | 26843 | Used to print out highly-nested dicts and lists etc, which are hard to read when it's all in one lin... |
| `print_to_string()` | 27107 | args and kwargs are passed to f Example: assert print_to_string(lambda:print("Hello World"))=="Hello... |
| `print_lines()` | 27124 | Shorthand for print(line_join(args))  EXAMPLE: >>> print_lines(1,2,3,4,5) 1 2 3 4 5 |
| `fansi_print_lines()` | 27141 | Shorthand for print(fansi(line_join(args), style=...))  EXAMPLE: >>> fansi_print_lines(1,2,3,4,5, st... |
| `print_fix()` | 27704 | r Meant to use this command in the pseudoterminal: `print_fix\py Turn all python2 print statements (... |
| `_cv_morphological_helper()` | 29144 | Used for erosion, dilation, and other functions. Please see the documentation if you'd like to know ... |
| `warn_if_multiple_devices()` | 30661 | *(No description)* |
| `print_line()` | 36510 | *(No description)* |
| `printed_generator()` | 41956 | *(No description)* |
| `debug()` | 42429 | Launch a debugger at 'level' frames up from the frame where you call this function. Try to launch rp... |
| `print_line()` | 46584 | *(No description)* |
| `_log()` | 49206 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.log(x) ... |
| `_log10()` | 49212 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.log10(x... |
| `_log2()` | 49274 |  works across libraries - such as numpy, torch, pure python  if is_numpy_array (x):return np.log2(x)... |
| `print_gpu_summary()` | 57185 | Prints a summary of GPU information using the Rich library.  Args: include_processes (bool, optional... |
| `print_notebook_gpu_summary()` | 57300 | >>> display_notebook_gpu_summary() ┏━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━... |
| `print_process_info()` | 57502 | *(No description)* |

## Architectural Analysis


## Function Relationships

### Batch Operations
- `print_line()` ↔ `print_lines()`

