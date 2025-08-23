# RP Python Compatibility Requirements

## Critical Compatibility Constraint

**r.py MUST remain Python 3.5 compatible**

### What This Means

#### ❌ FORBIDDEN in r.py:
- **f-strings** (`f"hello {name}"`) - Added in Python 3.6
- **Type annotations** in function signatures - Limited in 3.5
- **Async/await syntax** - Limited in 3.5  
- **Dict comprehensions with **kwargs** - Python 3.5 limitations
- **Pathlib** extensive usage - Limited in 3.5
- **dataclasses** - Added in Python 3.7

#### ✅ ALLOWED in r.py:
- **String formatting**: `"hello {}".format(name)` or `"hello %s" % name`
- **Type hints in comments**: `# type: List[str]`
- **Basic dict/list operations**
- **All core Python 3.5 features**

#### ✅ ALLOWED in libs/ and lazy-loaded modules:
- **f-strings** - These modules load on-demand and can require newer Python
- **Modern type annotations** - Not loaded until used
- **Advanced features** - Can use Python 3.6+ features safely

### Examples

#### ❌ BAD (in r.py):
```python
def load_image(path):
    print(f"Loading {path}")  # F-STRING - FORBIDDEN
    return result

def process_data(items: List[str]) -> Dict:  # TYPE ANNOTATIONS - FORBIDDEN
    pass
```

#### ✅ GOOD (in r.py):
```python
def load_image(path):
    print("Loading {}".format(path))  # String formatting - OK
    return result

def process_data(items):
    # type: (List[str]) -> Dict  # Comment type hints - OK
    pass
```

#### ✅ GOOD (in libs/):
```python
# In libs/advanced_image.py (lazy-loaded)
def advanced_process(path: str) -> Image:
    print(f"Processing {path}")  # F-strings OK in libs/
    return result
```

### Why This Matters

1. **Broad compatibility** - RP works on older systems
2. **Server environments** - Many production systems use older Python
3. **Embedded systems** - Limited Python versions available
4. **Legacy support** - Existing installations continue working

### How Management Tools Handle This

#### Management Tools (Python 3.6+)
- **All management tools** can use modern Python features
- **Analysis scripts** use f-strings, type annotations, etc.
- **Located in management/** - separate from r.py

#### r.py Modifications
- **Any modifications to r.py** must maintain Python 3.5 compatibility
- **Use management tools** to validate compatibility
- **Test on Python 3.5** before committing changes

### Compatibility Validation

#### Manual Testing
```bash
# Test r.py on Python 3.5 (if available)
python3.5 -m py_compile r.py

# Check for f-strings
grep -n "f[\"']" r.py  # Should return nothing

# Check for type annotations in function signatures
grep -n "def.*:" r.py | grep -v "# type:"
```

#### Automated Checks
The management system includes compatibility validators:

```python
# management/scripts/compatibility_checker.py
def validate_r_py_compatibility():
    """Ensure r.py remains Python 3.5 compatible"""
    # Check for f-strings
    # Check for function annotations
    # Check for other 3.6+ features
```

### Migration Strategy

#### When Adding New Features to r.py:

1. **Check compatibility first** - No 3.6+ features
2. **Use string .format()** instead of f-strings  
3. **Comment type hints** instead of function annotations
4. **Lazy-load modern features** - Put in libs/ if needed

#### When Modifying Existing r.py Code:

1. **Preserve existing patterns** - Don't introduce 3.6+ features
2. **Maintain backwards compatibility** - Never break existing function signatures
3. **Test compatibility** - Validate with older Python if possible

### Future Considerations

#### Eventually Upgrading Minimum Version:

When Python 3.5 usage drops significantly:

1. **Announce deprecation** - Give users time to upgrade
2. **Gradual migration** - Phase in modern features slowly  
3. **Maintain branches** - Keep 3.5-compatible version available
4. **Update documentation** - Clear migration path

#### Current Status:

- **r.py**: Python 3.5 compatible (strict requirement)
- **libs/**: Can use modern Python features
- **management/**: Uses Python 3.6+ features freely
- **No immediate plans** to upgrade r.py minimum version

### For Claude Code Contributors

#### When Working on r.py:
1. **Never use f-strings** in r.py itself
2. **Use .format() or % formatting** for strings
3. **Comment-based type hints** only
4. **Test changes** don't break 3.5 compatibility

#### When Working on Management Tools:
1. **Use modern Python freely** - f-strings, type annotations, etc.
2. **Target Python 3.6+** for management tools
3. **Don't worry about 3.5** - management tools separate from r.py

#### When Working on libs/:
1. **Modern Python OK** - libs are lazy-loaded
2. **Check import paths** - ensure lazy loading works
3. **Document requirements** - if lib needs specific Python version

---

**This compatibility constraint ensures RP remains accessible to the widest possible user base while allowing management tools to use modern Python features for better development experience.**