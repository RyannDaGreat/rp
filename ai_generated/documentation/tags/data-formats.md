# Data Format Handling

Functions for loading, saving, and converting between different data formats.

## JSON Operations
- **load_json** (r.py:12234) - JSON loading with EasyDict conversion and caching
- **save_json** (r.py:12298) - JSON serialization with pretty-printing options
- **_view_json_via_jtree** (r.py:19521) - Interactive JSON tree viewer

## Pickle & Serialization
- **load_pickled_value** (r.py:12389) - Pickle loading with security notes
- **save_pickled_value** (r.py:12434) - Python object serialization
- **file_to_object** (r.py:44067) - RP Object format loading (.rpo files)

## Color Format Conversion
- **is_float_color** (r.py:15789) - Float color validation (0-1 range)
- **is_byte_color** (r.py:15823) - Integer color validation (0-255 range)
- **is_color** (r.py:15856) - General color format detection
- **is_binary_color** (r.py:15889) - Boolean color validation
- **float_color_to_byte_color** (r.py:15923) - Float to integer color conversion
- **float_color_to_hex_color** (r.py:15956) - Float to hex color conversion
- **color_name_to_byte_color** (r.py:15989) - Named colors to integer format
- **hex_colors_to_byte_colors** (r.py:16023) - Batch hex to byte conversion

## List & Array Processing
- **resize_lists_to_max_len** (r.py:42456) - Pad lists to maximum length
- **resize_lists_to_min_len** (r.py:42489) - Truncate lists to minimum length
- **_tensorify** (r.py:42523) - Convert data structures to tensor format

## URL & Web Content
- **download_url** (r.py:13456) - HTTP content downloading with headers
- **is_valid_url** (r.py:13389) - URL format validation
- **shorten_github_url** (r.py:13523) - GitHub URL shortening utility
- **display_website_in_terminal** (r.py:13578) - Terminal-based web browsing