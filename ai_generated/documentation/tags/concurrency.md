# Concurrency and Parallel Execution Functions

Functions that enable concurrent execution, parallel processing, and asynchronous operations.

## Core Concurrency Functions

### par_map
- **Concurrency model**: Thread-based parallel mapping
- **Executor**: ThreadPoolExecutor with configurable thread count  
- **Order preservation**: Maintains input order in output
- **Error handling**: Individual task failures don't stop entire operation
- **Location**: Line 422 in r.py

### lazy_par_map
- **Concurrency model**: Lazy parallel iterator with buffer management
- **Memory model**: Bounded buffer prevents memory exhaustion
- **Flow control**: Tasks submitted as previous ones complete
- **Backpressure**: Buffer limits provide natural backpressure mechanism
- **Location**: Line 484 in r.py

### par  
- **Concurrency model**: Function broadcasting with shared arguments
- **Execution**: Multiple functions execute concurrently on same data
- **Return values**: Designed for side-effect functions (void semantics)  
- **Synchronization**: No explicit synchronization - fire-and-forget pattern
- **Location**: Line 600 in r.py

## Concurrency Patterns Supported

### Map Pattern (par_map)
- **Input**: Single function, multiple argument sets
- **Output**: Ordered results corresponding to input order
- **Use case**: Transform collections of data in parallel
- **Example**: `par_map(process_file, file_list)`

### Broadcast Pattern (par)  
- **Input**: Multiple functions, single argument set
- **Output**: Side effects only (no return values)
- **Use case**: Execute multiple independent operations  
- **Example**: `par([log_event, send_alert, update_metrics], event_data)`

### Lazy Stream Pattern (lazy_par_map)
- **Input**: Function and iterables (potentially infinite)
- **Output**: Iterator yielding results as available
- **Use case**: Process large datasets without loading all into memory
- **Example**: `lazy_par_map(download_url, url_stream, buffer_limit=10)`

## Threading Configuration

### Thread Pool Sizing
- **Default**: 32 threads (optimized for I/O-bound tasks)
- **CPU-bound**: Consider setting to CPU count or slightly higher
- **I/O-bound**: Can often handle more threads than CPU count
- **Sequential**: Set to 0 for debugging or comparison

### Buffer Management  
- **Unlimited (0)**: Maximum throughput, high memory usage
- **Limited (N)**: Bounded memory usage, controlled backpressure
- **Auto**: Defaults to thread count for balanced performance

## Error Handling and Robustness

### Individual Task Failures
- Tasks are independent - one failure doesn't affect others
- Consider wrapping functions with try/catch for robustness
- Results maintain order even with variable task completion times

### Resource Management
- Thread pools are properly cleaned up after execution
- Buffer limits prevent resource exhaustion
- Configurable threading allows adaptation to system constraints

## Integration with RP Ecosystem

### Functional Programming
- Integrates with RP's functional patterns (seq, pam, scoop)
- Maintains referential transparency when used with pure functions
- Composable with other RP higher-order functions

### Performance Optimization
- Complements RP's lazy evaluation and memory management
- Works with RP's "accept anything" input flexibility
- Scales with RP's large dataset processing capabilities