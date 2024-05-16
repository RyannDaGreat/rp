import inspect
import atexit
import re

#TODO: Integrate this into RP's repl too somehow
#      when repl command finishes, we should also trigger it - not just atexit
#      Also we should be able to do this when using <c-e> -- should modify the buffer (can be undone with <c-z> as normal)
#      SHould be able to toggle this on and off globally to disable debug_eval's
#      Should be able to make it verbose or silent
#      Perhaps ask a yes/no at the end of whether we shoudl replace
#      Inform the user of what files have changed at least...ONLY IF they changed...

def is_zero_arg_callable(func):
    if callable(func):
        if not inspect.signature(func).parameters:
            return True
    return False

# List to store results and metadata
_debug_eval_results = []

def debug_comment(value):
    # Get caller's frame
    frame = inspect.currentframe().f_back
    filename = frame.f_globals['__file__']
    lineno = frame.f_lineno
    
    try:
        if is_zero_arg_callable(value):
            # If value is a zero-argument callable, call it
            result = value()
        elif isinstance(value, str):
            # Evaluate the string expression
            result = eval(value, frame.f_globals, frame.f_locals)
        else:
            # For non-callable, non-string values, convert directly to string
            result = value

        try:
            result = str(result)
        except Exception as e:
            result = "Error turning value into string: " + str(e)

    except Exception as e:
        result = "Error: " + str(e)

    _debug_eval_results.append((filename, lineno, result))
    
    # Return result to allow inline usage if desired
    return result

def format_debug_comment(result):
    print(result)
    return comment_prefix+str(result)

comment_prefix = "# --> " #Make this regex-friendly. TODO: regex escape this

@atexit.register
def _perform_debug_eval_substitutions():
    # Process each file only once
    file_changes = {}
    for filename, lineno, result in _debug_eval_results:
        if filename not in file_changes:
            with open(filename, 'r') as file:
                lines = file.readlines()
        
        # Prepare new comment
        new_comment = format_debug_comment(result)
        current_line = lines[lineno - 1]
        
        # Check if there's an existing debug comment and replace it
        #TODO: Do this with split_python_tokens instead and do more checks to make sure the source wasn't modified as it was running so that we're replacing the right line. AKA check to make sure this line in the file matches the line in the linecache, and starts with either rp.debug_comment or debug_comment. And check to make sure we only modify the last --> because --> might be in the value itself (unlikely edge case granted).
        if comment_prefix in current_line:
            current_line = re.sub(comment_prefix + r'.+?(?=\n|$)', new_comment, current_line)
        else:
            current_line = current_line.rstrip() + new_comment + '\n'
        
        lines[lineno - 1] = current_line
        file_changes[filename] = lines

    # Write changes back to the files
    for filename, lines in file_changes.items():
        with open(filename, 'w') as file:
            try:
                file.writelines(lines)
            except Exception:
                print("debug_comment: Failed to modify "+filename)

# Example usage within the same file
if __name__ == "__main__":
    x = 10
    debug_comment(lambda:'#####'+ str(x * 20))  # This should replace or append the result `20` to this line in the source file. # --> #####200# ----> #####200
    for _ in range(10):
        from rp import random_int
        debug_comment(lambda:"What is "+str(344*random_int(0,100))) # --> What is 11008# ----> What is 24424
