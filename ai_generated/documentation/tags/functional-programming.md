# Functional Programming

Higher-order functions, function composition, and functional programming utilities.

## Core Function Composition
- **seq** (r.py:586) - Sequential function pipelining and composition
  - RP's flagship functional utility
  - Handles None-returning functions by preserving previous values
  - Supports both single functions and function chains
  - Common patterns: data pipelines, string processing, mathematical sequences

- **fog** (r.py:276) - Function currying for deferred execution
  - Creates parameterless lambda closures: `lambda: func(*args, **kwargs)`
  - Essential for threading, partial application, and deferred execution
  - Used throughout RP codebase for thread-safe function passing

- **scoop** (r.py:320) - Functional reduce/fold operation
  - Left-fold semantics with safe deep-copying
  - Mathematical reductions, string concatenation, list building
  - Defensive copying prevents accumulator mutations

## Parallel Functional Operations
- **par_map** (r.py:422) - Parallel mapping with order preservation
  - Higher-order function for concurrent transformations
  - Thread-safe with configurable worker pools
  - Maintains input-output order despite parallel execution

- **par** (r.py:600) - Parallel function broadcasting
  - Execute multiple functions with same arguments concurrently
  - Designed for side-effect operations (logging, notifications, updates)
  - Complements seq() for ordered vs parallel execution patterns

## Function Utilities & Helpers  
- **gather_args_call** (r.py:33456) - Dynamic argument gathering and function calls
- **gather_args_recursive_call** (r.py:33489) - Recursive argument gathering for complex calls

## Argument Processing & Function Management
- **args_hash** (r.py:33523) - Generate hash signatures for function arguments
- **_get_pynput_mouse_controller** (r.py:33567) - Lazy-loaded input device controllers

## Design Philosophy
RP's functional programming system emphasizes:
- **Composition over complexity** - Simple functions that combine powerfully
- **None-aware pipelines** - Functions returning None don't break chains
- **Thread-safe patterns** - All functions designed for concurrent execution
- **Memory safety** - Defensive copying prevents unintended mutations
- **Universal compatibility** - Functions accept diverse input types