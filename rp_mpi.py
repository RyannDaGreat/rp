from rp import *
import mpi4py
from mpi4py import MPI
comm=MPI.COMM_WORLD
rank=comm.rank
size=comm.size

# __all__='start_slave parallel_mapper exit_mpi'.split()

def print_verbose_stack_trace(exception):
    import stackprinter
    stackprinter.show(exception,style='darkbg2',file=sys.stdout)

MASTER_TO_SLAVE_TAG=1923784#Arbitrary unique integer

def exec_in_new_thread(code):
    run_as_new_thread(lambda:exec(code))

def eval_function_from_name(function_name,scope,*args,**kwargs):
    #Pass code that genrates a function called function_name
    #It will return the value that function returns when passed *args and **kwargs
    #EXAMPLE:
    # >>> eval_function_from_name('f=lambda x,y:x+y','f',10,y=20)
    # ans = 30

    assert isinstance(function_name,str),'Function name should be a string'

    assert function_name in scope,'This name isn\'t in the scope: '+repr(function_name)
    function=scope[function_name]
    assert callable(function),'You tried to call an object that exists called '+repr(function_name)+', but it\'s not a function'

    output=function(*args,**kwargs)
    return output

def accept_command(command,scope):
    #Parse the command object (passed as a dict for mpi4py's convenience)
    assert isinstance(command,dict)
    function_name  =command['function_name'  ]#The name of the function
    function_args  =command['function_args'  ]#args we pass to the function
    function_kwargs=command['function_kwargs']#kwargs we pass to the fucnction
    reply_dest     =command['reply_dest'     ]#Rank we send the response to
    reply_tag      =command['reply_tag'      ]
    assert isinstance(function_name  ,str  )
    assert isinstance(function_args  ,tuple)
    assert isinstance(function_kwargs,dict )
    assert isinstance(reply_dest     ,int  )
    assert isinstance(reply_tag      ,int  )
    assert 0<=reply_dest<size

    #Create the reply
    reply={}#If we don't error, add a 'result' key to reply containing the function result
    try:
        reply['result']=eval_function_from_name(function_name,scope,*function_args,**function_kwargs)
    finally:
        #No error handling yet...the indication that you have an error is that the reply is empty, and the stack trace this thread prints
        comm.isend(obj=reply,dest=reply_dest,tag=reply_tag)

def outsourced(function,dest):
    #A decorator that outsources a function to another processor and returns the result to the original processor

    #Input assertions
    assert callable(function)
    assert isinstance(dest,int)
    assert 0<=dest<size

    function_name=function.__name__

    def wrapper(*args,**kwargs):
        unique_tag=random_int(99999999)#Generate a random, unique tag for our response so we can operate asynchronously without intercepting other functions' arguments

        #Create the command object...
        command={}
        command['function_name'  ]=function_name
        command['function_args'  ]=args
        command['function_kwargs']=kwargs
        command['reply_dest'     ]=rank#Reply to us
        command['reply_tag'      ]=unique_tag

        #Immediately send the command and return the request
        comm.isend(obj=command,dest=dest,tag=MASTER_TO_SLAVE_TAG)
        return comm.irecv(source=dest,tag=unique_tag)

    return wrapper

def wait_all(responses):
    #Given a list of irecv() outputs, wait for them all in parallel and return the result as a list
    assert is_iterable(responses)
    
    for i in range(len(responses)):
        responses[i]=responses[i].wait()
    return responses
    # return [responses.wait() for request in requests]

def parallel_mapper(function,dests=None):
    #Pass a function to parallel_map, passing each 
        #The default is to send to all processors. Otherwise, dest should be a list of integers.
    if dests==None:
        dests=list(range(size))

    #Input assertions
    assert callable(function)
    assert is_iterable(dests)
    for dest in dests:
        assert isinstance(dest,int)
        assert 0<=dest<size

    def parallel_map(*arg_lists,**kwarg_lists):
        for arg_list in arg_lists:
            assert is_iterable(arg_list)
            assert len(arg_list)==len(dests)
        for kwarg_list in kwarg_lists.values():
            assert is_iterable(kwarg_list)
            assert len(kwarg_list)==len(dests)

        #Send out all of the requests, and gather the responses
        responses=[]
        for index,dest in enumerate(dests):
            args=[]
            for arg_list in arg_lists:
                args.append(arg_list[index])

            kwargs={}
            for key in kwarg_lists:
                kwargs[key]=kwarg_lists[key][index]

            try:
                response=outsourced(function,dest)
            except Exception as e:
                print_verbose_stack_trace(e)
                print(end='',flush=True)

            response=response(*args,**kwargs)
            responses.append(response)

        #Wait for all the replies in parallel
        replies=wait_all(responses)#See accept_command, which creates the reply objects with the results

        #Extract the results
        results=[]
        for index,reply in enumerate(replies):
            if 'result' in reply:
                result=reply['result']
                results.append(result)
            else:
                print("WARNING AT RANK "+str(rank)+": Received error from rank "+str(index)+", returning None",flush=True)
                results.append(None)

        return results

    return parallel_map

def slave_loop(scope=globals()):
    while True:
        command=comm.irecv(tag=MASTER_TO_SLAVE_TAG)
        command=command.wait()
        try:
            accept_command(command,scope=scope)
        except BaseException as e:
            print_verbose_stack_trace(e)
            print(end='',flush=True)

def start_slave():
    run_as_new_thread(slave_loop)

def exit_mpi():
    #We have to call this to exit our program. Ignore the segfault error; it doesn't matter.
    comm.barrier()
    MPI.Finalize()




# if __name__=='__main__':

#     #A demo of how to use this module

#     def printy(string):
#         print(rank,string,flush=True)
#         return rank**2

#     start_slave()#Every processor should call this exactly once, AFTER you've defined all of your functions...

#     if rank==0:
#         output=parallel_mapper(printy)(['Hello']*size)
#         print("FINAL OUTPUT =",output,flush=True)

#     exit_mpi()


def test_1(x):
        print(rank,x,flush=True)
        return rank,x

def test_2():
        return parallel_mapper(test_1)([rank]*size)


if rank==0:
    output=parallel_mapper(test_2)()
    print("FINAL OUTPUT =",output,flush=True)

start_slave()
exit_mpi()
