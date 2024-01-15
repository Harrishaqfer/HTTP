from http.server import BaseHTTPRequestHandler, HTTPServer
from http import cookies

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/version':
            if self.headers.get('Cookie'):
                cookie=self.headers.get('Cookie')
                cookie=cookies.SimpleCookie(cookie)
                intern=cookie.get('_intern')
                if intern is None:
                    self.send_response(200)
                    self.create()
                else:
                    self.send_response(204)
            else:
                self.send_response(200)
                self.create()
            self.end_headers()
            self.wfile.write(b'1')
        else:
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()

    def create(self):
        cookie=cookies.SimpleCookie()
        cookie['_intern']='JAYA HARRISH'
        cookie['_intern']['path']='/'
        self.send_header('Set-Cookie',cookie.get('_intern').OutputString())
if __name__=="__main__":
    server_address=('127.0.0.1',9090)
    http=HTTPServer(server_address,MyRequestHandler)
    print("Starting Server")
    http.serve_forever()