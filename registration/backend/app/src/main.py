import http.server
from time import time

PORT = 80


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        response = f"The time is {time()}.\nYour IP is {self.client_address}.You requesteed '{self.path}'"
        self.send_response(200)
        self.end_headers()
        self.wfile.write(response.encode('utf8'))


with http.server.HTTPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
