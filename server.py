import json
import http.server
import urllib.parse

from socketserver import ThreadingMixIn
import _thread

import analysis

log_in = ('MjEwMTY1ODc6MjEwMTY1ODc=')


def gobble_file(filename, mode='r'):
    with open(filename, mode) as fin:
        content = fin.read()
    return content


class MyHandler(http.server.BaseHTTPRequestHandler):

    # Override to handle GET requests
    def do_GET(self):
        filename = self.path.strip('/')
        print('GET:', filename, _thread.get_native_id())

        print(self.headers)

        if 'Authorization' in self.headers:
            authstr = self.headers['Authorization'].split()[-1]
            if authstr == log_in:
                print('correct')
                self.send_response(200)
            else:
                self.send_response(401)
                self.send_header('WWW-Authenticate', 'Basic realm="159352"')
                self.end_headers()
        else:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="159352"')
            self.end_headers()

        if self.path == '/':
            self.send_header('Content-type', 'text/html')
            content = gobble_file('index.html').encode()

        elif self.path == '/form':
            self.send_header('Content-type', 'text/html')
            content = gobble_file('psycho.html').encode()

        elif self.path == '/view/input':
            self.send_header('Content-type', 'application/json')
            content = gobble_file('data/input.json').encode()

        elif self.path == '/view/profile':
            self.send_header('Content-type', 'application/json')
            content = gobble_file('data/profile.json').encode()

        elif filename.endswith('.jpg'):
            self.send_header('Content-type', 'image/jpeg')
            content = gobble_file(filename, mode='rb')

        elif filename.endswith('.ico'):
            self.send_header('Content-type', 'image/x-icon')
            content = gobble_file(filename, mode='rb')

        elif filename.endswith('.js'):
            self.send_header('Content-type', 'text/javascript')
            content = gobble_file(filename, mode='rb')

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            content = json.dumps(
                {'status': 404, 'path': filename, 'message': 'Resource not recognized'}
            ).encode()

        self.end_headers()
        self.wfile.write(content)

    # Override to handle POST requests
    def do_POST(self):
        # Extract the raw POST string from the request body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print('POST:', post_data, _thread.get_native_id())

        pdata = urllib.parse.parse_qs(post_data.decode())

        analysis.process_pdata(pdata)

        # Finally, send the response packet
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        content = json.dumps(
            {'http-status': 'ok'}
        )
        # Here is a very basic response
        self.wfile.write(content.encode())


class ThreadedHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    """Handle requests in a separate thread."""


def main(port):
    # Threaded http server instance

    webServer = ThreadedHTTPServer(('', port), MyHandler)
    webServer.serve_forever()


if __name__ == '__main__':
    port = 8080
    main(port)
