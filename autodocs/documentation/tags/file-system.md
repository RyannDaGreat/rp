# File System Operations

Comprehensive file and directory management, path operations, and file I/O utilities.

## Path Operations & Validation
- **path_exists** (r.py:35050) - Universal path existence check (files and directories)
- **file_exists** (r.py:35000) - File-specific existence validation with safety
- **get_absolute_path** (r.py:35123) - Path resolution with symlink handling
- **get_relative_path** (r.py:35189) - Convert absolute paths to relative
- **get_current_directory** (r.py:35245) - Working directory with process info
- **path_join** (r.py:35298) - Cross-platform path joining utility

## Directory Management
- **make_directory** (r.py:35401) - Create directories with nested support
- **make_parent_directory** (r.py:35445) - Ensure parent directory exists
- **make_directories** (r.py:35489) - Batch directory creation
- **get_all_paths** (r.py:30571) - Comprehensive directory traversal with filtering
- **get_random_folder** (r.py:33635) - Random directory selection for sampling
- **get_random_folders** (r.py:33628) - Multiple random directory selection

## File Reading & Writing
- **text_file_to_string** (r.py:12578) - Text file reading with URL support and caching
- **string_to_text_file** (r.py:12645) - Write text to file with encoding
- **append_line_to_file** (r.py:12685) - Atomic line appending with file creation
- **file_to_bytes** (r.py:12723) - Binary file reading utility
- **bytes_to_file** (r.py:12789) - Binary file writing with directory creation
- **save_file_lines** (r.py:12834) - Write list of strings as file lines

## File Movement & Organization  
- **move_path** (r.py:35567) - mv-like functionality with directory handling
- **temporary_file_path** (r.py:35634) - Generate unique temporary file paths

## File Discovery & Filtering
- **get_all_files** (r.py:30623) - File-only directory traversal
- **get_all_folders** (r.py:30645) - Directory-only traversal  
- **get_all_image_files** (r.py:30689) - Image file discovery with format filtering

## File Properties & Analysis
- **is_utf8_file** (r.py:12456) - UTF-8 encoding validation with performance optimization
- **get_system_fonts** (r.py:51811) - Cross-platform font file discovery

## Interactive File Operations
- **input_select_path** (r.py:18234) - Interactive file/folder selection interface
- **vim** (r.py:18189) - Vim editor integration with object introspection