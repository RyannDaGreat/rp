# Utility Functions

General-purpose utility functions for common programming tasks.

## Type Detection & Validation
- **is_iterable** (r.py:10234) - Check if object supports iteration
- **is_torch_tensor** (r.py:10892) - PyTorch tensor detection
- **is_numpy_array** (r.py:10923) - NumPy array validation
- **is_binary_image** (r.py:10967) - Binary/boolean image detection

## Mathematical & Computational Utilities
- **clamp** (r.py:15456) - Constrain values to specified range
- **graham_scan** (r.py:15523) - Convex hull computation algorithm

## String & Text Processing
- **line_join** (r.py:53618) - Join strings with newline separators
- **detuple** (r.py:53578) - Extract single value from single-item tuples

## Data Structure Operations
- **add** (r.py:53200) - Universal addition for lists, dictionaries, and objects
- **as_easydict** (r.py:53312) - Convert dictionaries to dot-notation accessible objects
- **set_ans** (r.py:42965) - Set answer variable for REPL convenience

## Batch Operations
- **labeled_images** (r.py:19789) - Add text labels to multiple images with progress tracking
- **resize_lists_to_max_len** (r.py:42456) - Pad lists to uniform maximum length
- **resize_lists_to_min_len** (r.py:42489) - Truncate lists to uniform minimum length

## Animation & Sequences
- **load_animated_gif** (r.py:11823) - Load GIF animations as frame sequences
- **save_animated_png** (r.py:11892) - Create APNG animations from image sequences