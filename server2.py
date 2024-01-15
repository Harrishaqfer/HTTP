from http.server import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/version':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes("1","utf-8"))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()


if __name__ == '__main__':
    port = 9090
    server_address = ('', port)

    try:
        httpd = HTTPServer(server_address, MyHandler)
        print(f"Server running on port {port}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

