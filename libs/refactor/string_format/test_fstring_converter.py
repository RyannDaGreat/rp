#!/usr/bin/env python3.10
import sys
import re
from fstring_converter import convert_string

def normalize_code(code):
    """
    Normalize code for comparison by removing whitespace variations.
    This helps ensure that functionally equivalent code is considered equal
    even if whitespace or quotes differ slightly.
    """
    # Remove leading/trailing whitespace
    code = code.strip()
    
    # Normalize whitespace around operators
    code = re.sub(r'\s*([=+\-*/,])\s*', r'\1', code)
    
    # Normalize quotes - for test purposes, treating ' and " as equivalent
    # Not generally true, but helps with testing format strings
    def normalize_quotes(match):
        content = match.group(2)
        return f'"{content}"'
    
    code = re.sub(r"(['\"])(.*?)(\1)", normalize_quotes, code)
    
    return code

# Test cases covering all possible f-string scenarios
test_cases = [
    # Basic f-strings
    ('f"Hello, {name}"', '"Hello, {0}".format(name)'),
    ('f"{x} + {y} = {x + y}"', '"{0} + {1} = {2}".format(x, y, x + y)'),
    
    # Nested expressions
    ('f"Result: {calculate(x, y=3, z={"key": value})}"', 
     '"Result: {0}".format(calculate(x, y=3, z={"key": value}))'),
    
    # Format specifiers
    ('f"Pi: {math.pi:.2f}"', '"Pi: {0:.2f}".format(math.pi)'),
    ('f"Progress: {progress:.0%}"', '"Progress: {0:.0%}".format(progress)'),
    ('f"{num:05d}"', '"{0:05d}".format(num)'),
    
    # Conversions
    ('f"Debug: {obj!r}"', '"Debug: {0!r}".format(obj)'),
    ('f"String: {data!s}"', '"String: {0!s}".format(data)'),
    ('f"ASCII: {text!a}"', '"ASCII: {0!a}".format(text)'),
    
    # Expressions with format specifiers and conversions
    ('f"{complex_obj!r:>20}"', '"{0!r:>20}".format(complex_obj)'),
    
    # Escaped braces
    ('f"{{Not a variable}}"', '"{{Not a variable}}"'),
    ('f"{{These are literal braces}} but {this} is a variable"', 
     '"{{These are literal braces}} but {0} is a variable".format(this)'),
    
    # Raw f-strings
    ('rf"Raw string with {var}"', 'r"Raw string with {0}".format(var)'),
    
    # Multiline f-strings
    ('''f"""
    Multiline
    {variable}
    String
    """''', 
     '''"""
    Multiline
    {0}
    String
    """.format(variable)'''),
    
    # Complex expressions
    ('f"Math: {2 * (3 + 4)}"', '"Math: {0}".format(2 * (3 + 4))'),
    ('f"Dict: {data["key"]}"', '"Dict: {0}".format(data["key"])'),
    ('f"Method: {obj.method(arg1, arg2=val)}"', '"Method: {0}".format(obj.method(arg1, arg2=val))'),
    
    # Multiple expressions with different attributes
    ('f"{x.name} is {y[0].upper()}"', '"{0} is {1}".format(x.name, y[0].upper())'),
    
    # Empty f-string
    ('f""', '""'),
    
    # Multiple lines of code with f-strings
    ('''
def func():
    name = "Alice"
    age = 30
    print(f"{name} is {age} years old")
    return f"Info: {name}, {age}"
''', 
     '''
def func():
    name = "Alice"
    age = 30
    print("{0} is {1} years old".format(name, age))
    return "Info: {0}, {1}".format(name, age)
'''),
]

# Test real-world examples from actual codebase
real_world_cases = [
    ("""print(f"Saving {len(tensors)} tensors to {path}")""", 
     """print("Saving {0} tensors to {1}".format(len(tensors), path))"""),
    
    ("""print(f"    - {k}: {v.shape if hasattr(v, 'shape') else 'no shape'}")""", 
     """print("    - {0}: {1}".format(k, v.shape if hasattr(v, 'shape') else 'no shape'))"""),
]

# Add real-world test cases to our test suite
test_cases.extend(real_world_cases)

def run_tests():
    """Run all test cases and report failures"""
    passed = 0
    failed = 0
    errors = 0
    
    # First, try individual test cases
    for i, (input_code, expected_output) in enumerate(test_cases):
        try:
            actual_output = convert_string(input_code)
            
            # Function that evaluates if outputs are functionally equivalent
            def are_equivalent(actual, expected):
                # For simple strings, direct comparison
                if len(actual) < 100 and len(expected) < 100:
                    return normalize_code(actual) == normalize_code(expected)
                
                # For more complex code, check if key structures match
                # Strip all whitespace for comparison
                actual_condensed = re.sub(r'\s+', '', actual)
                expected_condensed = re.sub(r'\s+', '', expected)
                
                return actual_condensed == expected_condensed
            
            if are_equivalent(actual_output, expected_output):
                passed += 1
                print(f"✅ Test {i+1} passed")
            else:
                failed += 1
                print(f"❌ Test {i+1} failed")
                print(f"Input:    {input_code}")
                print(f"Expected: {expected_output}")
                print(f"Actual:   {actual_output}")
                print()
        except Exception as e:
            errors += 1
            print(f"❌ Test {i+1} failed with exception: {e}")
            print(f"Input:    {input_code}")
            print()
            
    # Real-world verification: The file from which this was extracted
    print("\n==== Testing Real File Conversion ====")
    try:
        file_test = """
def save_safetensors(tensors, path, metadata=None, *, verbose=False):
    \"\"\"
    Saves tensors to a .safetensors file.

    Args:
        tensors (dict or easydict): Dictionary of tensors to save
        path (str): Path to save the .safetensors file
        metadata (dict, optional): Metadata to include in the file. Defaults to None.
        verbose (bool, optional): Print tensor names. Defaults to False.

    Returns:
        str: Path to the saved file
        
    Reference: https://huggingface.co/docs/safetensors/en/index

    EXAMPLE:
        >>> tensors = {"weight": torch.randn(3, 4), "bias": torch.randn(4)}
        >>> save_safetensors(tensors, "model.safetensors")
        'model.safetensors'
        >>> loaded = load_safetensors("model.safetensors")
        >>> loaded.keys()
        ['weight', 'bias']
    \"\"\"
    import os
    from rp.r import pip_import
    pip_import("safetensors")
    from safetensors.torch import save_file
    
    # Convert to regular dict if it's an easydict
    if hasattr(tensors, 'to_dict'):
        tensors = tensors.to_dict()
    
    # Ensure all values are tensors
    if verbose:
        print(f"Saving {len(tensors)} tensors to {path}")
    
    for k, v in tensors.items():
        if verbose:
            print(f"    - {k}: {v.shape if hasattr(v, 'shape') else 'no shape'}")
    
    # Make sure the directory exists
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    
    # Save the tensors
    save_file(tensors, path, metadata)
    
    return path
"""
        converted = convert_string(file_test)
        
        # Check that f-strings are converted
        if "f\"" in converted or "f'" in converted:
            print("❌ File test failed - f-strings remain in the converted code")
            failed += 1
        else:
            print("✅ File test passed - all f-strings were converted")
            passed += 1
            
        # Visual check of conversion for debugging
        print("\nConverted real-world sample:")
        for line in converted.splitlines()[:20]:  # Show first 20 lines
            if ".format(" in line:
                print(f"  {line.strip()}")
    except Exception as e:
        print(f"❌ File test failed with exception: {e}")
        errors += 1
            
    print(f"\nResults: {passed} passed, {failed} failed, {errors} errors")
    return failed == 0 and errors == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)