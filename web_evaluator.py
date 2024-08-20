import ast
from concurrent.futures import thread
import traceback
from urllib.parse import urlparse, parse_qs
import socket
import json
import time
from http.server import (
    BaseHTTPRequestHandler,
    HTTPServer,
    SimpleHTTPRequestHandler,
    # BaseHTTPServer,
    # SimpleHTTPServer,
)
import argparse
from socketserver import ThreadingMixIn
import threading
from collections import deque

import rp
from contextlib import nullcontext

rp.pip_import('requests')
import requests

rp.pip_import('icecream')
from icecream import ic

DEFAULT_SERVER_PORT = 43234 #This is an arbitrary port I chose because its easy to remember and didn't conflict with any known services I could find on https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers

#RP's Web Evaluator
#    This module provides duct-tape to connect python between computers
#    It's very fast, very versatile and very easy to set up and use.
#    However, communication is not encrypted, and also you can freeze the server if given bad code (for example, an infinite loop given by the client can hang the server)
#    With this in mind, it's extremely useful in situations where you need to offload computation from one computer to another.
#    Because it's an HTTP server, one server can service multiple clients.
#    It can also double as a web server and fileserver, allowing you to host websites with it that can even run custom python code from the frontend, similar to Jupyter lab.
#    To use this module, one computer runs the run_server() function and the other creates a Client and uses client.evaluate()
#    For testing, you can also use "python3 -m rp.experimental.web_evaluator" on client, server or both


sync_lock = threading.Lock()
# According to this stack overflow post, 
# this thread lock operates on a FIFO queue - so the order of calls sent will be preserved
# https://stackoverflow.com/questions/55951233/does-pythons-asyncio-lock-acquire-maintain-order

class Evaluation:
    """
    The Evaluation class represents the result of executing Python code on the server.
    Instances of this class are created by web_evaluator servers,
    and passed over the network to Client objects, that then deserialize and read them.
    
    It includes the following attributes:
        - code: The original Python code that was executed.
        - value: The return value of the executed code (if it didn't error)
        - error: The exception object if an error occurred during execution.
        - errored: A boolean indicating whether an error occurred.
        - is_eval: A boolean indicating whether the code was executed using eval() (as opposed to exec()).
        - is_exec: A boolean indicating whether the code was executed using exec().
    The `error` and `value` attributes are not always present - 
        but you can determine if they are from other attributes (see `create`'s docstring)

    Here's an example of accessing the attributes of an Evaluation object:
        >>> result = client.evaluate('x + y')
        >>> print(result.code)  # Output: 'x + y'
        >>> print(result.value)  # Output: 30
        >>> print(result.errored)  # Output: False
        >>> print(result.is_eval)  # Output: True
        
        >>> result = client.evaluate('invalid code')
        >>> print(result.errored)  # Output: True
        >>> print(result.error)  # Output: SyntaxError: invalid syntax
    """

    __slots__='code sync is_eval is_exec errored error value'.split()

    @staticmethod
    def create(code: str, scope: dict, sync=True):
        """
        You can pass either eval() code or exec() code to this object
        It will be evaluated using with eval() or exec(), using globals=locals=scope
        If it is eval, it will return the calculated value
        If it fails, it will return its error
        If not sync, will run the code in a new thread. Otherwise will run in main thread.
        Here are some rules to help you use the Evaluation objects, given an arbitrary evaluation object 'e' such that isinstance(e,Evaluation):
            If not e.errored and e.is_eval, then                hasattr(e,'value')
            If not e.errored and e.is_exec, then            not hasattr(e,'value')
            If     e.errored, then     hasattr(e,error) and not hasattr(e,'value')
            If not e.errored, then not hasattr(e,error)
            If not e.is_eval and not e.is_exec, then e.errored and isinstance(e.error,SyntaxError)
            Never are e.is_eval and e.is_exec both True
            Always hasattr(e,'errored') and hasattr(e,'code') and hasattr(e,'is_eval') and hasattr(e,'is_exec')
            Not Always hasattr(e,'error') or hasattr(e,'value')
        TODO: Hide optional attributes such as 'errored' behind @property's so we can give better errors than AttributeErrors when they don't exist
        """

        self=Evaluation()

        self.code=code
        self.sync=sync
        self.is_eval=False
        self.is_exec=False
        self.errored=False
        try:
            if rp.is_valid_python_syntax(self.code,mode='eval'):
                self.is_eval=True
                self.value=self._exeval(self.code,scope,sync)
            else:
                self.is_exec=True
                self._exeval(self.code,scope,sync)
        except KeyboardInterrupt:
            raise
        except BaseException as error:
            rp.print_stack_trace(error)
            self.error=error
            self.errored=True

        return self

    @staticmethod
    def from_dict(dict):
        output=Evaluation()
        for key,value in dict.items():
            setattr(output,key,value)
        return output

    def to_dict(self):
        #Dicts are more versatile with dill across python versions than custom object classes are
        output={}
        for key in self.__slots__:
            if hasattr(self,key):
                output[key]=getattr(self,key)
        return output

    @staticmethod
    def _exeval(code, scope, sync):
        return rp.exeval(code, scope)

    def _json_dumps(self):
        #TODO: Use a more powerful json dumps via external library
        out = self.to_dict()
        if self.errored:
            out["error"] = rp.r._get_stack_trace_string(self.error)
        return json.dumps(out, default=lambda value:"< json-unfriendly: %s >"%str(type(value)))
        
    def __repr__(self):
        return '<Evaluation: errored=%s is_eval=%s>'%(self.errored,self.is_eval)

def _HandlerMaker(scope:dict=None, base_class=SimpleHTTPRequestHandler):

    def update_scope(vars):
        assert isinstance(vars, dict), 'update_scope received '+str(type(vars))
        report_vars(vars)
        scope.update(vars)

    def report_vars(vars):
        rp.fansi_print("VARS: " + " ".join(sorted(vars)), "green")

    def report_code(code):
        assert isinstance(code, str)
        rp.fansi_print("CODE: " + code, "green")

    def parse_vars(string):
        """Vars can be given either as JSON or as python code to be eval'd"""
        if isinstance(string, dict):
            return string
        try:
            return json.loads(string)
        except Exception:
            return rp.exeval(string, scope)
            return ast.literal_eval(string)

    def get_rp_js_code():
        file = rp.path_join(
            rp.get_parent_directory(rp.get_module_path(rp)),
            "libs",
            "javascript",
            "rp.js",
        )
        return rp.text_file_to_string(file, use_cache=True)

    class _Handler(base_class):
        def do_POST(self):
            handlers = [self.handle_py2py, self.handle_web_query, self.handle_rp_js]
            for handler in handlers:
                handled = handler()
                if handled:
                    return
            super().do_POST() # Otherwise, behave like the original server

        def do_GET(self):
            handlers = [self.handle_py2py, self.handle_web_query, self.handle_rp_js]
            for handler in handlers:
                handled = handler()
                if handled:
                    return
            super().do_GET()

        def handle_py2py(self):
            #This type of request should only be sent by a web_evaluator.Client object
            should_handle = self.path == "/webeval/py2py"
            
            if should_handle:
                #Get the request inputs
                body = self.get_request_body()
                data = rp.bytes_to_object(body)
                code = data["code"]
                sync = data.get("sync", True) #Defaults to True for compatibility - older webevals didn't have a sync option
                assert isinstance(code, str)

                with (sync_lock if sync else nullcontext()):

                    if "vars" in data:
                        assert isinstance(data["vars"], dict)
                        update_scope(data["vars"])

                    #Do evaluation. The Evaluation.create function handles exceptions
                    report_code(code)
                    evaluation = Evaluation.create(code, scope, sync).to_dict()
                    response = evaluation

                    #Send over the result
                    content = rp.object_to_bytes(response)
                    self.send_content_bytes(content, "application/octet-stream")

            return should_handle

        #TODO:
        #    Multithreaded

        def handle_web_query(self):
            if not self.has_path_prefix("/webeval/web"):
                return False

            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            body = self.get_request_body()

            try:
                if body:
                    data = json.loads(body)
                else:
                    data = {}
            except Exception:
                raise ValueError("Can't evaluate body, please use JSON-like")

            def get_param(name, default=None):
                if name in data and name in query_params:
                    raise ValueError("Parameter '{}' specified in both URL query and request body".format(name))
                return data.get(name, query_params.get(name, [default])[0])

            code = get_param("code", "")
            sync = get_param("sync", True)
            vars_string = get_param("vars", "{}")
            content_type = get_param("content_type")  # Default to None

            with (sync_lock if sync else nullcontext()):
                try:
                    if isinstance(vars_string, str):
                        vars = parse_vars(vars_string)
                    elif isinstance(vars_string, dict):
                        vars = vars_string
                    else:
                        raise ValueError('Please provide a JSON dictionary, not a '+type(vars_string))
                    if isinstance(vars, dict):
                        update_scope(vars)
                    else:
                        raise ValueError("'vars' must be a JSON dictionary, but got type "+str(type(vars)))
                except Exception as e:
                    self.send_error(400, 'Error evaluating vars: ' + rp.r._get_stack_trace_string(e))
                    return True

                handlers = [self.handle_web_query_bytes, self.handle_web_query_json, self.handle_rp_js]
                for handler in handlers:
                    handled = handler(code, sync, content_type)
                    if handled:
                        return True

            return True

        def has_path_prefix(self, prefix):
            return self.path==prefix or self.path.startswith(prefix)

        def handle_web_query_bytes(self, code, sync, content_type=None):
            if not self.has_path_prefix("/webeval/web/bytes"):
                return False

            if content_type is None:
                content_type = "application/octet-stream"  # Default content type for bytes handler

            try:
                report_code(code)
                evaluation = Evaluation.create(code, scope, sync)
                if evaluation.errored:
                    raise evaluation.error

                if evaluation.is_exec or evaluation.value is None:
                    content = b""
                elif not isinstance(evaluation.value, bytes):
                    self.send_error(400, "Code must return a bytes object")
                    return True
                else:
                    content = evaluation.value

            except Exception as e:
                stack_trace = traceback.format_exc()
                error_message = "Error executing code: %s\n\n%s" % (str(e), stack_trace)
                self.send_error(500, error_message)
                return True

            self.send_content_bytes(content, content_type)
            return True

        def handle_web_query_json(self, code, sync, content_type=None):
            if not self.has_path_prefix("/webeval/web/evaluate"):
                return False

            if content_type is None:
                content_type = "application/json"  # Default content type for JSON handler

            report_code(code)
            evaluation = Evaluation.create(code, scope, sync)
            rp.fansi_print(evaluation, 'yellow')
            content = evaluation._json_dumps()

            self.send_content_str(content, content_type)
            return True

        def handle_rp_js(self):
            """
            In a webpage, you can use <script src="/webeval/rp.js">
            This loads rp's javascript library - useful for webeval
            """
            should_handle = self.path=="/webeval/rp.js"

            if should_handle:
                content_type="application/javascript"
                content = get_rp_js_code()
                self.send_content_str(content, content_type)

            return should_handle

        def send_content_bytes(self, content, content_type):
            assert isinstance(content, bytes)
            assert isinstance(content_type, str)
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            
        def send_content_str(self, content, content_type):
            assert isinstance(content, str)
            content_bytes = content.encode()
            self.send_content_bytes(content_bytes, content_type)

        def get_request_body(self):
            content_length = int(self.headers.get('Content-Length', 0))
            return self.rfile.read(content_length)

    return _Handler

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def run_server(server_port:int=None,scope:dict=None, handler_base_class=SimpleHTTPRequestHandler):
    """
    Set handler_base_class = SimpleHTTPRequestHandler to make it a fileserver + python-to-python server
    Set handler_base_class = BaseHTTPRequestHandler to make it a python-to-python-only server (no fileserver)

    EXAMPLE WEBSITE 1:
        #TODO: Set sync to false for image loading!

        <script src="/webeval/rp.js"></script>
        <script>
            function updateImage() {
                const textBoxValue = document.getElementById('textInput').value;
                const newUrl = rp.buildQueryUrl(
                    '/webeval/web/bytes/Bichon.png',
                    {
                        code: 'encode_image_to_bytes(cv_text_to_image(x))',
                        vars: { x: textBoxValue },
                        content_type: 'image/png',
                    }
                );

                document.getElementById('dynamicImage').src = newUrl;
            }

            window.onload = updateImage

        </script>

        <!-- Technically you can execute code by loading images, though it is janky to do it this way -->
        <img src="/webeval/web/bytes?code=from rp import *">

        <label for="textInput">Enter text:</label>
        <input type="text" id="textInput" value="Bichon" oninput="updateImage()">
        <br>
        <img id="dynamicImage">
        <br>
        <!-- Hand-Written Image Url Demo -->
        <img src="/webeval/web/bytes/custom_image_name.png?content_type=image/png&code=encode_image_to_bytes(cv_text_to_image(random_namespace_hash()))">
    
    EXAMPLE WEBSITE 2:
        # In it you can try a demo:
        #    without sync, run
        #       for x in range(10): print(x); sleep(1)
        #    then repeatedly run "x" and see the value change!

        <script src="/webeval/rp.js"></script>

        <h1>Interactive Webeval Demo</h1>

        <label for="codeInput">Enter code:</label><br>
        <textarea id="codeInput" rows="5" cols="50"></textarea><br>

        <label for="varsInput">Enter variables (JSON):</label><br>
        <textarea id="varsInput" rows="3" cols="50">{}</textarea><br>

        <div>
          <input type="checkbox" id="syncCheckbox">
          <label for="syncCheckbox">Sync</label>
        </div>

        <button id="evaluateButton">Evaluate</button>

        <h2>Result:</h2>
        <textarea id="resultOutput" rows="10" cols="50" readonly></textarea>

        <script>
          document.getElementById('evaluateButton').addEventListener('click', async function() {
            const code = document.getElementById('codeInput').value;
            const varsString = document.getElementById('varsInput').value;
            const sync = document.getElementById('syncCheckbox').checked;
            
            try {
              const vars = JSON.parse(varsString);
              const result = await rp.webeval.evaluate(code, vars, sync);
              document.getElementById('resultOutput').value = JSON.stringify(result, null, 2);
            } catch (error) {
              console.error('Evaluation error:', error);
            }
          });
        </script>



    """
    if server_port is None:
        server_port = DEFAULT_SERVER_PORT

    if scope is None:
        #If scope is not specified, use the scope of the caller.
        scope=rp.get_scope(frames_back=1)

    host_name = "0.0.0.0"
    #TODO: Use mutexes or something + an option to do this multithreadedly where default is sync, which will trigger said mutexeses in the exeval func...
    # webServer = HTTPServer(
    webServer = ThreadingHTTPServer(
        (host_name, server_port),
        _HandlerMaker(scope, base_class=handler_base_class),
    )
    print("Server started at http://%s:%s" % (rp.get_my_local_ip_address(), server_port))

    try:
        webServer.serve_forever()
    finally:
        webServer.server_close()

    print("Server stopped.")

class Client:
    def __init__(self, server_name: str = "localhost", server_port: int = None, sync=True):
        #server_name is like "127.0.1.33" or like "glass.local"
        if server_port is None:
            server_port = DEFAULT_SERVER_PORT

        self.server_port=server_port
        self.server_name=server_name
        self.sync=sync

        self.server_url='http://%s:%i/webeval/py2py'%(self.server_name,self.server_port)

    def evaluate(self,code:str='',**vars):
        """
        EXAMPLE:
            >>> while True:
            >>>    i=client.evaluate('i*20',i=load_image_from_webcam()).value
            >>>    display_image(i)
            >>>    #Kinda pointless, because we can just multiply it on the client...but it demonstrates the vars functionality
        
        EXAMPLE:
            >>> client.evaluate('import rp')
            >>> print(client.evaluate('rp.pi').value)
        
        EXAMPLE:
            >>> print(client.evaluate('1/0').error
        
        EXAMPLE:
            >>> import rp.web_evaluator as we
            >>> c=we.Client('192.168.1.182')
            >>> c.evaluate('from rp import *')
            >>> while True:
            >>>     c.evaluate('i=load_image_from_webcam()')
            >>>     c.evaluate('i=encode_image_to_bytes(i)')
            >>>     i=c.evaluate('i')
            >>>     i=i.value
            >>>     i=decode_image_from_bytes(i)
            >>>     display_image(i)
        
        EXAMPLE:
            >>> import rp.web_evaluator as we
            >>> c=we.Client('192.168.1.182')
            >>> c.evaluate(x=1,y=2,z=3)
            >>> c.evaluate('i=x*y+z')
            >>> print(c.evaluate('i').value)
        
        EXAMPLE:
            >>> #You can send multiple codes over in one trip by sending the codes as a list. This function will return a list of evaluations.
            >>> import rp.web_evaluator as we
            >>> c=we.Client('192.168.1.182')
            >>> l=c.evaluate(['1','2','1/0'])
            >>> v=[x.value for x in l if not x.errored]
            >>> # result: v=[1,2]

        TODO: Allow multiple code's to be passed in one request, which will be processed by the server as multiple Evaluation objects. Can decrease the latency by reducing number of round-trips to and from the server
        """
        

        data={}
        data['code']=code
        assert isinstance(code,str) or all(isinstance(x,str) for x in code),'Client.evaluate: code must either be a string or a list of strings'
        assert isinstance(vars,dict)
        if vars:
            data['vars']=vars
            data['sync']=self.sync
        data=rp.object_to_bytes(data)
        response=requests.request('POST',self.server_url,data=data)
        result=rp.bytes_to_object(response.content)
        assert isinstance(result,dict) or isinstance(result,list),'Client.evaluate: Bad response...please make sure the server and client are running on the same version of python and rp.'
        if isinstance(result,dict):
            result=Evaluation.from_dict(result)
        else:
            assert isinstance(result,list)
            result=[Evaluation.from_dict(x) for x in result]
        return result
    
    def __repr__(self):
        """
        Client's repr is such that we can copy client via eval(repr(client))
        This makes it easy to store and load them into text files
        """
        return "Client(%s, %s, sync=%s)"%(repr(self.server_name), repr(self.server_port), repr(self.sync))

    @staticmethod
    def from_string(string):
        """
        Client.from_string(repr(client)) is the same as copy(client)
        """
        assert string.startswith('Client(')
        return eval(string)

    def __hash__(self):
        return hash(repr(self))

class ClientWrangler:

    def __init__(self, clients: list[Client]=[], *, on_connection_error='unregister', max_jobs_per_client=1):
        """      
        The ClientWrangler class enables distributing Python computation across multiple servers.

        It maintains a pool of Client objects, each representing a connection to a server 
        running the web_evaluator module. The ClientWrangler delegates jobs to available 
        servers, automatically balancing the workload.

        Args:
            clients (list[Client], optional): A list of Client instances representing servers to manage.
                Defaults to an empty list. Clients can also be added later with register_client().
                Only one of each client instance may be added, but you can register
                    multiple client instances with the same address/port.
            
            on_connection_error (str, optional): Specifies behavior when a client encounters a connection
                error. Defaults to 'unregister'. Valid values:
                - 'unregister': Remove the client from the pool. Avoids delays due to server outages.
                - 'raise': Raise the error immediately to the caller.
                - 'wait': Keep trying the request until the server responds. May delay jobs indefinitely.
            
            max_jobs_per_client (int, optional): The maximum number of jobs that can be concurrently 
                executed by a single client before it's considered busy. Defaults to 1. 
                Values above 1 are only meaningful if the Client instances have sync=False

        Methods:
            register_client(client: Client) -> None:
                Adds a Client instance to the pool of managed servers.

            unregister_client(client: Client) -> None:  
                Removes a Client instance from the pool of managed servers.

            evaluate(code: str, **vars) -> Evaluation:
                Submits a job to be executed on the next available server.
                The code is executed as if by client.evaluate(code, **vars).
                If no servers are available, the job is queued until one becomes available.
                Returns an Evaluation object representing the result of the execution.

        Usage:
            >>> from web_evaluator import *
            >>> servers = [Client('192.168.0.1'), Client('192.168.0.2')]
            >>> wrangler = ClientWrangler(servers)

            >>> # Execute a job on the next available server  
            >>> result = wrangler.evaluate('math.sqrt(49)')

            >>> # Add a new server to the pool
            >>> new_server = Client('192.168.0.3')
            >>> wrangler.register_client(new_server)

            >>> # Remove a server from the pool
            >>> wrangler.unregister_client(servers[0]) 

            >>> # Jobs are queued until a server is available
            >>> for i in range(100):
            >>>     wrangler.evaluate(f'print({i})')

        Example:
            >>> # Run servers on ports 43234 through 43237
            >>> from web_evaluator import *
            >>> w=ClientWrangler([],on_connection_error='wait')
            >>> for _ in range(8):
            >>>     run_as_new_thread(w.evaluate,'sleep(.5);print(123)')
            >>> w.register_client(Client(server_port=43234))
            >>> w.register_client(Client(server_port=43235))
            >>> w.register_client(Client(server_port=43236))
            >>> w.register_client(Client(server_port=43237))

        The ClientWrangler abstracts the details of server communication, job queueing, 
        and load balancing, making it easier to scale Python computation across multiple machines.
        
        The original use case of this class is to allow streaming data processing for torch dataloaders,
        so we don't need to process a huge dataset's optical flow etc before training. Especially because 
        dataloader workers cannot use GPU on torch, communicating via a ClientWrangler to a bunch of 
        GPU-enabled slave workers is a good option.

        A simple way to have clients enlist is to keep a file clients.txt, and each time a relevant 
        client is made it does rp.append_line_to_file(repr(client), 'clients.txt')
        And then we do ClientWrangler(map(Client.from_string,set(rp.file_line_iterator('clients.txt'))))
        Note that if we have on_connection_error='unregister', any bad servers will be quickly removed
        """
        assert on_connection_error in ['wait', 'unregister', 'raise']
        self.on_connection_error=on_connection_error

        self._clients=[]
        self._locks=deque()
        self._free_clients=[]
        self.max_jobs_per_client=max_jobs_per_client

        #TODO: I'm not super confident this won't have race conditions.
        #I also don't know if we need all these locks. But empirically, so far, it seems to work perfectly.
        #I've added some additional locks below to mitigate what I anticipate so far
        self._update_lock = threading.Lock()
        self._register_lock = threading.Lock()
        self._evaluate_lock = threading.Lock()
        self._client_select_lock = threading.Lock()
        self._release_lock = threading.Lock()

        for client in clients:
            self.register_client(client)

    def register_client(self, client):
        """
        Adds a Client instance to the pool of managed servers.

        Args:
            client (Client): The Client instance to add to the pool.

        Raises:
            AssertionError: If the client is already registered with another ClientWrangler.
        """
        #Add an attribute _busy_count - used for the ClientWrangler
        assert not hasattr(client, '_busy_count'), 'A Client should belong to at most one ClientWrangler'
        client._busy_count=0

        with self._register_lock:
            self._clients.append(client)
            self._update()

    def unregister_client(self, client):
        """
        Removes a Client instance from the pool of managed servers.

        Args:
            client (Client): The Client instance to remove from the pool.
        """
        with self._register_lock:
            self._clients = [c for c in self._clients if c is not client]

    def _update(self):
        """
        Internal, private method.

        Updates the internal state of the ClientWrangler.
        Possibly releases a thread lock to enable a queued evalution job.

        This method is called automatically after registering or unregistering clients,
        or after a job is submitted or completed. It updates the list of available servers
        and assigns pending jobs to free servers if possible.
        """
        with self._update_lock:
            self._free_clients = [c for c in self._clients if c._busy_count<self.max_jobs_per_client]
            if self._locks and self._free_clients:
                self._release_lock.acquire()
                self._locks.popleft().release()
                self._chosen_client = rp.random_element(self._free_clients)
                self._chosen_client._busy_count+=1

    def evaluate(self, code, **vars):
        """
        Submits a job to be executed on the next available server. Blocks until evaluated.

        This method behaves like Client.evaluate(code, **vars), but automatically selects
        a server from the pool of registered clients. If no servers are available, the job
        is queued until a server becomes free.

        Args:
            code (str): The Python code to execute on the server.
            **vars: Additional variables to pass to the server for the job execution.

        Returns:
            Evaluation: An Evaluation object representing the result of the job execution.

        Note:
            If no clients are registered, this method will block until a client is added
            using register_client().
        """
        
        with self._evaluate_lock:
            lock = threading.Lock()
            lock.acquire()

            self._locks.append(lock)

            self._update() 

        #Second time we acquire - will lock if _update didn't unlock it
        lock.acquire()
        client = self._chosen_client
        self._release_lock.release()

        self._update()

        try:
            result = client.evaluate(code, **vars)
            return result
        
        except requests.exceptions.ConnectionError as e:
            rp.fansi_print("Warning: "+str(client)+" is unreachable! Error: "+str(e), 'red')
            
            if self.on_connection_error == 'unregister':
                #Delete dead clients
                self.unregister_client(client)
                return self.evaluate(code, **vars)
            elif self.on_connection_error == 'raise':
                #Throw an error right away - handle it elsewhere
                raise
            elif self.on_connection_error == 'wait':
                while True:
                    try:
                        result = client.evaluate(code, **vars)
                        return result
                    except requests.exceptions.ConnectionError:
                        time.sleep(1)
            else:
                assert False, 'Invalid self.on_connection_error value: '+str(self.on_connection_error)

        finally:
            client._busy_count-=1
            assert client._busy_count>=0
            self._update()
        
            


def interactive_mode():
    if rp.input_yes_no("Is this the server? No means this is the client."):
        print("Running the server.")
        run_server()
    else:
        print("Running the client.")
        import readline
        address = input("Enter the server's IP: ") or 'localhost'
        client = Client(address)
        while True:
            try:
                rp.pretty_print(client.evaluate(input(" >>> ")).to_dict())
            except Exception:
                rp.print_stack_trace()

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(prog='web_evaluator.py', description='Web Evaluator: Remote Python code execution server and client',
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-p', '--port', type=int, default=DEFAULT_SERVER_PORT, help='Server port (default: 43234)')

        subparsers = parser.add_subparsers(dest='mode', title='Modes', metavar='{server,s,client,c}', help='Select "server" or "client" mode')

        # Server mode arguments
        server_parser = subparsers.add_parser('server', aliases=['s'], help='Run the script as a server')

        # Client mode arguments
        client_parser = subparsers.add_parser('client', aliases=['c'], help='Run the script as a client')
        client_parser.add_argument('server_ip', type=str, help='Server IP address (e.g., 192.168.1.10)')

        parser.epilog = '''Examples:
      Run the script interactively (no arguments):
        python3 script_name.py

      Run as a server with the default port:
        python3 script_name.py server

      Run as a server with a custom port:
        python3 script_name.py server -p 12345

      Run as a client connecting to a server IP and default port:
        python3 script_name.py client 192.168.1.10

      Run as a client connecting to a server IP and custom port:
        python3 script_name.py client 192.168.1.10 -p 12345
        '''

        args, unknown = parser.parse_known_args()

        if unknown:
            print("Unknown arguments provided. Switching to interactive mode.")
            interactive_mode()
        elif args.mode in ('server', 's'):
            print("Running the server.")
            run_server(server_port=args.port)
        elif args.mode in ('client', 'c'):
            print("Running the client.")
            client = Client(args.server_ip, server_port=args.port)
            import readline
            while True:
                print(client.evaluate(input(" >>> ")))
        else:
            interactive_mode()

    except KeyboardInterrupt:
        print("Received KeyboardInterrupt. Exiting.")

