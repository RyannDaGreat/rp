import sys
import rp

default_scope = rp.r.__dict__
default_scope['r'] = rp.r

def arg_eval(code):
    if not rp.is_namespaceable(code) and rp.r._is_valid_exeval_python_syntax(code) or code in default_scope:
        #Try to evaluate it. Include rp in the scope for easy access.
        scope = dict(default_scope)
        value = rp.exeval(code, scope=scope)
    else:
        #Just treat it as a string
        value = code

    return value

def pop_kwargs():
    kwargs = {}
    while len(sys.argv) > 3 and rp.starts_with_any(sys.argv[-2], "--", "---"):
        #While we might have a "--kwarg value" at the end
        value = sys.argv.pop()
        name  = sys.argv.pop()

        if name.startswith('---'):
            #Treated as string
            name = name[len('---'):]

        elif name.startswith('--'):
            #Treated as evaluable
            name = name[len('--'):]
            value = arg_eval(value)

        else:
            assert False, 'Sanity check'

        kwargs[name] = value
    return kwargs

def pop_args():
    #Always call pop_kwargs before calling pop_args!
    args = []
    while len(sys.argv) > 3:
        value = sys.argv.pop()
        value = arg_eval(value)
        args.insert(0, value)
    return args

help_text = """

HELP:
    Usage: rp <command> [<args>]

    Available commands:
      help    Show this help message
      call    Call a function with arguments and keyword arguments
              Format: rp call <funcname> arg1 arg2 arg3 --kwarg1 value1 --kwarg2 value2
      exec    Execute Python code with optional variable assignments
              Format: rp exec <code> --variable1 value1 --variable2 value2
      
    Note: All kwargs whose keys start with -- are evaluated as python code, 
        and all that start with --- are treated as string literals

    If no command is provided, an interactive Python terminal (rp.pterm) is started.
"""

def main():
    if len(sys.argv) > 1: 
        if sys.argv[1] == "call":
            #Lets you call a function
            #rp call fansi_print "Hello World!" green bold

            if not len(sys.argv) > 2:
                raise RuntimeError("rp call: Please provide a funcname. Format: 'rp call <funcname> arg1 arg2 arg3 --kwarg1 value1 --kwarg2 value2'")
            
            func_name = sys.argv[2]
            kwargs = pop_kwargs()
            args   = pop_args()

            scope = dict(default_scope)
            scope.update({"args__" : args, "kwargs__" : kwargs})

            #TODO: THE SCOPE SHOULD INCLUDE ALL IMPORTS FROM RP
            ans = rp.exeval(func_name+'(*args__, **kwargs__)', scope=scope)

        elif sys.argv[1] == "exec":
            # Import everything from your package at the top level

            if not len(sys.argv) > 2:
                raise RuntimeError("rp exec: Please provide code. Format: 'rp call <code> --variable1 value1 --variable2 value2'")

            # Allow kwargs: "rp exec 'print(x+y)' --x 123 --y 321"
            # Command is like:   rp exec print(x) --x 123
            # Or most minimally, like:   rp exec print(x) --x 123
            kwargs = pop_kwargs()

            scope = dict(default_scope)
            scope.update(kwargs)

            code = ' '.join(sys.argv[2:])

            ans = rp.exeval(code, scope=scope)

        else:
            raise RuntimeError(help_text+"\nERROR: Supported rp commands: [exec, call] not "+sys.argv[1])

        #It's often useful to pipe the ans by printing it
        if ans is not None:
            print(ans)

    else:
        # If no additional arguments or not the 'run' command, call _pterm
        rp.r._pterm()

    import threading
    threading._shutdown=lambda *x,**y:None #Fuck the threading shutdown crap

if __name__ == '__main__':
    main()
