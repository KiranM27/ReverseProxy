#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler,HTTPServer
import requests
from socketserver import ThreadingMixIn
from constants import DESTINATION_DOMAIN, REVERSE_PROXY_HOST, REVERSE_PROXY_PORT

def merge_two_dicts(x, y):
    x.update(y)
    return x

def set_header():
    headers = {
        'Host': DESTINATION_DOMAIN
    }

    return headers

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'
    def do_HEAD(self):
        self.do_GET(body=False)
        return
        
    def do_GET(self, body=True):
        sent = False
        try:
            url = 'https://{}{}'.format(DESTINATION_DOMAIN, self.path)
            req_header = self.parse_headers()

            print("*" * 30)
            print("Request has been received and will be forwarded as ", url)
            merged_headers = merge_two_dicts(req_header, set_header())
            print("Request Headers - Request to Backend  - ", merged_headers)
            resp = requests.get(url, headers=merged_headers, verify=False)
            sent = True

            self.send_response(resp.status_code)
            self.send_resp_headers(resp)
            msg = resp.text
            if body:
                self.wfile.write(msg.encode(encoding='UTF-8',errors='strict'))
            return
        finally:
            if not sent:
                self.send_error(404, 'error trying to proxy')

    def do_POST(self, body=True):
        sent = False
        try:
            url = 'https://{}{}'.format(DESTINATION_DOMAIN, self.path)
            content_len = int(self.headers.getheader('content-length', 0))
            post_body = self.rfile.read(content_len)
            req_header = self.parse_headers()

            resp = requests.post(url, data=post_body, headers=merge_two_dicts(req_header, set_header()), verify=False)
            sent = True

            self.send_response(resp.status_code)
            self.send_resp_headers(resp)
            if body:
                self.wfile.write(resp.content)
            return
        finally:
            if not sent:
                self.send_error(404, 'error trying to proxy')

    def parse_headers(self):
        req_header = {}
        for line in self.headers:
            line_parts = [o.strip() for o in line.split(':', 1)]
            if len(line_parts) == 2:
                req_header[line_parts[0]] = line_parts[1]
        return req_header

    def add_cors_to_headers(self, headers):
        headers["Access-Control-Allow-Origin"] = "*"
        headers["Access-Control-Allow-Methods"] = "*"
        headers["Access-Control-Allow-Headers"] = "*"
        headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        return headers

    def send_resp_headers(self, resp):
        respheaders = resp.headers
        respheaders = self.add_cors_to_headers(respheaders)
        print ('Response Headers - Response to Origin - ', respheaders)
        for key in respheaders:
            if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding', 'content-length', 'Content-Length']:
                self.send_header(key, respheaders[key])
        self.send_header('Content-Length', len(resp.content))
        self.end_headers()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def main():
    global hostname
    hostname = DESTINATION_DOMAIN
    server_address = (REVERSE_PROXY_HOST, REVERSE_PROXY_PORT)
    httpd = ThreadedHTTPServer(server_address, ProxyHTTPRequestHandler)
    print(f'Reverse proxy running on {server_address}')
    print(f"Reverse proxy will forward requests to {hostname}")
    httpd.serve_forever()

if __name__ == '__main__':
    main()