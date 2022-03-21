#This is the ultimate debugging tool when you know something weird is happening but you don't know where.
#This is kinda like hunter.py but it doesn't hav syntax errors and it can launch a debugger
def f():
    i=0
    for _ in range(100) :
        print('i=',i)
        i+=1
        i%=30
def set_pudb_trace_at_frame(frame,event,args):
    import pudb
    dbg = pudb._get_debugger()
    dbg.set_trace(frame)
    #dbg.break_here(frame)
    #dbg.stop_here(frame)
    dbg.trace_dispatch(frame, event, args)
def trap_namespace_tracer(**checks):
    #Really, we can put any kind of condition in here. This is just a demo that simply checks to see if there's an i=1 in the namespace.
    def tracer(frame,event,args):
        #TODO: Use 'event' to detect function calls to make new kinds of traps, such as when we're entering a function.
        #TODO: Take inspiration from hunter.py?
        flag=True
        print('TRACE')#For some reason this isn't printed after we exit the debugger. investigaet.\c
        for key,value in checks.items():
            namespace=frame.f_locals
            if key not in namespace or namespace[key]!=value:
                flag=False
        if flag:
            print('CAUGHT!!!')
            set_pudb_trace_at_frame(frame,event,args)
        return tracer#We must return the tracer otherwise python will lose track of it
    sys.settrace(tracer)
trap_namespace_tracer(i=19)
f()