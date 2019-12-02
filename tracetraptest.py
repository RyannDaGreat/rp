#This entire module is currently experimental, because I haven't put much thought into making an elegant interface for it. Decorators are the simplest.
#This is the ultimate debugging tool when you know anything weird is happening but you don't know where.
#This is kinda like hunter.py but it doesn't hav syntax errors and it can launch a debugger
#This is the ultimate debugging tool when you know anything weird is happening but you don't know where.
#This is kinda like hunter.py but it doesn't hav syntax errors and it can launch a debugger

        
#TODO make this so that you must manually import it
anything="s;odfijspdouhpiwuerpinvcdouygw3rbsdljniuwhefhsboewbouebroscnousygeouygweubovsbpuebwpurbtpuwerb"#nobody will get tjis by coincidence lololol. debug_when(some_variable=anything) will trigger when that variable does exist
nothing="daoisdoijasodijasoijowqpnsdpvnspdnfpiwpiefbpsndpfsodfnpsodnfpsondfposndfpsodnfpsodnfpsondfpwpiw"#nobody will get tjis by coincidence lololol. debug_when(some_variable=nothing) will trigger when that variable doesn't exist
def debug_when(trap=None,**kwargs):
    #Don't use this in any code yet...the name might change into anything more palatable...
    #A decorator that goes over a tracer function(frame,event,args). This might be refined for convenience later, but this is the simplest and most versatile version.
    #Note that debug_when will slow your code down to a crawl, so use it for serious debug issues ans never ever ever in production code (unless you're writing a debugger too, in which case by all means...)
    #EXAMPLES:
    #   debug_when(i=5) #Will launch debugger if there's a variable called i with value 5
    #   debug_when(i=5,j=3) #Will launch debugger if there's a variable called i with value 5 AND theres a variable called j with value=3 (commas in the function definition represent AND)
    #   debug_when(i=anything) #Will launch debugger if there's a variable called i regardless of it's value
    #   debug_when(i=nothing) #Will launch debugger if there's NOT a variable called i, such as if it was deleted
    #   (NEEDS TO BE FIXED) UNTESTED: debug_when(anything=5) #Will launch debugger if there's any variable with value = 5
    #   (NEEDS TO BE FIXED) UNTESTED: debug_when(nothing=5) #Will launch debugger if there's NOT any variable with value = 5
    #   (NEEDS TO BE FIXED) UNTESTED: debug_when(anything=lambda x:x>5) #Will launch debugger if there's any variable with value greater than 5
    #   (NEEDS TO BE FIXED) UNTESTED: debug_when(nothing=lambda x:x>5) #Will launch debugger if there's NOT any variable with value greater than 5
    #   debug_when(i=lambda i:i>5) #Will launch debugger if there's a variable called i which has value greater than 5
    #   debug_when(lambda frame,event,args:'cv2' in sys.modules)#Debugger when cv2 is imported
    #   @debug_when#Can also be used as a decorator
    #   def _(frame,event,args):
    #       return 'hello world' in frame.f_locals.values() #Will launch debuger when there's a variable (regardless of name) with value 'hello world'

    import sys,pudb

    def set_pudb_trace_at_frame(frame,event,args):
        #This method is still hidden because I'm not confident in it yet
        import pudb
        dbg = pudb._get_debugger()
        dbg.set_trace(frame)
        #dbg.break_here(frame)
        #dbg.stop_here(frame)
        dbg.trace_dispatch(frame, event, args)

    if not callable(trap):
        #Syntactic sugar for debug_when's trap
        def trap(frame,event,args):
            #EXAMPLE: debug_when(i=5,j=6,x=lambda:x>5)#Will launch debugger if there's a variable called i==5 and a variable called j==6
            for name,check in kwargs.items():
                name_exists=name in frame.f_locals
                if name=='anything' or name=='nothing':
                    flag=False#If some value in the namespace satisfies the check
                    for value in frame.f_locals.values():
                        if callable(check):
                            if check(value):
                                flag=True
                                break
                        elif check==value or check is anything:
                            flag=True
                            break
                    if    name=='nothing'  and flag==True \
                       or flag=='anything' and flag==False:
                        return False
                elif not name_exists and check is not nothing:
                    return False
                elif check is nothing:
                    return False
                else:
                    value=frame.f_locals[name]
                    if callable(check):
                        if not check(value):
                            return False
                    elif check!=value and check is not anything:#If we set check to None, it will break if the variable exists at all
                        return False
            return True

    def tracer(frame,event,args):
        if trap(frame,event,args):
            set_pudb_trace_at_frame(frame,event,args)
        return tracer#We must return the tracer otherwise python will lose track of it

    sys.settrace(tracer)

def debug_when_namespace_satisfies(condition):
    #This is a decorator function
    #Namespace will be passed to condition as kwargs
    @debug_when
    def _(frame,event,args):
        namespace=frame.f_locals
        return condition(**namespace)

def theres_a_value_in_namespace_such_that(condition):
    def trap(frame,event,args):
        for key,value in frame.f_locals.items():
            if condition(value):
                return True
        return False
    return trap

def theres_a_value_equal_to(value,equals=lambda x,y:x==y):
    return theres_a_value_in_namespace_such_that(lambda x:equals(x,value))

if __name__=='__main__':
    from rp import *
    def f():
        i=0
        for _ in range(100) :
            print('i=',i)
            i+=1
            i%=30
    #@debug_when#the more robust but harder to read/write way: use debug_when as a decorator
    #def _(frame,event,args):
        #return 'i' in frame.f_locals and frame.f_locals['i']==15

    # debug_when(theres_a_value_equal_to(14))

    # debug_when(i=13)

    debug_when(i=lambda i:i>13)
    f()