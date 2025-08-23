# RP Argument Naming Conventions

**Auto-generated from analysis of 2001 functions with 979 unique arguments**

## Standard Arguments (Must Use These Names & Defaults)

### Error Handling
- **`strict`** (bool|None, default=True)
  - **Usage**: Error handling behavior
  - **Values**: `True`=raise error, `False`=skip/continue, `None`=return None
  - **Used in**: 36 functions
  - **⚠️ INCONSISTENCY**: Currently uses both True AND False as defaults!
  - **DECISION NEEDED**: Standardize to `True` (fail-fast) or `False` (permissive)

### Progress Display  
- **`show_progress`** (bool|str, default=False)
  - **Usage**: Progress bar display
  - **Values**: `False`=no progress, `True`=default progress, `'eta'`=ETA display, `'tqdm'`=tqdm library
  - **Used in**: 70 functions
  - **⚠️ INCONSISTENCY**: Mixed True/False defaults

### Threading
- **`num_threads`** (int|None, default=None)
  - **Usage**: Number of parallel threads
  - **Values**: Positive integer or `None` (auto-detect)
  - **Used in**: 21 functions
  - **✅ CONSISTENT**: All use None default

### Caching
- **`use_cache`** (bool, default=False)  
  - **Usage**: Enable result caching
  - **Values**: `True`=cache results, `False`=no caching
  - **Used in**: 39 functions  
  - **⚠️ INCONSISTENCY**: Mixed True/False defaults

### Data Modification
- **`copy`** (bool, default=True)
  - **Usage**: Return copy vs potential in-place modification
  - **Values**: `True`=always return copy, `False`=MIGHT not copy but sometimes still might, sometimes might mutate original
  - **Used in**: 51 functions
  - **⚠️ INCONSISTENCY**: Mixed True/False defaults
  - **⚠️ SEMANTIC NOTE**: copy=False is performance optimization, NOT guarantee of in-place operation

### Output Suppression
- **`shutup`** (bool, default=False)
  - **Usage**: Suppress warnings/output  
  - **Values**: `True`=suppress output, `False`=normal output
  - **Used in**: 6 functions
  - **✅ CONSISTENT**: All use False default

## Most Common Arguments (Consider Standardizing)

### File/Path Arguments
- **`path`** (str) - 125 functions use this
  - **Common patterns**: File paths, directory paths
  - **Defaults**: `'/'`, `'.'` (when default needed)

### Image Processing Arguments  
- **`image`** (array) - 172 functions use this
  - **Most used argument** in RP!
  - **Type**: NumPy array, PIL Image, or torch tensor
  - **Convention**: Accept any image type, convert internally

- **`width`** (int) - 45 functions
  - **Common defaults**: 64, 256, 1
  - **Usage**: Image/video width in pixels

- **`height`** (int) - 38 functions  
  - **Common defaults**: 64, 256, 128
  - **Usage**: Image/video height in pixels

- **`color`** (tuple|str) - 30 functions
  - **Common defaults**: `'white'`, `(1,1,1,1)`, `(0,0,0,0)`
  - **Convention**: Accept color names or RGBA tuples

- **`interp`** (str) - 29 functions
  - **Common defaults**: `'nearest'`, `'floor'`, `'auto'`
  - **Usage**: Interpolation method for resizing

### General Arguments
- **`x`** (int|float) - 163 functions
  - **Most used coordinate** argument
  - **Common default**: 0

- **`y`** (int|float) - 26 functions  
  - **Common default**: 0

- **`string`** (str) - 63 functions
  - **Usage**: Text input for processing

- **`lazy`** (bool) - 43 functions
  - **Common default**: False
  - **Usage**: Lazy evaluation/loading

## CRITICAL Issues to Fix

### 1. Inconsistent Standard Argument Defaults ⚠️⚠️⚠️

**672 inconsistencies found!** Key problems:

- **`strict`**: Some functions default to True, others to False
- **`show_progress`**: Mixed defaults across similar functions
- **`use_cache`**: Inconsistent defaults in load functions
- **`copy`**: Some modify in-place by default, others return copies

### 2. Argument Name Variations

Functions use different names for the same concept:
- `num_threads` vs `number_of_threads` vs `thread_count`
- `show_progress` vs `progress_bar` vs `display_progress`  
- `use_cache` vs `cache` vs `enable_cache`

### 3. Missing Standard Arguments

Many functions that could benefit from standard arguments don't have them:
- Load functions missing `strict`, `use_cache`, `show_progress`
- Process functions missing `num_threads`, `show_progress`
- Modify functions missing `copy` parameter

## Recommendations

### Immediate Actions (High Priority)

1. **Standardize `strict` default** across all functions
   - **Recommendation**: Default to `True` (fail-fast principle)
   - **Rationale**: Better to fail obviously than silently skip

2. **Standardize `show_progress` default**  
   - **Recommendation**: Default to `False` (quiet by default)
   - **Add to all functions** that process multiple items or take >1 second

3. **Standardize `use_cache` default**
   - **Recommendation**: Default to `False` (explicit caching)
   - **Add to all load/get functions**

4. **Fix argument name variations**
   - Use `num_threads` (not `number_of_threads`)
   - Use `show_progress` (not `progress_bar`)
   - Use `use_cache` (not `cache`)

### Implementation Strategy

1. **Audit Phase**: Generate function-specific recommendations
2. **Standardization Phase**: Update function signatures systematically  
3. **Documentation Phase**: Update all docstrings with standard patterns
4. **Validation Phase**: Ensure backward compatibility with deprecation warnings

## For Future Claudes

**Before adding new functions:**
1. **Check this file** for standard argument names and defaults
2. **Use `argument_conventions.json`** to see usage patterns  
3. **Add standard arguments** if function fits the patterns:
   - Load/save functions → `strict`, `use_cache`, `show_progress`  
   - Process functions → `show_progress`, `num_threads`
   - Modify functions → `copy`

**When updating existing functions:**
1. **Check for missing standard arguments** that would be useful
2. **Verify default values** match the conventions here
3. **Update related functions together** to maintain consistency

---

**This file is maintained by the RP management tools. Update when making standardization decisions.**