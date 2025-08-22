# Performance Optimization Functions

Functions designed for performance optimization, parallel execution, and efficiency improvements.

## Parallel Processing Functions

### par_map
- **Purpose**: High-performance parallel mapping using thread pools
- **Performance**: Best for I/O-bound tasks, can provide significant speedups
- **Configuration**: Tunable thread count (default: 32), buffer management
- **Memory**: Eager evaluation - stores all results in memory
- **Location**: Line 422 in r.py

### lazy_par_map
- **Purpose**: Memory-efficient parallel processing with lazy evaluation
- **Performance**: Balances throughput with memory conservation
- **Configuration**: Thread pools + buffer limits for memory management  
- **Memory**: Lazy evaluation - processes items on-demand
- **Location**: Line 484 in r.py

### par
- **Purpose**: Parallel execution of multiple functions (side effects)
- **Performance**: Concurrent execution of independent operations
- **Use case**: Broadcasting operations, parallel cleanup, concurrent validations
- **Location**: Line 600 in r.py

## Performance Guidelines

### When to Use Parallel Functions
- **I/O-bound tasks**: Network requests, file operations, database queries
- **Independent operations**: Tasks that don't depend on each other's results
- **Large datasets**: Where thread overhead is amortized over data size
- **Side effects**: Operations valued for their effects rather than return values

### When NOT to Use Parallel Functions
- **CPU-bound tasks**: Limited by GIL, consider multiprocessing instead
- **Small datasets**: Thread overhead may exceed benefits
- **Sequential dependencies**: Where order matters or results depend on previous operations
- **Memory-constrained**: Use lazy variants or sequential processing

### Thread Configuration
- **Default threads**: 32 (reasonable for most I/O-bound workloads)
- **Sequential mode**: Set num_threads=0 for benchmarking or debugging
- **Custom sizing**: Tune based on system resources and task characteristics
- **Buffer limits**: Control memory usage with buffer_limit parameter

## Related Performance Functions

Functions that complement parallel processing for overall performance optimization.