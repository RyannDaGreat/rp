import inspect
import atexit
import rp

#TODO: Integrate this into RP's repl too somehow
#      when repl command finishes, we should also trigger it - not just atexit
#      Also we should be able to do this when using <c-e> -- should modify the buffer (can be undone with <c-z> as normal)
#      SHould be able to toggle this on and off globally to disable debug_eval's
#      Should be able to make it verbose or silent
#      Perhaps ask a yes/no at the end of whether we shoudl replace
#      Inform the user of what files have changed at least...ONLY IF they changed...
#      Allow a frames_back or similar option to debug_comment so other functions can build upon it, adding defaults etc.

def is_zero_arg_callable(func):
    if callable(func):
        if not inspect.signature(func).parameters:
            return True
    return False

# List to store results and metadata
_debug_comment_results = []

def debug_comment(value):
    """
    Modifies the source code of the file this was called in!
    Best practice is to commit all changed to git before this is called so you can revert changes.

    Notes:
        Because it simply adds or modifies # comments, the number of lines in a modified file will not be changed by this code

    EXAMPLE:
        >>> import rp

        >>> #This function modifies your code - it adds comments next to debug_comment that show what it evaluated
        >>> rp.debug_comment(rp.debug_comment)# --> <function debug_comment at 0x10717cee0>

        >>> #If you align the comments like this it will respect the alignment upon updating
        >>> rp.debug_comment(rp.debug_comment.__module__)# --> rp.experimental.debug_comment
        >>> rp.debug_comment(rp)                         # --> <module 'rp' from '/opt/homebrew/lib/python3.10/site-packages/rp/__init__.py'>
        >>> rp.debug_comment(__file__)                   # --> /Users/ryan/CleanCode/Sandbox/debugevaltest/evaltest.py
        >>> rp.debug_comment(__name__)                   # --> __main__

        >>> rp.debug_comment("What\nHappens\nWith\nMultiple\nLines")# --> 'What\nHappens\nWith\nMultiple\nLines'

        >>> #The last evaluation will be the one that's kept
        >>> for i in range(5):
        >>> rp.debug_comment(i)   # --> 4
        >>> rp.debug_comment(i**2)# --> 16

        >>> rp.debug_comment(# --> I is 4
        >>> "I is "+str(i)
        >>> )   

        >>> #This is what happens if you call it on multiple lines
        >>> rp.debug_comment(# --> 127
        >>> 123+i
        >>> )   

        >>> #If you give it a function that takes 0 args, it will try to evaluate it
        >>> #This is good for if you want to disable debug_comments and disable all the evaluation inside them too to make your code faster
        >>> rp.debug_comment(lambda: 22*22)# --> 484

        >>> #Use cases:
        >>> import torch
        >>> t=torch.randn(10,100).cpu()
        >>> rp.debug_comment(t.shape) # --> torch.Size([10, 100])
        >>> rp.debug_comment(t.dtype) # --> torch.float32
        >>> rp.debug_comment(t.min()) # --> tensor(-3.1440)
        >>> rp.debug_comment(t.max()) # --> tensor(2.9910)
        >>> rp.debug_comment(t.device)# --> cpu
    """
    # TODO: allow varargs
    # Kwargs will be reserved for special purposes, like if we want to also record the date, or number of times the value changed or number of times we called debug comment etc etc

    # Get caller's frame
    frame = inspect.currentframe().f_back
    filename = frame.f_globals['__file__']
    lineno = frame.f_lineno
    
    try:
        if is_zero_arg_callable(value):
            # If value is a zero-argument callable, call it
            result = value()
        ## Disabled eval-strings because I found I often feed it strings...this only makes sense if we give it a string literal, requiring complex introspection and parsing
        # elif isinstance(value, str):
        #     # Evaluate the string expression
        #     result = eval(value, frame.f_globals, frame.f_locals)
        else:
            # For non-callable, non-string values, convert directly to string
            result = value

        try:
            result = str(result)
        except Exception as e:
            result = "Error turning value into string: " + str(e)

    except Exception as e:
        result = "Error: " + str(e)

    if '\n' in result or '\r' in result: 
        result=repr(result) #No multiline allowed! Has to fit in a single comment string

    _debug_comment_results.append((filename, lineno, result))
    
    #Let original value pass through
    return value

def format_debug_comment(result):
    # _debug_print(result) # This can get a bit spammy...
    return comment_prefix+str(result)

def _debug_print(x):
    rp.fansi_print('rp.debug_comment: '+str(x), 'green', 'underlined')

comment_prefix = "# --> " #Make this regex-friendly. TODO: regex escape this

def _perform_debug_eval_substitutions():
    # Process each file only once
    file_changes = {}
    for filename, lineno, result in _debug_comment_results:
        if filename not in file_changes:
            with open(filename, 'r') as file:
                file_changes[filename] = file.readlines()
        
        # Prepare new comment
        new_comment = format_debug_comment(result)
        current_line = file_changes[filename][lineno - 1]
        
        #TODO: Do this with split_python_tokens instead and do more checks to make sure the source wasn't modified as it was running so that we're replacing the right line. AKA check to make sure this line in the file matches the line in the linecache, and starts with either rp.debug_comment or debug_comment. And check to make sure we only modify the last --> because --> might be in the value itself (unlikely edge case granted).

        # Check if there's an existing debug comment and replace it
        if comment_prefix in current_line:
            current_line = current_line[:current_line.rfind(comment_prefix)] + new_comment + '\n'
        else:
            current_line = current_line.rstrip() + new_comment + '\n'
        
        file_changes[filename][lineno - 1] = current_line

    # Write changes back to the files
    for filename, lines in file_changes.items():
        with open(filename, 'w') as file:
            try:
                _debug_print("writing to "+filename)
                file.writelines(lines)
            except Exception:
                _debug_print("Failed to modify "+filename)

    #Don't do anything twice
    _debug_comment_results.clear()

atexit.register(_perform_debug_eval_substitutions)

# Example usage within the same file
if __name__ == "__main__":
    x = 10
    debug_comment(lambda:'#####'+ str(x * 20))  # This should replace or append the result `20` to this line in the source file. # --> #####200# ----> #####200
    for _ in range(10):
        from rp import random_int
        debug_comment(lambda:"What is "+str(344*random_int(0,100))) # --> What is 11008# ----> What is 24424
