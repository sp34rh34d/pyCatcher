import readline, argparse, logging, ast, subprocess, atexit, threading
from flask import Flask, Response, request
from core.utilities import msg

class request_catcher():
    def __init__(self,bind_address,bind_port,ssl=False,private_key=None,public_key=None,custom_routes={},serveo=False):
        self.bind_address = bind_address
        self.bind_port = bind_port
        self.enable_ssl = ssl
        self.private_key_file = private_key
        self.public_key_file = public_key
        self.app = Flask(__name__)
        self.setup_routes()
        self.custom_routes = custom_routes
        self.enable_serveo = serveo
        self.serveo_is_running = False
        self.serveo_process = None
        atexit.register(self.cleanup)

    def setup_routes(self):
        @self.app.after_request
        def log_all(response):
            if request.path == '/favicon.ico':
                return response
            request_values = ""
            request_values = msg.newRequest()
            request_values += msg.requestInfo(str(request.method),str(request.remote_addr),str(request.full_path))
            request_values += msg.requestHeaders(request.headers)
            request_values += msg.requestCookies(request.cookies)

            if request.method == 'POST':
                if request.form:
                    request_values += msg.requestPostData(dict(request.form))
                else:
                    data = request.get_data(as_text=True)
                    request_values += msg.requestPostData(data)

            request_values += msg.requestFiles(request.files)
            print(request_values)
            return response


        @self.app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
        @self.app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
        def catch_all(path):
            return f'request caught',200

    def add_custom_routes(self):
        if self.custom_routes.keys():
            msg.info("Adding custom route")
            for route in self.custom_routes:
                path = "/" + self.custom_routes[route]["path"]
                file_path = self.custom_routes[route]["file"]
                headers = self.custom_routes[route].get("headers") or {}

                if isinstance(headers, str):
                    headers = ast.literal_eval(headers)

                def create_new_route(file_path=file_path, extra_headers=headers):

                    def route_func():
                        try:
                            with open(file_path, "rb") as f:
                                data = f.read()
                            resp = Response(data)

                            for k,v in extra_headers.items():
                                resp.headers[k] = v.replace("++"," ")

                            return resp

                        except FileNotFoundError:
                            return Response("File not found", status=404)
                    return route_func

                endpoint_name = f"route_{route}"
                self.app.add_url_rule(path, endpoint_name, create_new_route(), methods=["GET"])
        else:
            msg.info("No custom route yet")

    def start_serveo(self):
        msg.info("Starting Serveo service")
        self.serveo_process = subprocess.Popen(
            ["ssh", "-R", f"80:localhost:{self.bind_port}", "serveo.net"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in self.serveo_process.stdout:
            if "Forwarding HTTP traffic" in line:
                msg.info(line.strip())
                break

    def cleanup(self):
        if self.serveo_is_running:
            msg.info("Stopping Serveo...")
            self.serveo_process.terminate()
            self.serveo_process.wait()

    def run(self):
        try:
            logging.getLogger('werkzeug').disabled = True
            self.add_custom_routes()
            msg.info("Starting monitor mode")
            msg.info("Press CTRL+C to cancel")

            if self.enable_serveo:
                threading.Thread(target=self.start_serveo, daemon=True).start()

            if self.enable_ssl:
                msg.info("SSL context is enable")
                msg.info(f"Listening for requests on https://{self.bind_address}:{self.bind_port}")
                self.app.run(host=self.bind_address, port=self.bind_port,debug=False,ssl_context=(self.public_key_file, self.private_key_file))
            else:
                msg.info(f"Listening for requests on http://{self.bind_address}:{self.bind_port}")
                self.app.run(host=self.bind_address, port=self.bind_port,debug=False)
        except Exception as e:
            msg.error('error:',e)
        finally:
            if self.enable_serveo:
                self.cleanup()
