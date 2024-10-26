"""
Black Macchiato wrapper that prints errors as stdout and avoids directory permission errors
Lean and mean - faster than importing all of rp
"""
import macchiato
import sys
import io
import os
import tempfile

def autoformat_python_via_black_macchiato(python_code_snippet: str, max_line_length=None) -> str:

    black_args=[]
    if max_line_length is not None:
        assert isinstance(max_line_length, int)
        black_args += ["--line-length", str(max_line_length)]

    input_file = io.StringIO(python_code_snippet)
    output_file = io.StringIO()
    
    exit_code = macchiato.macchiato(input_file, output_file, args=black_args)
    
    if exit_code != 0:
        raise ValueError("rp.autoformat_python_via_black_macchiato: Formatting failed with exit code:", exit_code)
    
    return output_file.getvalue()

try:
    os.chdir(tempfile.gettempdir()) #Make sure we don't get any read-only errors

    code = sys.stdin.read()

    # Format the code
    formatted_code = autoformat_python_via_black_macchiato(code, max_line_length=150)

    if formatted_code.endswith('\n'):
        #Black macchiato adds a new line
        formatted_code = formatted_code[:-1]

    # Print the formatted code
    print(end=formatted_code)

except Exception:
    import rp
    rp.disable_fansi()
    rp.print_verbose_stack_trace()
