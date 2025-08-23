# RP Argument Standardization Plan

**Status**: URGENT - 672 inconsistencies found  
**Impact**: Massive improvement to RP's usability and predictability

## Critical Decisions Needed

### 1. `strict` Parameter Default ⚠️ URGENT ⚠️

**Current State**: 36 functions use `strict`, but some default to `True`, others to `False`

**Functions using `strict=True`**:
- Functions that should fail obviously when errors occur
- Data loading functions where silent failures are dangerous

**Functions using `strict=False`**:  
- Batch processing functions where skipping bad items makes sense
- Functions where errors are expected/common

**DECISION OPTIONS**:
```python
# Option A: Always fail-fast (strict=True)
def load_image(path, strict=True):  # Fail if image doesn't exist
def load_images(paths, strict=True):  # Fail if ANY image missing

# Option B: Context-dependent defaults  
def load_image(path, strict=True):   # Single items should fail
def load_images(paths, strict=False):  # Batch operations can skip

# Option C: Always permissive (strict=False)
def load_image(path, strict=False):  # Never fail, return None
```

**RECOMMENDATION**: **Option B** (Context-dependent)
- Single-item functions: `strict=True` (fail-fast for obvious errors)
- Batch/plural functions: `strict=False` (skip bad items, continue processing)

### 2. `show_progress` Standardization

**Current State**: 70 functions, mixed defaults

**DECISION**: 
- **Default**: `False` (quiet by default)
- **Add to ALL functions** that:
  - Process multiple items (batch operations)
  - Take more than 1-2 seconds typically
  - Involve network operations or file I/O

### 3. `use_cache` Standardization

**Current State**: 39 functions, mixed defaults

**DECISION**:
- **Default**: `False` (explicit caching)
- **Add to ALL functions** that:
  - Load data from files/URLs
  - Perform expensive computations
  - Are called repeatedly with same inputs

## Systematic Implementation Plan

### Phase 1: Critical Functions (Week 1)
**Target**: Top 50 most-used functions with argument inconsistencies

Priority list:
1. **`load_image`** and variants - ensure consistent `strict`, `use_cache`
2. **`resize_image`** - add `show_progress` for batch operations  
3. **`save_image`** - add `strict` for write failures
4. **All `*_images` plural functions** - ensure `show_progress=False` default
5. **`pip_import`** - consider adding `show_progress` for downloads

### Phase 2: Function Families (Week 2-3)
**Target**: Standardize entire function families together

**Image Functions** (172 functions using `image` parameter):
- Add missing `copy` parameters where applicable
- Standardize `interp` parameter naming and defaults
- Ensure consistent `color` parameter format

**Load Functions** (125+ functions with `path` parameter):
- Add `strict`, `use_cache`, `show_progress` where missing
- Standardize error handling behavior

**Process Functions**:
- Add `num_threads` where parallelization possible
- Add `show_progress` for long operations

### Phase 3: Argument Name Cleanup (Week 4)
**Target**: Fix argument name variations

**Standardize to preferred names**:
- `num_threads` (never `number_of_threads`, `thread_count`)
- `show_progress` (never `progress_bar`, `display_progress`)  
- `use_cache` (never `cache`, `enable_cache`)
- `strict` (never `strict_mode`, `fail_on_error`)

## Implementation Scripts Needed

### 1. Function Signature Updater
```python
# Script to systematically update function signatures
def update_function_signature(func_name, new_args):
    # Parse AST, update signature, preserve body
    # Add backward compatibility warnings
```

### 2. Docstring Argument Updater
```python  
# Update all docstrings to document new standard arguments
def update_docstring_args(func_name, standard_args):
    # Add parameter documentation following RP template
```

### 3. Compatibility Checker
```python
# Ensure changes don't break existing code
def check_compatibility(old_sig, new_sig):
    # Warn about breaking changes
    # Suggest migration paths
```

## Quality Assurance Plan

### Testing Strategy
1. **Backward compatibility tests** - ensure existing code still works
2. **Default behavior tests** - verify new defaults make sense  
3. **Cross-function consistency tests** - ensure similar functions behave similarly
4. **Documentation tests** - verify all new arguments are documented

### Rollout Strategy  
1. **Gradual rollout** - update function families together
2. **Deprecation warnings** - for any breaking changes
3. **Migration guides** - document changes for users
4. **Monitoring** - track any issues after changes

## Success Metrics

### Quantitative Goals
- **Reduce inconsistencies from 672 to <50**
- **100% of load functions** have `strict`, `use_cache` parameters
- **100% of batch functions** have `show_progress` parameter  
- **100% of parallelizable functions** have `num_threads` parameter
- **Zero argument name variations** for standard concepts

### Qualitative Goals
- **Predictable behavior** - similar functions behave similarly
- **Better discoverability** - standard arguments work everywhere
- **Improved documentation** - consistent parameter docs across functions
- **Easier to learn** - new users can predict argument names

## Risk Mitigation

### Potential Issues
1. **Breaking changes** for existing users
2. **Performance impact** from new parameters  
3. **Increased complexity** for simple functions
4. **Inconsistent rollout** if done partially

### Mitigation Strategies
1. **Gradual rollout** with deprecation warnings
2. **Performance testing** before/after changes
3. **Keep simple functions simple** - only add truly useful parameters
4. **Complete family updates** - never leave function families half-updated

## Tools and Automation

### Required Scripts
- **`argument_auditor.py`** - Find functions missing standard arguments
- **`signature_updater.py`** - Safely update function signatures  
- **`docstring_updater.py`** - Update parameter documentation
- **`compatibility_tester.py`** - Test backward compatibility

### Validation Tools
- **`consistency_validator.py`** - Verify standardization is complete
- **`usage_analyzer.py`** - Monitor how new parameters are used
- **`regression_tester.py`** - Ensure no functionality broken

---

**This is a massive undertaking that will dramatically improve RP's usability. The payoff is enormous - users will be able to predict how RP functions work based on consistent patterns.**