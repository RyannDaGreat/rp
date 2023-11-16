import sys
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "exec" and len(sys.argv) > 2:
        # Import everything from your package at the top level

        # Execute the command passed in the arguments
        import rp
        rp.exeval('from rp import *\n'+' '.join(sys.argv[2:]))
    else:
        # If no additional arguments or not the 'run' command, call _pterm
        from rp.r import _pterm
        _pterm()

if __name__ == '__main__':
    main()
