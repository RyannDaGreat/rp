#THIS CODE IS FROM bpython's patch_linecache.py. Get it with pip install bpython.
#I adapted it for use in rp to provide better stack traces

#This module is what lets us do this:
# File <rp-input-4>, line 1, in <module>
#     f()
# File <rp-input-3>, line 2, in f
#     1    def f():
# --> 2        g()

# File <rp-input-3>, line 4, in g
#     3    def g():
# --> 4        h()

# File <rp-input-3>, line 6, in h
#     def h():

# ZeroDivisionError: division by zero

#Note how the stack trace includes lines of code in it, even though they're from user inputs. Previously I needed ipython to do this but I found that bpython also did it. Then I stole bypthon's code and put it in here. lol. Maybe I'll rewrite it some day....when I rewrite rp...

import linecache
class BPythonLinecache(dict):
    """Replaces the cache dict in the standard-library linecache module,
    to also remember (in an unerasable way) rp console input."""

    def __init__(self, *args, **kwargs):
        super(BPythonLinecache, self).__init__(*args, **kwargs)
        self.bpython_history = []

    def is_bpython_filename(self, fname):
        try:
            return fname.startswith('<rp-input-')
        except AttributeError:
            # In case the key isn't a string
            return False

    def get_bpython_history(self, key):
        """Given a filename provided by remember_bpython_input,
        returns the associated source string."""
        try:
            idx = int(key.split('-')[2][:-1])
            return self.bpython_history[idx]
        except (IndexError, ValueError):
            raise KeyError

    def remember_bpython_input(self, source):
        """Remembers a string of source code, and returns
        a fake filename to use to retrieve it later."""
        filename = '<rp-input-%s>' % len(self.bpython_history)
        self.bpython_history.append((len(source), None,
                                     source.splitlines(True), filename))
        return filename

    def __getitem__(self, key):
        if self.is_bpython_filename(key):
            return self.get_bpython_history(key)
        return super(BPythonLinecache, self).__getitem__(key)

    def __contains__(self, key):
        if self.is_bpython_filename(key):
            try:
                self.get_bpython_history(key)
                return True
            except KeyError:
                return False
        return super(BPythonLinecache, self).__contains__(key)

    def __delitem__(self, key):
        if not self.is_bpython_filename(key):
            return super(BPythonLinecache, self).__delitem__(key)


def _bpython_clear_linecache():
    try:
        bpython_history = linecache.cache.bpython_history
    except AttributeError:
        bpython_history = []
    linecache.cache = BPythonLinecache()
    linecache.cache.bpython_history = bpython_history


# Monkey-patch the linecache module so that we're able
# to hold our command history there and have it persist
linecache.cache = BPythonLinecache(linecache.cache)
linecache.clearcache = _bpython_clear_linecache


def filename_for_console_input(code_string):
    """Remembers a string of source code, and returns
    a fake filename to use to retrieve it later."""
    try:
        return linecache.cache.remember_bpython_input(code_string)
    except AttributeError:
        # If someone else has patched linecache.cache, better for code to
        # simply be unavailable to inspect.getsource() than to raise
        # an exception.
        return '<input>'
fc=filename_for_console_input
import code
#ans=code.InteractiveInterpreter().runsource('18/0',fc('18/0'),'single')
interpereter=code.InteractiveInterpreter()
# ans=interpereter.compile('148/0',fc('148/0'),'single')
# def ans():
#     pass
# def run(code):
#     exec(interpereter.compile(code,fc(code),'single'))
# ans=fc


def run_code(code,mode,namespace,exv):
    import sys
    old_tracer=sys.gettrace()#To make sure any debuggers launched in this exeval aren't carried through to pseudo-terminal internal code, while still letting you call pseudo-terminal from a debugger
    try:
        #THE FOLLOWING 4 LINES HAVE BEEN BOILED DOWN INTO 1 LINE TO MAKE EXITING THE DEBUGGER FASTER
        #comp=interpereter.compile(code,fc(code),mode)
        #if comp is None:#This means the code is incomplete; see help(interpereter.compile). Because interpereter.compile("(","<filename",'exec') returns None and not an error.
        #    #I want it to raise an error, though. We know it won't compile, so we might as well call exec.
        #    exec(code) #This shouldn't actually run anything; it should throw an EOF error with the appropriate text. Also, pseudo_terminal should hide the difference from the user.
        #else:
        #    return exv(comp,namespace,namespace)















































#################################    EXITING THE DEBUGGER #######################################


        return exv(interpereter.compile(code,fc(code),mode) or exec(code),namespace,namespace)
    finally:#This should happen no matter what, but shouldn't squelch any errors we get when evaluating the code
        #EXIT THE DEBUGGER: (Do this so we don't debug the next pseudo-terminal prompt as well)
        sys.settrace(old_tracer)#Instead of just setting it to None, set it to what it was before. This allows us to run pseudo_terminal from a debugger without exiting the debugger.






