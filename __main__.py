import sys
import rp

scope = rp.r.__dict__

def arg_eval(code):
    if not rp.is_namespaceable(code) and rp.r._is_valid_exeval_python_syntax(code):
        #Try to evaluate it. Include rp in the scope for easy access.
        value = rp.exeval(code, scope=scope)
    else:
        #Just treat it as a string
        value = code

    return value

def pop_kwargs():
    kwargs = {}
    while len(sys.argv) > 3 and sys.argv[-2].startswith('--'):
        #While we might have a "--kwarg value" at the end
        value = sys.argv.pop()
        value = arg_eval(value)
        name  = sys.argv.pop()[len('--'):]
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

def main():
    if len(sys.argv) > 2: 
        if sys.argv[1] == "call":
            #Lets you call a function
            #rp call fansi_print "Hello World!" green bold
            
            func_name = sys.argv[2]
            kwargs = pop_kwargs()
            args   = pop_args()

            scope = dict(scope)
            scope.update({"args__" : args, "kwargs__" : kwargs})

            #TODO: THE SCOPE SHOULD INCLUDE ALL IMPORTS FROM RP
            ans = rp.exeval(func_name+'(*args__, **kwargs__)', scope=scope)

        elif sys.argv[1] == "exec":
            # Import everything from your package at the top level

            # Allow kwargs: "rp exec 'print(x+y)' --x 123 --y 321"
            # Command is like:   rp exec print(x) --x 123
            # Or most minimally, like:   rp exec print(x) --x 123
            kwargs = pop_kwargs()

            scope = dict(scope)
            scope.update(kwargs)

            code = ' '.join(sys.argv[2:])

            ans = rp.exeval(code, scope=scope)

        #It's often useful to pipe the ans by printing it
        if ans is not None:
            print(ans)

    else:
        # If no additional arguments or not the 'run' command, call _pterm
        rp.r._pterm()

if __name__ == '__main__':
    main()
