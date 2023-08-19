import socket
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import argparse

import rp

rp.pip_import('requests')
import requests

DEFAULT_SERVER_PORT = 43234 #This is an arbitrary port I chose because its easy to remember and didn't conflict with any known services I could find on https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers

#RP's Web Evaluator
#    This module provides duct-tape to connect python between computers
#    It's very fast, very versatile and very easy to set up and use.
#    However, communication is not encrypted, and also you can freeze the server if given bad code (for example, an infinite loop given by the client can hang the server)
#    With this in mind, it's extremely useful in situations where you need to offload computation from one computer to another.
#    Because it's an HTTP server, one server can service multiple clients.
#    To use this module, one computer runs the run_server() function and the other creates a Client and uses client.evaluate()
#    For testing, you can also use "python3 -m rp.experimental.web_evaluator" on client, server or both

class Evaluation:
    __slots__='code is_eval is_exec errored error value'.split()

    @staticmethod
    def create(code:str,scope:dict):
        #You can pass either eval() code or exec() code to this object
        #It will be evaluated using with eval() or exec(), using globals=locals=scope
        #If it is eval, it will return the calculated value
        #If it fails, it will return its error
        #Here are some rules to help you use the Evaluation objects, given an arbitrary evaluation object 'e' such that isinstance(e,Evaluation):
        #    If not e.errored and e.is_eval, then                hasattr(e,'value')
        #    If not e.errored and e.is_exec, then            not hasattr(e,'value')
        #    If     e.errored, then     hasattr(e,error) and not hasattr(e,'value')
        #    If not e.errored, then not hasattr(e,error)
        #    If not e.is_eval and not e.is_exec, then e.errored and isinstance(e.error,SyntaxError)
        #    Never are e.is_eval and e.is_exec both True
        #    Always hasattr(e,'errored') and hasattr(e,'code') and hasattr(e,'is_eval') and hasattr(e,'is_exec')
        #    Not Always hasattr(e,'error') or hasattr(e,'value')
        #TODO: Hide optional attributes such as 'errored' behind @property's so we can give better errors than AttributeErrors when they don't exist

        self=Evaluation()

        self.code=code
        self.is_eval=False
        self.is_exec=False
        self.errored=False
        try:
            if rp.is_valid_python_syntax(self.code,mode='eval'):
                self.is_eval=True
                self.value=eval(self.code,scope,scope)
            else:
                self.is_exec=True
                exec(self.code,scope,scope)
        except KeyboardInterrupt:
            raise
        except BaseException as error:
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

    def __repr__(self):
        return '<Evaluation: errored=%s is_eval=%s>'%(self.errored,self.is_eval)

def _HandlerMaker(scope:dict=None):
    class _Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "application/octet-stream")
            self.end_headers()
            body=self.get_request_body()
            data=rp.bytes_to_object(body)
            code=data['code']
            if 'vars' in data:
                assert isinstance(data['vars'],dict)
                rp.fansi_print("VARS: "+' '.join(sorted(data['vars'])),'green')
                scope.update(data['vars'])
            if isinstance(code,list):
                #Process multiple Evaluations in bulk
                for i,e in enumerate(code):
                    rp.fansi_print("CODE %i/%i: "%(i+1,len(code))+e,'green')
                evaluations=[Evaluation.create(x,scope).to_dict() for x in code]
                response=evaluations
            else:
                assert isinstance(code,str)
                rp.fansi_print("CODE: "+code,'green')
                evaluation=Evaluation.create(code,scope).to_dict()
                response=evaluation
            response=rp.object_to_bytes(response)
            self.wfile.write(response)

        def get_request_body(self):
            length=int(self.headers.get('Content-Length'))
            body = self.rfile.read(length)
            return body

    return _Handler

def run_server(server_port:int=None,scope:dict=None):
    if server_port is None:
        server_port = DEFAULT_SERVER_PORT

    if scope is None:
        #If scope is not specified, use the scope of the caller.
        scope=rp.get_scope(level=1)

    host_name = "0.0.0.0"
    webServer = HTTPServer((host_name, server_port), _HandlerMaker(scope))
    print("Server started at http://%s:%s" % (rp.get_my_local_ip_address(), server_port))

    try:
        webServer.serve_forever()
    finally:
        webServer.server_close()

    print("Server stopped.")

class Client:
    def __init__(self,server_name:str="localhost",server_port:int=None):
        #server_name is like "127.0.1.33" or like "glass.local"
        if server_port is None:
            server_port = DEFAULT_SERVER_PORT

        self.server_port=server_port
        self.server_name=server_name
        self.server_url='http://%s:%i'%(self.server_name,self.server_port)

    def evaluate(self,code:str='',**vars):
        #TODO: Allow multiple code's to be passed in one request, which will be processed by the server as multiple Evaluation objects. Can decrease the latency by reducing number of round-trips to and from the server
        #
        #EXAMPLE:
        #    while True:
        #       i=client.evaluate('i*20',i=load_image_from_webcam()).value
        #       display_image(i)
        #       #Kinda pointless, because we can just multiply it on the client...but it demonstrates the vars functionality
        #
        #EXAMPLE:
        #    client.evaluate('import rp')
        #    print(client.evaluate('rp.pi').value)
        #
        #EXAMPLE:
        #    print(client.evaluate('1/0').error
        #
        #EXAMPLE:
        #    import rp.experimental.web_evaluator as we
        #    c=we.Client('192.168.1.182')
        #    c.evaluate('from rp import *')
        #    while True:
        #        c.evaluate('i=load_image_from_webcam()')
        #        c.evaluate('i=encode_image_to_bytes(i)')
        #        i=c.evaluate('i')
        #        i=i.value
        #        i=decode_image_from_bytes(i)
        #        display_image(i)
        #
        #EXAMPLE:
        #    import rp.experimental.web_evaluator as we
        #    c=we.Client('192.168.1.182')
        #    c.evaluate(x=1,y=2,z=3)
        #    c.evaluate('i=x*y+z')
        #    print(c.evaluate('i').value)
        #
        #EXAMPLE:
        #    #You can send multiple codes over in one trip by sending the codes as a list. This function will return a list of evaluations.
        #    import rp.experimental.web_evaluator as we
        #    c=we.Client('192.168.1.182')
        #    l=c.evaluate(['1','2','1/0'])
        #    v=[x.value for x in l if not x.errored]
        #    # result: v=[1,2]
        #

        data={}
        data['code']=code
        assert isinstance(code,str) or all(isinstance(x,str) for x in code),'Client.evaluate: code must either be a string or a list of strings'
        assert isinstance(vars,dict)
        if vars:
            data['vars']=vars
        data=rp.object_to_bytes(data)
        response=requests.request('GET',self.server_url,data=data)
        result=rp.bytes_to_object(response.content)
        assert isinstance(result,dict) or isinstance(result,list),'Client.evaluate: Bad response...please make sure the server and client are running on the same version of python and rp.'
        if isinstance(result,dict):
            result=Evaluation.from_dict(result)
        else:
            assert isinstance(result,list)
            result=[Evaluation.from_dict(x) for x in result]
        return result


def interactive_mode():
    if rp.input_yes_no("Is this the server? No means this is the client."):
        print("Running the server.")
        run_server()
    else:
        print("Running the client.")
        import readline
        client = Client(input("Enter the server's IP: "))
        while True:
            print(client.evaluate(input(" >>> ")))

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

