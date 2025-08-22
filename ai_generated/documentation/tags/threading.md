# Threading and Asynchronous Execution Functions

Functions that support threading, deferred execution, and asynchronous operations.

## Core Threading Utilities

### fog
- **Purpose**: Creates parameterless closures for deferred execution
- **Threading use**: Commonly used with run_as_new_thread for async execution
- **Pattern**: `run_as_new_thread(fog(func, *args, **kwargs))`
- **Benefits**: Avoids lambda syntax, captures arguments at creation time
- **Location**: Line 276 in r.py

## Core Parallel Execution Functions

### par_map
- **Purpose**: Parallel version of built-in map() using ThreadPoolExecutor
- **Threading**: Configurable thread pool (default: 32 threads)
- **Features**: Order preservation, memory management, sequential fallback
- **Use cases**: I/O-bound operations, concurrent data processing
- **Location**: Line 422 in r.py

### lazy_par_map  
- **Purpose**: Memory-efficient lazy parallel mapping iterator
- **Threading**: Configurable thread pool with buffer management
- **Features**: Lazy evaluation, memory conservation, order preservation
- **Use cases**: Large datasets, streaming processing, memory-constrained environments
- **Location**: Line 484 in r.py

### par
- **Purpose**: Execute multiple functions in parallel with same arguments
- **Threading**: Built on par_map() for consistent behavior
- **Features**: Side-effect focused, void function execution, broadcast pattern
- **Use cases**: Parallel notifications, concurrent cleanup, multiple validations
- **Location**: Line 600 in r.py

## Functions with Threading Support

### text_to_speech_via_apple
- **Threading**: Optional async execution via run_as_thread parameter (default: True)
- **Implementation**: Uses fog() internally for deferred shell command execution
- **Synchronous mode**: Set run_as_thread=False for blocking execution
- **Location**: Line 6650 in r.py