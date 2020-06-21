from http.server import BaseHTTPRequestHandler, HTTPServer
import simple_https
import urllib
import threading
import webbrowser
import requests
import os

CLIENT_ID = 'b2cc1c864bed962e73b9'

CODE = None

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        global CODE
        CODE = params['code'][0]
        self._set_headers()
        self.wfile.write(str.encode(
            "<html><body><h1>Authorization successful</h1><p>Authorization successful, you can close this page.</p></body></html>")
        )

    def do_HEAD(self):
        self._set_headers()

def run_server(server_class=HTTPServer, handler_class=RequestHandler, port=9192):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.handle_request()
    httpd.socket.close()

def obtain_auth_code():
    redirect_uri= "https://localhost/"
    webbrowser.open('https://exist.io/oauth2/authorize?response_type=code&client_id=%s&scope=%s' %
                    (CLIENT_ID, "read+write"))
    # run_server()
    return CODE

def get_oauth_token(code):
    url = 'https://exist.io/oauth2/access_token'
    # client_secret = os.environ['CLIENT_SECRET']
    print("Auth is broken; paste your client secret below")
    CLIENT_SECRET = input()
    response = requests.post(url,
               {'grant_type':'authorization_code',
                'code':code,
                'client_id':CLIENT_ID,
                'client_secret':CLIENT_SECRET})
    return response.json()['access_token']

def token():
    code = obtain_auth_code()
    print("Auth is broken; paste your code below")
    code = input()
    return get_oauth_token(code)
