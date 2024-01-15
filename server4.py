from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        if 'redirect' in query_params:
            redirect_type = query_params['redirect'][0]
            if redirect_type in ['301', '302']:
                destination = 'http://aqfer.com'
                self.send_response(int(redirect_type))
                self.send_header('Location', destination)
                self.end_headers()
            else:
                self.send_response(400)  # Bad Request for invalid redirect type
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(bytes("Invalid redirect type", "utf-8"))
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes("1","utf-8"))
            
if __name__ == '__main__':
    port = 9090
    server_address = ('', port)

    try:
        httpd = HTTPServer(server_address, MyHandler)
        print(f"Server running on port {port}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
