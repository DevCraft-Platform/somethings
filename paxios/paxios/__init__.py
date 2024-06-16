#   , __    ___,    _          _    __
#  /|/  \  /   |   (_\  /     | |  /\_\/   ()
#   |___/ |    |      \/      | | |    |   /\
#   |     |    |      /\    _ |/  |    |  /  \
#   |      \__/\_/  _/  \_/ \_/\/  \__/  /(__/
#   ==========================================
#   A supercharged version of the requests module, with more features and better performance.

#   _sumary_:
# 	Paxios permits you tu create in a super fast and easy ways a full API for your web application.

#   _author_: INovomiast2 (Ivan Novomiast)
#   _version_: 1.0.0
#   _license_: MIT
#   _github_: https://github.com/INovomiast2/paxios

# Here is all the code of paxios, this is going to be a long file, so be prepared.

import time
import subprocess
import sys
import ssl
import threading
import json
from typing import Dict, Any, List, Type
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from http.server import HTTPServer, BaseHTTPRequestHandler

class _ReloadHandler(FileSystemEventHandler):
    def __init__(self, server_instance, start_server):
        self.server_instance = server_instance
        self.start_server = start_server
        self.last_restart = time.time()

    def on_modified(self, event):
        if event.src_path.endswith('.py') and (time.time() - self.last_restart > 2):
            self.server_instance._stop()
            self.server_instance.join()
            self.server_instance = self.start_server()
            self.last_restart = time.time()

class CreatePaxios:
    """
    To use paxios, you MUST create an instance of this class.
    With this class you can create a full API for your web application.
    """

    def __init__(self, host: str = 'localhost', port: int = 3000, debug: bool = False, version: int = 0, ssl: bool = False, ssl_key: str = None, ssl_cert: str = None, auth: bool = True, auth_token: str = None) -> None:
        self.host = host
        self.port = port
        self.debug = debug
        self.version = version
        self.ssl = ssl
        self.ssl_key = ssl_key
        self.ssl_cert = ssl_cert
        self.auth = auth
        self.auth_token = auth_token
        self.routes = {}
        self.middlewares = []

        @self.endpoint('/', methods=['GET'])
        def index():
            return self.json({'message': 'Welcome to Paxios!'})

        @self.endpoint('/version', methods=['GET'])
        def api_version():
            return self.json({'version': self.version})

        @self.endpoint('/servinfo', methods=['GET'])
        def server_info():
            return self.json({
                'host': self.host,
                'port': self.port,
                'ssl': 'enabled' if self.ssl else 'disabled',
                'auth': 'enabled' if self.auth else 'disabled',
                'paxios_version': '1.0.0',
                'debug': 'enabled' if self.debug else 'disabled'
            })

    class CustomHTTPServer(HTTPServer):
        def __init__(self, server_address, RequestHandlerClass, routes, bind_and_activate=True):
            super().__init__(server_address, RequestHandlerClass, bind_and_activate)
            self.routes = routes

    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            route = self.server.routes.get(self.path)
            if route is not None and 'GET' in route:
                response = route['GET']()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response.encode())
            else:
                response = json.dumps({'message': 'Route not found'})
                self.send_response(404)
                self.end_headers()
                self.wfile.write(response.encode())

        def do_POST(self):
            route = self.server.routes.get(self.path)
            if route is not None and 'POST' in route:
                response = route['POST']()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response.encode())
            else:
                response = json.dumps({'message': 'Route not found'})
                self.send_response(404)
                self.end_headers()
                self.wfile.write(response.encode())

        def do_PUT(self):
            route = self.server.routes.get(self.path)
            if route is not None and 'PUT' in route:
                response = route['PUT']()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response.encode())
            else:
                response = json.dumps({'message': 'Route not found'})
                self.send_response(404)
                self.end_headers()
                self.wfile.write(response.encode())

    def endpoint(self, path: str, methods: List[str]):
        def decorator(f):
            versioned_path = f"/v{self.version}{path}"
            if versioned_path not in self.routes:
                self.routes[versioned_path] = {}
            for method in methods:
                if method in self.routes[versioned_path]:
                    raise ValueError(f"La ruta {versioned_path} ya está definida para el método {method}.")
                self.routes[versioned_path][method] = f
            return f
        return decorator

    def start_server(self):
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.stop_flag = threading.Event()
        self.server_thread.start()
        return self.server_thread

    def run_server(self):
        if self.ssl:
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile=self.ssl_cert, keyfile=self.ssl_key)
            server = self.CustomHTTPServer((self.host, self.port), self.RequestHandler, self.routes)
            server.socket = context.wrap_socket(server.socket, server_side=True)
        else:
            server = self.CustomHTTPServer((self.host, self.port), self.RequestHandler, self.routes)

        print(f"API running at http://{self.host}:{self.port}/v{self.version}/")
        while not threading.current_thread().stop_flag.is_set():
            server.handle_request()

    def run(self) -> None:
        """
        Runs the API.
        """
        if not self.routes:
            raise ValueError("No routes defined.")

        if self.debug:
            print(self.list_endpoints())
            server_thread = self.start_server()

            observer = Observer()
            event_handler = _ReloadHandler(server_thread, self.start_server)
            observer.schedule(event_handler, ".", recursive=False)
            observer.start()

            try:
                while server_thread.is_alive():
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
            finally:
                observer.stop()
                observer.join()
                server_thread.stop_flag.set()
                server_thread.join()
        else:
            self.run_server()

    def json(self, data: Dict[str, Any]) -> str:
        """
        Devuelve un objeto JSON.

        Args:
            data (Dict[str, Any]): The data to convert to JSON.
        """
        return json.dumps(data)

    def list_endpoints(self):
        route_names = {path: {method: func.__name__ for method, func in funcs.items()} for path, funcs in self.routes.items()}
        return route_names

    def use(self, middleware: Type['Middleware']) -> 'Middleware':
        if not issubclass(middleware, Middleware):
            raise ValueError("{} is not a valid middleware.".format(middleware))
        instance = middleware()
        self.middlewares.append(instance)
        return instance

class fromFile:
	def __init__(self, file: str = None) -> None:
		self.file = file
		self.data = None

	def read(self) -> dict:
		"""
		Read a JSON file and return it as a dictionary.
		"""
		# Protecting the function from errors
		try:
			# Opening the file
			with open(self.file, "r") as f:
				# Reading the file
				self.data = json.load(f)
			# Returning the data
			return self.data
		except Exception as e:
			# If an error occurs, return the error
			return e

	def write(self, data: dict) -> None:
		"""
		Write a dictionary to a JSON file.
		"""
		# Protecting the function from errors
		try:
			# Opening the file
			with open(self.file, "w") as f:
				# Writing the data
				json.dump(data, f)
		except Exception as e:
			# If an error occurs, return the error
			return e