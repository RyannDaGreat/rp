from rp import *
import mpi4py
from mpi4py import MPI
comm=MPI.COMM_WORLD
rank=comm.rank
size=comm.size

MASTER_TO_SLAVE_TAG=1923784#Random unique integer

def exec_in_new_thread(code):
    run_as_new_thread(lambda:exec(code))

def slave_loop():
    while True:
        command=comm.recv(tag=MASTER_TO_SLAVE_TAG)
        #exec_in_new_thread(command)

run_as_new_thread(slave_loop)#Every processor should call this exactly once

def eval_function_from_code(code,function_name,*args,**kwargs):
    #Pass code that genrates a function called function_name
    #It will return the value that function returns when passed *args and **kwargs
    #EXAMPLE:
    # >>> eval_function_from_code('f=lambda x,y:x+y','f',10,y=20)
    # ans = 30

    assert isinstance(function_name,str),'Function name should be a string'
    assert isinstance(code         ,str),'Code should be a string'

    scope=globals()
    exec(code,scope,scope)

    assert function_name in scope,'Your code failed to create a function called '+repr(function_name)
    function=scope[function_name]
    assert callable(function),'Your code created an object called '+repr(function_name)+', but it\'s not a function'

    output=function(*args,**kwargs)
    return output

def accept_command(command):
    #Parse the command object (passed as a dict for mpi4py's convenience)
    assert isinstance(command,dict)
    function_code  =command['function_code']#The source code for the function
    function_name  =command['function_name']#The name of the function
    function_args  =command['args'         ]#args we pass to the function
    function_kwargs=command['kwargs'       ]#kwargs we pass to the fucnction
    reply_dest     =command['reply_dest'   ]#Rank we send the response to
    reply_tag      =command['reply_tag'    ]
    assert function_code  ,str
    assert function_name  ,str
    assert function_args  ,tuple
    assert function_kwargs,dict
    assert reply_dest     ,int
    assert reply_tag      ,int
    assert 0<=reply_rank<size

    #Create the reply
    reply={}#If we don't error, add a 'result' key to reply containing the function result
    try:
        reply['result']=eval_function_from_code(function_code,function_name,*function_args,**function_kwargs)
    finally:
        #No error handling yet...the indication that you have an error is that the reply is empty, and the stack trace this thread prints
        comm.isend(obj=reply,dest=reply_dest,tag=reply_tag)

def 


def parallelized(function):
    #A decorator that will parallelize a function
    function_name=function.__name__
    source_code=get_source_code(function)



def master_command(code):

    assert nodes is None or is_iterable(nodes)
    if nodes is None:nodes=list(range(size))

    for dest in nodes:
        comm.isend(obj =code,
                   dest=dest,
                   tag =MASTER_TO_SLAVE_TAG)


if rank==0:
    pseudo_terminal()
    while True:

        master_command(input('>>>'))