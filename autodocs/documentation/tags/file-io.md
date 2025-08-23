# File I/O Functions

Functions for reading, writing, and managing files and data formats.

## Text File Operations
- `string_to_text_file()` - Write strings to text files with path handling
- `text_file_to_string()` - Read text files into strings
- `save_text_file()` - Alias for string_to_text_file
- `append_line_to_file()` - Append content to existing files

## JSON Operations  
- `save_json()` - Serialize Python objects to JSON files with formatting options
- `load_json()` - Load JSON files into Python objects

## Path Utilities
- `get_absolute_path()` - Convert relative paths to absolute with symlink resolution
- `get_absolute_paths()` - Batch path conversion
- `get_relative_path()` - Convert absolute paths to relative

## Animation Export
- `save_animated_png()` - Export image sequences as animated PNG (APNG) files

## Features
- Automatic path expansion (~ to home directory)
- Parent directory creation
- Error handling with clear messages
- Support for various encoding formats
- Integration with RP's path management system

## Related Functions
- File system utilities in path-utilities tag
- Image saving functions in image-export tag
- Video export functions in video-processing tag