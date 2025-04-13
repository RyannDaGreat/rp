import argparse
import ast
import os
import json
import textwrap
import threading
import time
import traceback
from collections import deque
from contextlib import nullcontext
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import parse_qs, urlparse

import rp

rp.pip_import('requests')
import requests

DEFAULT_SERVER_PORT = 43234 #This is an arbitrary port I chose because its easy to remember and didn't conflict with any known services I could find on https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers
DEFAULT_DELEGATION_SERVER_PORT = 33234 #The port for delegation servers is different, making them easy to find if we have many servers

#RP's Web Evaluator
#    This module provides duct-tape to connect python between computers
#    It's very fast, very versatile and very easy to set up and use.
#    However, communication is not encrypted, and also you can freeze the server if given bad code (for example, an infinite loop given by the client can hang the server)
#    With this in mind, it's extremely useful in situations where you need to offload computation from one computer to another.
#    Because it's an HTTP server, one server can service multiple clients.
#    It can also double as a web server and fileserver, allowing you to host websites with it that can even run custom python code from the frontend, similar to Jupyter lab.
#    To use this module, one computer runs the run_server() function and the other creates a Client and uses client.evaluate()
#    For testing, you can also use "python3 -m rp.experimental.web_evaluator" on client, server or both

"""

TODO:
    - ClientDelegator server: dynamically reads from a roster and updates who's available, and proxies requests to its workers. This will balance workload.
          Downside: traffic will have to pass through it as a bottleneck. Oh well - perhaps it can become a traffic controller in the future. Should keep it extensible.
    - Client Timeout options. Useful to make a ping operator to check if server online and responsive.

        Todo:
            This class can gracefully balance evaluations between clients within a multithreaded context,
            but multiple ClientDelegator's in multiple processes will trip over eachother's shoelaces
            (nothing catastrophic, but it will be slower than a centralized one).
            One solution is to have a single server dedicated to delegation, that all workers pass requests through.
            It would be a middleman through which all traffic passes. This might hoog bandwidth and slow down 

"""


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
        - is_exec: A boolean indicating whether the code was executed using exec(). Will be (not is_eval)
    The `error` attribute is not always present - it is present if any only if errored==True
    Likewise, the `value` attribute is present if and only if errored==False

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
            if rp.r._is_valid_exeval_python_syntax(self.code,mode='eval'):
                self.is_eval=True
                self.value=self._exeval(self.code,scope,sync)
            else:
                self.is_exec=True
                self._exeval(self.code,scope,sync)
        except KeyboardInterrupt:
            raise
        except BaseException as error:
            rp.print_stack_trace()

            #Add the stack trace into the error
            stack_trace = '[WEB_EVALUATOR EVALUATION ERROR]\n'+traceback.format_exc()
            error.args = (stack_trace,) + error.args[1:]

            self.error = error
            self.errored = True


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

def _HandlerMaker(scope:dict=None, *, base_class=SimpleHTTPRequestHandler, default_sync=True):
    assert isinstance(default_sync, bool)

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
                sync = data.get("sync", default_sync) #Defaults to True for compatibility - older webevals didn't have a sync option
                assert isinstance(code, str), type(code)
                assert isinstance(sync, bool), sync

                with (sync_lock if sync else nullcontext()):

                    if "vars" in data:
                        assert isinstance(data["vars"], dict)
                        update_scope(data["vars"])

                    #Do evaluation. The Evaluation.create function handles exceptions
                    report_code(code)
                    evaluation = Evaluation.create(code, scope, sync).to_dict()
                    response = evaluation

                    #Send over the result
                    try:
                        content = rp.object_to_bytes(response)
                    except Exception as e:
                        #If the output involves something we can't pickle, return that as an error
                        if e:
                            response['errored']=True
                            response['error']=e
                            if 'value' in response:
                                del response['value']
                            rp.fansi_print("ERROR When serializing response:",'red','bold')
                            rp.print_stack_trace()
                            content = rp.object_to_bytes(response)

                    self.send_content_bytes(content, "application/octet-stream")

            return should_handle

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
            sync = get_param("sync", default_sync)
            vars_string = get_param("vars", "{}")
            content_type = get_param("content_type")  # Default to None
            assert isinstance(sync, bool), sync
            assert isinstance(code, str), type(code)

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

def run_server(server_port:int=None,
               scope:dict=None,
               *,
               sync=True,
               handler_base_class=SimpleHTTPRequestHandler):
    """
    Runs a web_evaluator server, which provides an HTTP interface for remote Python code execution (and can double as a fileserver as well)

    Args:
        server_port (int, optional): The port number on which the server will listen for incoming connections. 
            If not provided, it defaults to the value of `rp.web_evaluator.DEFAULT_SERVER_PORT` (43234).
            Choose a port that is not already in use by other services.

        scope (dict, optional): A dictionary containing the scope we run exec/eval inside. Pass it globals() or some custom dictionary to control what run_server sees / has access to. By default, it uses the scope of this function's caller.

        sync (bool): The default value of sync if not specified by the client. Determines whether this server is multithreaded or singlethreaded on a request that doesnt specify whether it should be or not. Defaults to True (synchronous execution - aka one handling request at a time)

        handler_base_class (class, optional): The base class for the HTTP request handler. This determines the capabilities of the server.
            If `SimpleHTTPRequestHandler` (default), the server will serve files from the current directory in addition to 
            accepting code execution requests. This is useful for serving HTML/JS files that can interact with the Python backend.
            If `BaseHTTPRequestHandler`, the server will only support code execution requests and will not serve files.
            You can also provide your own custom handler class to extend the server's functionality.

    Returns:
        None. The function will block indefinitely to handle incoming HTTP requests until the process is terminated.

    The server supports several types of requests, including:
        - Python code execution requests (POST to /webeval/py2py)
        - Python code execution with result formatting (POST to /webeval/web/evaluate)
        - Binary response from Python code execution (POST to /webeval/web/bytes) 
        - JavaScript library hosting (GET /webeval/rp.js)

    Clients can interact with this server using the `rp.web_evaluator.Client` class or by making HTTP requests directly (such as the following web-browser-based examples)


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
    assert isinstance(sync, bool)

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
        _HandlerMaker(scope, base_class=handler_base_class, default_sync=sync),
    )
    print("Server started at http://%s:%s" % (rp.get_my_local_ip_address(), server_port))

    try:
        webServer.serve_forever()
    finally:
        webServer.server_close()

    print("Server stopped.")

class Client:
    DEFAULT_PORT = DEFAULT_SERVER_PORT
    def __init__(self, server_name: str = "localhost", server_port: int = None, *, sync=None, timeout=None):
        """
        Initialize a Client object, which is used to interact with a web_evaluator server (started with rp.web_evaluator.run_server).
        The Client stores the address and port of the server, as well as other settings such as sync (synchronous server-side execution vs asynchronous)

        Args:
            - server_name (str): server_name is like "127.0.1.33" or like "glass.local"
            - server_port(int): the port of the server. Defaults to rp.web_evaluator.Client.DEFAULT_PORT
            - sync (bool, optional): Whether commands sent by this Client should be synchronous or not. If sync is None, uses the server's default sync option. If bool, overrides it. See run_server's doc too.
            - timeout (float, optional): If not None, connections will timeout in that number of seconds
        """
        if server_port is None:
            server_port = self.DEFAULT_PORT

        assert sync is None or isinstance(sync, bool)

        self.server_port=server_port
        self.server_name=server_name
        self.sync=sync
        self.timeout=timeout

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

        EXEVAL DIRECTIVES:
            [I may remove this documentation in the future, as rp.exeval's docstring has a near-duplicate of this information]

            The Client class uses the `exeval` function internally to execute code on the server. The `exeval` function
            supports directives that provide additional functionality (please see rp.exeval for a full list):

            1. `%return <variable_name>`: Allows specifying a variable to be returned from the executed code's scope.
               This is useful when executing code that cannot be evaluated as an expression.

               Example:
                   >>> code = '''
                       %return result
                       a = 10
                       b = 20
                       result = a + b
                       '''
                   >>> result = client.evaluate(code)
                   >>> print(result.value)
                   30

               Example:
                   >>> code = '''
                       %return output
                       %private_scope
                       def f():
                           import time
                           return time.time()
                       output = f()
                       '''
                   >>> result = client.evaluate(code)
                   >>> print(result.value)
                   1724402196.466829

            2. `%private_scope`: Creates a private copy of the scope before executing the code. This directive ensures that
               variable changes made during code execution are not persistent between requests. It is particularly important
               when `sync=False` to prevent unintended side effects and maintain the integrity of the server's scope.

               Example (without `%private_scope`):
                   >>> code1 = 'x = 10'
                   >>> code2 = 'print(x)'
                   >>> client.evaluate(code1)
                   >>> client.evaluate(code2)
                   10

               Example (with `%private_scope`):
                   >>> code1 = '''
                       %private_scope
                       x = 10
                       '''
                   >>> code2 = 'print(x)'
                   >>> client.evaluate(code1)
                   >>> client.evaluate(code2).error
                   NameError: name 'x' is not defined

               In the example without `%private_scope`, the variable `x` is persisted between requests, allowing the second
               request to access its value. However, with `%private_scope`, each request has its own isolated scope, and
               variables defined in one request are not accessible in subsequent requests.

            3. `prepend_code <python_expression>`: Prepends some code to your command, specified by a given python expression.
               This allows for creation of variables in the given scope from server-side code, which cannot happen without this directive.

               Example:
                    >>> exeval('%prepend_code rp.load_text_file("code.py")')

               (see rp.exeval's docstring for more examples)
            
            3. `append_code` <python_expression>`: Just like prepend_code, but adds code to the end instead of the beginning

               Example:
                    >>> exeval('%append_code rp.load_text_file("code.py")')

               (see rp.exeval's docstring for more examples)
        """
        
        return self._evaluate(
            code=code,
            vars=vars,
            server_url=self.server_url,
            sync=self.sync,
            timeout=self.timeout,
        )

    @staticmethod
    def _evaluate(*, code, vars, server_url, sync, timeout):
        data={}
        data['code']=code
        assert isinstance(code,str) or all(isinstance(x,str) for x in code),'Client.evaluate: code must either be a string or a list of strings'
        assert isinstance(vars,dict)
        if vars:
            data['vars']=vars
        if sync is not None:
            data['sync']=sync
        data=rp.object_to_bytes(data)

        # https://stackoverflow.com/questions/21965484/timeout-for-python-requests-get-entire-response
        response = requests.request("POST", server_url, data=data, timeout=timeout)

        result=rp.bytes_to_object(response.content)
        assert isinstance(result,dict) or isinstance(result,list),'Client.evaluate: Bad response...please make sure the server and client are running on the same version of python and rp.'
        if isinstance(result,dict):
            result=Evaluation.from_dict(result)
        else:
            assert isinstance(result,list)
            result=[Evaluation.from_dict(x) for x in result]
        return result

    def ping(self):
        """ Returns a float of how long it took to reach the server asynchronously """
        start_time = time.time()

        #This is literally just for the sake of timing...
        self._evaluate(
            code="#PING",
            vars={},
            server_url=self.server_url,
            sync=False,
            timeout=self.timeout,
        )

        end_time = time.time()

        elapsed_time = end_time - start_time

        return elapsed_time
    
    def __repr__(self):
        """
        Client's repr is such that we can copy client via eval(repr(client))
        This makes it easy to store and load them into text files
        """
        args = [repr(self.server_name), repr(self.server_port)]
        if self.sync is not None:
            args.append("sync={}".format(repr(self.sync)))
        if self.timeout is not None:
            args.append("timeout={}".format(repr(self.timeout)))

        return "{}({})".format(type(self).__name__, ", ".join(args))

    @staticmethod
    def from_string(string):
        """
        Client.from_string(repr(client)) is the same as copy.copy(client)
        """
        output = eval(string)
        assert isinstance(output, Client)
        return output

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, x):
        if not isinstance(x, Client):
            return False
        return repr(self) == repr(x)

class ClientDelegator:

    def __init__(self, clients=[], *, on_connection_error='unregister', max_jobs_per_client=1):
        """      
        The ClientDelegator class enables distributing Python computation across multiple servers.

        It maintains a pool of Client objects, each representing a connection to a server 
        running the web_evaluator module. The ClientDelegator delegates jobs to available 
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
            >>> delegator = ClientDelegator(servers)

            >>> # Execute a job on the next available server  
            >>> result = delegator.evaluate('math.sqrt(49)')

            >>> # Add a new server to the pool
            >>> new_server = Client('192.168.0.3')
            >>> delegator.register_client(new_server)

            >>> # Remove a server from the pool
            >>> delegator.unregister_client(servers[0]) 

            >>> # Jobs are queued until a server is available
            >>> for i in range(100):
            >>>     delegator.evaluate(f'print({i})')

        Example:
            >>> # Run servers on ports 43234 through 43237
            >>> from web_evaluator import *
            >>> w=ClientDelegator([],on_connection_error='wait')
            >>> for _ in range(8):
            >>>     run_as_new_thread(w.evaluate,'sleep(.5);print(123)')
            >>> w.register_client(Client(server_port=43234))
            >>> w.register_client(Client(server_port=43235))
            >>> w.register_client(Client(server_port=43236))
            >>> w.register_client(Client(server_port=43237))

        The ClientDelegator abstracts the details of server communication, job queueing, 
        and load balancing, making it easier to scale Python computation across multiple machines.
        
        The original use case of this class is to allow streaming data processing for torch dataloaders,
        so we don't need to process a huge dataset's optical flow etc before training. Especially because 
        dataloader workers cannot use GPU on torch, communicating via a ClientDelegator to a bunch of 
        GPU-enabled slave workers is a good option.
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

    def register_client(self, client, *, unique=True, after_ping=False, silent=False):
        """
        Adds a Client instance to the pool of managed servers.

        Args:
            client (Client): The Client instance to add to the pool.
            unique (bool): If true, will not register the same client twice
            after_ping (bool): If true, will try to ping the client in a separate thread, and upon success it will be registered
            silent (bool): If True, won't print anything

        Raises:
            AssertionError: If the client is already registered with another ClientDelegator.
        """

        if unique and client in self._clients:
            #TODO: This is a duplicate code block. Simplify somwhow?
            #If unique is True, don't add the same client twice.
            if not silent:
                rp.fansi_print("ClientDelegator.register_client: Skipped duplicate registration: "+str(client), 'yellow')
            return

        if after_ping:
            @rp.run_as_new_thread
            def register_client_after_ping():
                try:
                    # print("Pinging",client) #Good for debugging
                    client.ping()
                except Exception as e:
                    if not silent:
                        rp.fansi_print("ClientDelegator.register_client: Didn't register - failed to ping "+str(client)+" because of Error: "+str(e), 'yellow')
                    return #Don't register it!

                self.register_client(
                    client,
                    unique=unique,
                    after_ping=False,
                )

        else:
            with self._register_lock:
                if unique and client in self._clients:
                    #If unique is True, don't add the same client twice.
                    if not silent:
                        rp.fansi_print("ClientDelegator.register_client: Skipped duplicate registration: "+str(client), 'yellow')
                    return

                #Add an attribute _busy_count - used for the ClientDelegator
                assert not hasattr(client, '_busy_count'), 'A Client should belong to at most one ClientDelegator'
                client._busy_count=0


                rp.fansi_print("ClientDelegator.register_client: Registered "+str(client), 'green', 'bold')
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

        rp.fansi_print("ClientDelegator.unregister_client: Unregistered "+str(client), 'magenta')

    def register_clients(self, clients, **kwargs):
        """ Plural of register_client """
        for client in clients:
            self.register_client(client, **kwargs)

    def unregister_clients(self, clients):
        """ Plural of unregister_client """
        for client in clients:
            self.unregister_client(client)

    def _update(self):
        """
        Internal, private method.

        Updates the internal state of the ClientDelegator.
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

        if not self._clients:
            rp.fansi_print("ClientDelegator.evaluate: We currently have no clients. Evaluation is paused until a new client is registered.", 'yellow')
        
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
            rp.fansi_print("Warning: "+str(client)+" is unreachable! Error: "+str(e), 'yellow')
            
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

            #TODO: Figure out why this below assertion sometimes triggers. Makes no sense to me. For now I'll ignore it and just make a warning.
            #assert client._busy_count>=0
            if client._busy_count<0:
                rp.fansi_print("rp.web_evaluator.ClientDelegator.evaluate: client._busy_count<0 - this shouldn't be possible. Setting it to 0. Todo: Investigate this.", 'red', 'bold')
                client.busy_count=0

            self._update()
        
class ClientRoster:
    """
    The ClientRoster class manages a roster of clients for the ClientDelegator.

    It provides methods to load clients from your filesystem, clear the roster, and register new clients.
    Clients can register themselves to the roster, allowing the ClientDelegator to discover and utilize them.

    Args:
        location (str, optional): The folder path where the client roster is stored.
            Defaults to a folder named 'web_evaluator.py.default_client_roster' in the same directory as the script.

    Methods:
        load_clients(silent: bool = False) -> list[Client]:
            Loads the clients from the roster folder and returns them as a list of Client instances.
            If 'unique' is True (default), only unique clients will be loaded.
            If 'silent' is True, no output will be printed during loading.

        clear() -> None:
            Clears the contents of the roster foldefolder.

        register(server_port: int = DEFAULT_SERVER_PORT, server_name: str = None, sync: bool = True, silent: bool = False) -> None:
            Registers a new server/client to the roster folder.
            If server_name is not provided, the local IP address is used.
            If 'sync' is True (default), the client will use synchronous communication.
            If 'silent' is True, no output will be printed during registration.

    Example:
        >>> from web_evaluator import ClientRoster, ClientDelegator, run_server

        >>> # Register a server to the roster. Run this on several processes.
        >>> port = rp.get_next_free_port(43234, 'localhost')
        >>> roster = ClientRoster()
        >>> roster.register(port)
        >>> run_server(port)

        >>> # In a separate process, load clients from the roster and create a ClientDelegator
        >>> roster = ClientRoster()
        >>> clients = roster.load_clients()
        >>> delegator = ClientDelegator(clients)
        >>> result = delegator.evaluate('math.sqrt(49)')

    It stores clients via filenames in a roster folder, which makes it more robust to race conditions than maintaining a text file
    """

    def __init__(self, location=None):
        """
        Initializes a new instance of the ClientRoster class.

        Args:
            location (str, optional): The folder path where the client roster is stored.
                Defaults to a folder named 'web_evaluator.py.default_client_roster' in the same directory as the script.
        """
        if location is None:
            # The default client roster is kept in rp's directory
            location = __file__ + '.default_client_roster'

        location = rp.get_absolute_path(location)

        self.location = location

    def load_clients(self, *, silent=False):
        """
        Loads the clients from the roster folder and returns them as a list of Client instances.

        Args:
            silent (bool, optional): If True, no output will be printed during loading. Defaults to False.

        Returns:
            list[Client]: A list of Client instances loaded from the roster folder.
        """
        if not silent:
            rp.fansi_print("rp.web_evaluator.ClientRoster: Loading clients from " + self.location, 'green')

        if not rp.folder_exists(self.location):
            if not silent:
                rp.fansi_print("rp.web_evaluator.ClientRoster: Roster folder doesn't exist; loaded no clients: " + self.location, 'yellow')
            return []

        lines = os.listdir(self.location)

        clients = []
        for line in lines:
            line = line.strip()

            if line:
                client = Client.from_string(line)

                if not silent:
                    rp.fansi_print("   - Added " + str(client), 'green')

                clients.append(client)

        return clients

    def clear(self):
        """
        Clears the contents of the roster folder.
        """
        #Move it then delete it so it's immediately deleted
        rp.delete_folder(rp.move_folder(self.location, rp.temporary_file_path()))

    def register(self, server_port=DEFAULT_SERVER_PORT, server_name=None, *, sync=True, silent=False):
        """
        Registers a new client to the roster folder.

        Args:
            server_port (int, optional): The port number of the server. Defaults to DEFAULT_SERVER_PORT.
            server_name (str, optional): The name or IP address of the server.
                If not provided, the local IP address is used.
            sync (bool, optional): Indicates whether the client should use synchronous communication.
                Defaults to True.
            silent (bool, optional): If True, no output will be printed during registration. Defaults to False.
        """
        if server_name is None:
            server_name = rp.get_my_local_ip_address()

        client = Client(
            server_name=server_name,
            server_port=server_port,
            sync=sync,
        )

        line = repr(client)

        client_file = rp.path_join(self.location, line)

        if rp.path_exists(client_file):
            if not silent:
                rp.fansi_print("rp.web_evaluator.ClientRoster: Did NOT register duplicate client " + line + " to " + self.location, 'yellow')
        else:
            rp.touch_file(client_file)

            if not silent:
                rp.fansi_print("rp.web_evaluator.ClientRoster: Enlisted " + line + " to " + self.location, 'green')

    def __repr__(self):
        return "ClientRoster(%s)" % repr(self.location)

def run_delegation_server(server_port=None,
                          *,
                          delegator=None,
                          roster=None,
                          refresh_interval = 5
                          ):

    """
    Starts a delegation server that manages a pool of web_evaluator servers for distributed computation.

    The delegation server acts as a centralized coordinator for a group of web_evaluator servers. 
    It maintains a roster of available servers and delegates incoming jobs to them using a ClientDelegator instance.

    Clients can submit jobs to the delegation server, which then forwards the jobs to the next available web_evaluator server.
    This allows clients to utilize multiple servers for computation without needing to manage the server connections directly.

    Key features and considerations:
    - Provides a simplified interface for clients to submit jobs without worrying about server management
    - Delegates incoming jobs to available servers using a ClientDelegator instance
    - Utilizes a ClientRoster to discover and manage a list of available web_evaluator servers
    - Automatically refreshes the server roster at a configurable interval to handle dynamic additions or removals

    Args:
        server_port (int): The port we run the delegation server on. Defaults to DEFAULT_DELEGATION_SERVER_PORT
        refresh_interval (int): The number of seconds we wait before re-reading the roster and trying to add its clients
        roster (ClientRoster, optional)
        delegator (ClientDelegator, optional)

    TODO: Computation is wasted pickling and unpickling the objects before they're forwarded. Ideally, this would be entirely agnostic to the type of HTTP requests that pass through it - and forward the requests through steamingly to minimize latency. 
    Also, ideally this wouldn't have to forward the data at all - instead keeping track of which clients are busy and which aren't, and simply returning the client they should make a request with. However, this requires bidirectional communication (or timeouts in the event of errors) - which currently goes against Web Evaluator's assymetrical setup.
    """

    #If not specified, create the default versions
    if roster    is None: roster    = ClientRoster()
    if delegator is None: delegator = ClientDelegator()
    if server_port is None: server_port = DEFAULT_DELEGATION_SERVER_PORT

    if rp.get_port_is_taken(server_port):
        raise RuntimeError("rp.web_evaluator.run_delegation_server: port %i is already taken!" % server_port)

    stop_refreshing = False

    def refresh_clients():
        try:
            roster_clients = roster.load_clients(silent=True)

            delegator.register_clients(
                roster_clients,
                after_ping=True,
                silent=True,
            )

        except Exception:
            rp.fansi_print("run_delegation_server: Failed to load from "+str(roster), 'red', 'bold')
            rp.print_stack_trace()

    try:
        @rp.run_as_new_thread
        def refresh_loop():
            while not stop_refreshing:
                refresh_clients()
                time.sleep(refresh_interval)

        scope = dict(
            roster = roster,
            delegator = delegator,
        )
                
        run_server(server_port, scope=scope, sync=False)

    finally:
        #Exiting the server - kill loose threads
        stop_refreshing = True

class NotADelegationServerError(Exception):
    pass

class DelegationClient(Client):
    """
    A Client meant to be used for talking to a server launched via rp.web_evaluator.run_delegation_server

    The DelegationClient extends the base Client class and is specifically designed to communicate with a server
    running the `run_delegation_server` function. It provides a transparent way to execute code on a pool of
    web_evaluator servers managed by the delegation server.

    The `evaluate` method of the DelegationClient sends the code and variables to the delegation server,
    which then forwards the job to the next available web_evaluator server in its pool. The result is returned
    back to the client through the delegation server.

    TODO: Make this more efficient - see run_delegation_server's TODO. As a blackbox, the signatures can stay the same
    """
    DEFAULT_PORT = DEFAULT_DELEGATION_SERVER_PORT
    def evaluate(self, code, **vars):
        vars_string = ", ".join(x+'='+x for x in vars)

        code = rp.unindent(
            """
            %private_scope
            %return result
            import rp.web_evaluator as we
            if 'delegator' not in dir():
                raise we.NotADelegationServerError
            result = delegator.evaluate(CODE, VARS)
            """
        ).replace('CODE', repr(code)).replace('VARS', vars_string)

        result = super().evaluate(code, **vars)

        if not result.errored:
            result = result.value
        else:
            rp.fansi_print("Delegatee Error: "+str(result.error),'red','bold')

        return result

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



