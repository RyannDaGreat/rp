# RP Master Suggestions File

**Last Updated**: Auto-generated from analysis tools  
**Total Functions Analyzed**: 2001  
**Total Issues Identified**: 392+ consistency issues, 860 missing docstrings

## Quick Stats
- **43% functions have NO documentation** (860 functions)
- **104 functions need plural variants** (e.g., `resize_image` → `resize_images`)
- **79 functions could benefit from `_via_` variants** for backend flexibility
- **24 asymmetric pairs** missing (encode without decode)
- **Most critical undocumented function**: `pip_import` (called 310 times)

## High Priority Suggestions

### 1. Critical Missing Plurals ⭐⭐⭐
**Impact**: Major usability improvement for batch operations

- `resize_image` → `resize_images` (HUGE gap - most requested operation)
- `load_image_from_file` → `load_images_from_files` 
- `load_image_from_url` → `load_images_from_urls`
- `crop_image_to_square` → `crop_images_to_square`
- `save_image` → `save_images` (if not exists)

### 2. Documentation Priorities ⭐⭐⭐
**Impact**: Core RP functionality completely undocumented

- `pip_import` - Most called function (310 times), zero documentation
- `fog` - Core functional programming primitive, no docstring
- `seq` - Function composition foundation, no docstring  
- `_omni_load` - Multi-modal file loader, hidden gem
- `scoop` - Functional accumulator, no documentation

### 3. Backend Variant Opportunities ⭐⭐
**Impact**: Performance and flexibility improvements

Functions that should have `_via_` variants:
- `resize_image_via_opencv`, `resize_image_via_pillow`, `resize_image_via_skimage`
- `load_image_via_opencv`, `load_image_via_pillow`, `load_image_via_imageio`
- `convert_video_via_ffmpeg`, `convert_video_via_opencv`
- `text_to_speech_via_apple`, `text_to_speech_via_google`, `text_to_speech_via_aws`

### 4. Missing Symmetric Pairs ⭐⭐
**Impact**: API completeness and user expectations

- Functions with `_to_clipboard` but no `_from_clipboard`
- Functions with `encode_` but no `decode_`
- Functions with `compress_` but no `decompress_`

### 5. Parameter Consistency ⭐
**Impact**: API predictability

153 functions have inconsistent parameters compared to similar functions. Common missing parameters:
- `use_cache=False` - Should be standard across load functions
- `strict=True` - Should be standard for error handling
- `show_progress=False` - Should be standard for long operations

## Implementation Strategy

### Phase 1: Documentation Sprint (Immediate)
1. Document the top 50 most-called undocumented functions
2. Focus on `pip_import`, `fog`, `seq`, `_omni_load` first
3. Use minion work packages for systematic coverage

### Phase 2: Critical Missing Functions (Week 1-2)  
1. Implement `resize_images()` - highest impact plural
2. Add missing load/save plural variants
3. Create symmetric pairs for encode/decode functions

### Phase 3: Backend Variants (Week 3-4)
1. Add `_via_` variants for image processing functions
2. Implement video processing backends
3. Add text-to-speech backend options

### Phase 4: Parameter Standardization (Ongoing)
1. Add standard parameters to similar functions
2. Ensure consistent error handling across function families
3. Standardize progress reporting

## Tools Available

### Documentation Tools (`management/documentation/`)
- `function_mapper.py` - Analyzes function relationships (2001 functions mapped)
- `docstring_analyzer.py` - Assesses documentation quality 
- `minion_packager.py` - Creates work packages with context (1129 packages)

### Consistency Tools (`management/consistency/`)
- `consistency_tracker.py` - Finds 392 consistency issues
- `consistency_suggestions.md` - Detailed improvement suggestions

### Management Tools (`management/graveyard/`)
- `move_to_graveyard.py` - Safe refactoring of unused functions

## Progress Tracking

### Completed ✅
- [x] Function relationship mapping (2001 functions)  
- [x] Documentation quality analysis
- [x] Consistency issue identification (392 issues)
- [x] Work package generation (1129 packages)
- [x] Management tool organization

### In Progress 🔄
- [ ] High-priority function documentation
- [ ] Critical missing plural implementations
- [ ] Systematic minion work package execution

### Planned 📋
- [ ] Backend variant implementations
- [ ] Parameter consistency improvements
- [ ] AI-integrated documentation website
- [ ] Automated consistency monitoring

## For Future Claudes

**Before implementing new functionality:**
1. Check `consistency_suggestions.md` - function might already be identified as needed
2. Use `function_mapper.py` to understand relationship context
3. Check work packages in `management/documentation/work_packages/` for existing context

**When documenting functions:**
1. Use minion work packages for full context
2. Follow the enhancement template (don't replace existing docstrings)
3. Update appropriate tag files
4. Cross-reference related functions

**When adding new functions:**
1. Check for naming consistency with existing patterns
2. Consider if plural variant is needed immediately
3. Plan for potential `_via_` backends from the start
4. Add standard RP parameters (use_cache, strict, show_progress)

---

**This suggestions file is automatically maintained by the RP management tools. Update it when making significant improvements to the codebase.**