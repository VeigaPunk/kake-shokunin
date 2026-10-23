import http.server,sys
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        m={'/f':'file:///etc/hostname','/v':'http://[','/ok':None}
        loc=m.get(self.path)
        if loc: self.send_response(301); self.send_header('Location',loc); self.end_headers()
        else: self.send_response(200); self.send_header('Content-Type','text/plain'); self.end_headers(); self.wfile.write(b'hello world')
    def log_message(self,*a): pass
http.server.HTTPServer(('127.0.0.1',int(sys.argv[1])),H).serve_forever()
