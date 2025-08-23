# Core Utilities

Essential RP functions that form the foundation of the library.

## Package Management & Imports
- **pip_import** (r.py:52818) - Auto-installing import with lazy loading (called 310+ times)
- **_omni_load** (r.py:44078) - Smart file loading dispatcher

## Printing & Output
- **print** (r.py:52935) - Enhanced print with fansi color support
- **fansi_print** (r.py:52951) - Color-formatted printing
- **format** (r.py:53048) - String formatting utility
- **fansi** (r.py:53019) - Color formatting system

## Data Structures & Conversion
- **add** (r.py:53200) - Universal add operation (lists, dicts, etc.)
- **delete_file** (r.py:12702) - Safe file deletion with error handling  
- **as_easydict** (r.py:53312) - Convert dict to dot-notation accessible EasyDict
- **detuple** (r.py:53578) - Extract single value from single-item tuple
- **set_ans** (r.py:42965) - Set answer variable for REPL convenience

## Object Inspection & Debugging
- **rinsp** (r.py:33362) - Enhanced object inspection with recursive search
- **_rinsp_search_helper** (r.py:33375) - Internal breadth-first search for rinsp

## Functional Programming Core
- **seq** (r.py:586) - Sequential function composition and pipelining
- **fog** (r.py:276) - Function currying for deferred execution
- **scoop** (r.py:320) - Functional reduce/fold operation
- **par** (r.py:600) - Parallel function broadcasting
- **par_map** (r.py:422) - Parallel mapping operation

## Text Processing
- **line_join** (r.py:53618) - Join strings with newlines