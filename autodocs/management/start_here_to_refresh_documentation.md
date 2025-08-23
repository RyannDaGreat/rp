# START HERE: RP Documentation System Quick Start

**For fresh LLMs: Read this file to understand and begin RP documentation work.**

## 🚀 Quick Setup (2 minutes)

### Step 1: Update Analysis (if r.py changed)
```bash
cd /opt/homebrew/lib/python3.10/site-packages/rp/management/scripts
python3.10 diff_aware_updater.py
```
This automatically detects what changed in r.py and updates only necessary analysis databases.

### Step 2: Get Current Status
```bash
cd /opt/homebrew/lib/python3.10/site-packages/rp/management/documentation
python3.10 minion_packager.py | head -20
```
Shows highest priority work packages ready for documentation.

## 📋 What You're Working With

### Complete Analysis Already Done
- **2001+ functions** mapped with relationships
- **1129 work packages** prioritized and ready
- **Full context** for each function (dependencies, usage patterns)
- **Quality assessment** of existing documentation

### Your Mission: Systematic Documentation
- **Start with Package 1** (highest priority: pip_import, print, fansi_print, etc.)
- **Enhance existing docstrings** (NEVER replace them!)
- **Add examples, parameters, cross-references**
- **Follow RP conventions** for consistency

## 🎯 Start Documentation Now

### Load Highest Priority Package
```bash
cat /opt/homebrew/lib/python3.10/site-packages/rp/documentation/work_packages/package_001_priority_*.json
```

### Begin With pip_import (Most Critical Function)
- **Location**: r.py line ~52818
- **Status**: Has docstring but needs enhancement
- **Called by**: 310+ functions across RP
- **Never replace existing docstring** - add to it!

## 📖 Documentation Guidelines

### ✅ DO:
- **Preserve all existing docstrings** completely
- **Add "Enhanced Documentation:" section**
- **Include concrete examples** with `>>> syntax`
- **Test all examples** before documenting
- **Cross-reference related functions**
- **Add to tag files** in `documentation/tags/`

### ❌ NEVER:
- Replace existing docstrings
- Remove author's voice, humor, or TODOs
- Break Python 3.5 compatibility (no f-strings in r.py)
- Change existing function behavior

### Enhancement Template:
```python
def function_name(params):
    """
    [KEEP ALL ORIGINAL DOCSTRING - humor, TODOs, links, etc.]
    
    Usage notes:
    - [ANALYZE USAGE FIRST] Look at how function is actually called in codebase
    - [HUMAN-FRIENDLY LENGTH] Important functions get more info, simple ones stay concise
    - Key patterns: Most common ways this function is used (based on grep analysis)
    - Critical info: What developers need to know when they call this
    
    Parameters: [Only if non-obvious]
        param1 (type): Essential info only
    
    Returns: [Only if non-obvious]
        type: Brief description
        
    Examples: [WORKFLOW: Test code → Copy results → NEVER guess]
        >>> # 1. ALWAYS write test code to scratchpad.py and run with /opt/homebrew/opt/python@3.10/bin/python3.10 scratchpad.py
        >>> # 2. NEVER use python -c - ALWAYS USE scratchpad.py (CLAUDE.md rule)
        >>> # 3. Copy EXACT output from the scratchpad.py results
        >>> import numpy as np
        >>> video = np.random.rand(10, 480, 640, 3)
        >>> get_video_width(video)
        640
        
    Tags: 3-4 most relevant keywords
    """
```

### 📏 Documentation Length Guidelines:

**ANALYZE USAGE FIRST** - grep the codebase to see HOW the function is used:
- **Assertions/validation**: Document what makes input valid/invalid
- **Conditional branching**: Document the different code paths
- **Filter operations**: Document what gets included/excluded
- **Data transformation**: Document input→output transformations

**LENGTH BY IMPORTANCE**:
- **Core functions** (used 50+ times): More comprehensive docs
- **Simple utilities** (used <10 times): Minimal enhancement
- **Type checkers** (like `is_*`): Focus on what they accept/reject
- **Private functions**: Brief purpose only

## 🛠️ Tools Available

### Check Function Relationships
```python
# In Python
exec(open('/opt/homebrew/lib/python3.10/site-packages/rp/management/documentation/function_mapper.py').read())
```

### Analyze Documentation Quality  
```python
exec(open('/opt/homebrew/lib/python3.10/site-packages/rp/management/documentation/docstring_analyzer.py').read())
```

### Check Argument Consistency
```python
exec(open('/opt/homebrew/lib/python3.10/site-packages/rp/management/consistency/argument_tracker.py').read())
```

## 📊 Progress Tracking

### After Each Function
1. **Test your examples** - ensure they actually work
2. **Update tag files** - add function to relevant categories
3. **Cross-check related functions** - mention them in docs

### Work Package Completion
- Mark package as complete when all functions documented
- Move to next highest priority package
- Update progress in work package files

## 🎖️ Success Criteria

### Per Function:
- ☐ Original docstring preserved completely
- ☐ Enhanced documentation section added
- ☐ All parameters documented with types
- ☐ Return value documented
- ☐ At least one working example with >>> syntax  
- ☐ Related functions cross-referenced
- ☐ Added to appropriate tag files

### Per Work Package:
- ☐ All 8 functions in package documented
- ☐ Cross-references between package functions added
- ☐ Quality checklist completed
- ☐ Examples tested and working

## 🚦 Quality Gates

### Before Moving to Next Function:
- **🚨 MANDATORY: TEST EXAMPLES FIRST** 🚨
  - Write test code to scratchpad.py and run with /opt/homebrew/opt/python@3.10/bin/python3.10 scratchpad.py
  - **NEVER use python -c** - ALWAYS USE scratchpad.py (CLAUDE.md rule)
  - Copy EXACT working results - never guess outputs
  - If you write an example without testing first, you've failed
- Use concrete inputs with expected outputs (not just "my_data")
- Show assertions about input format/shape to make examples clear
- Check that you haven't broken existing functionality
- Ensure you preserved all original content

### Before Moving to Next Package:
- All functions in current package complete
- Cross-references between functions added
- Tag files updated with all new functions

## 📈 Time Estimates (Realistic)

- **Core functions** (pip_import, seq, fog): 30-60 minutes each
- **Functions with basic docs**: 10-20 minutes enhancement
- **Simple utilities**: 5-10 minutes each
- **Already good docs**: 2-5 minutes touch-up

**Total realistic estimate**: ~300-400 hours for all 2001 functions

## 🆘 Need Help?

### Check These Files:
- `management/README.md` - Complete system overview
- `management/HANDOFF_SUMMARY.md` - Detailed context
- `management/consistency/RP_ARGUMENT_CONVENTIONS.md` - Naming standards
- `management/documentation/DOCTEST_VALIDATION.md` - Quality validation approach

### Common Issues:
- **"Function already documented well"**: Just add examples and cross-references
- **"Can't find related functions"**: Use function_mapper.py to see relationships  
- **"Examples don't work"**: Check imports and ensure you're testing in clean environment

---

**Ready to start! Load Package 1, begin with pip_import, preserve Ryan's original voice, and systematically document RP's incredible functionality. 🚀**