#!/usr/bin/env python

import shelve
import sys
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import urllib2
import re
import traceback


def serve(port, file_):
    try:
        shelf = shelve.open(file_, "r")

        class HTTPRequestHandler(BaseHTTPRequestHandler):
            
            def do_GET(self):
                try:
                    path = urllib2.unquote(self.path);
                    path = path.replace("+", " ");
                    path_m = re.search(r'(?:http://[^/]*/+(.*)|/*(.*))', path);
                    if path_m:
                        name_ = path_m.group(1) or path_m.group(2)
                        content = shelf[name_]
                        self.send_response(200)
                        self.send_header("Content-Type", "text/plain; charset=UTF-8");
                        self.end_headers();
                        self.wfile.write(content.encode("UTF-8"))
                except:
                    self.send_response(404)
                    self.send_header("Content-Type", "text/plain");
                    self.end_headers();
                    (a,b,t) = sys.exc_info()
                    self.wfile.write("".join(traceback.format_exception(a,b,t)))

        httpd = HTTPServer(("0.0.0.0", port), HTTPRequestHandler);
        httpd.allow_reuse_address = True;
        httpd.serve_forever();

    except KeyboardInterrupt:
        httpd.socket.close();
        sys.exit(0);


if __name__ == '__main__':
    if len(sys.argv)<3:
        sys.stderr.write("Usage: shelve_server port file\n")
        sys.exit(1)
    serve(int(sys.argv[1]), sys.argv[2])




