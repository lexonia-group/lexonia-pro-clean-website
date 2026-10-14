"""Serve site/ on localhost applying the headers from netlify.toml, to test the site under the real security headers."""
import http.server, socketserver, tomllib, sys, os, fnmatch
cfg=tomllib.load(open('netlify.toml','rb'))
ROOT=sys.argv[1]; PORT=int(sys.argv[2])
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s,*a,**k): super().__init__(*a,directory=ROOT,**k)
    def log_message(s,*a): pass
    def end_headers(s):
        p=s.path.split('?')[0]
        for h in cfg['headers']:
            pat=h['for']
            if pat=='/*' or fnmatch.fnmatch(p,pat):
                for k,v in h['headers' if False else 'values'].items():
                    if k=='Strict-Transport-Security': continue   # http on localhost
                    if k=='Content-Security-Policy': v=v.replace('; upgrade-insecure-requests','')
                    s.send_header(k,v)
        super().end_headers()
    def do_POST(s):
        # emulate Netlify: accept the form post and answer with the thanks page
        n=int(s.headers.get('Content-Length',0)); s.rfile.read(n)
        s.path='/thanks.html'; self_get=super().do_GET; self_get()
socketserver.TCPServer.allow_reuse_address=True
socketserver.ThreadingTCPServer(('127.0.0.1',PORT),H).serve_forever()
