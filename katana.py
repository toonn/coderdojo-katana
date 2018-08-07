#! /usr/bin/env python3
from inputs import get_key
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import random

poll_values = {}

buttonMap = { 'KEY_E'     : 'button/\u25B2'
            , 'KEY_D'     : 'button/\u25BC'
            , 'KEY_S'     : 'button/\u25C0'
            , 'KEY_F'     : 'button/\u25B6'
            , 'KEY_K'     : 'button/\u2A2F'
            , 'KEY_L'     : 'button/\u25CB'
            , 'KEY_I'     : 'button/\u25B3'
            , 'KEY_J'     : 'button/\u25A1'
            , 'KEY_R'     : 'button/L1'
            , 'KEY_T'     : 'button/L2'
            , 'KEY_G'     : 'button/L3'
            , 'KEY_U'     : 'button/R1'
            , 'KEY_Y'     : 'button/R2'
            , 'KEY_H'     : 'button/R3'
            , 'KEY_V'     : 'joystick/L/X'
            , 'KEY_N'     : 'joystick/R/X'
            , 'KEY_C'     : 'button/\u25AC'
            , 'KEY_COMMA' : 'button/\u25BA'
            }

def kathread():
    global poll_values
    while True:
        es = get_key()
        for e in es:
            if e.ev_type == 'Key':
                poll_values[buttonMap[e.code]] = ['false','true','true'][e.state]

class KatanaHandler(BaseHTTPRequestHandler):
    
    def format_response(self, values=[]):
        response = ["{s} {v}".format(s=sensor, v=value) for (sensor,
                    value) in values]
        return "\n".join(response)

    def do_GET(self):
        global poll_values
        print(poll_values)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if self.path == '/poll':
            self.wfile.write("{poll}".format(
                             poll=self.format_response(poll_values.items())
                             ).encode('utf-8'))
        elif self.path == '/reset_all':
            pass
        elif self.path.startswith('/rumble/'):
            self.wfile.write(("<html><body>_problem Path <b>{path}</b>"
                              " requested but rumble not implemented."
                              "</body></html>"
                             ).format(path=self.path).encode('utf-8'))
            pass # rumble for int(self.path[8:]) seconds
        elif self.path == '/crossdomain.xml':
            self.wfile.write(('<cross-domain-policy>'
                              '<allow-access-from domain=="*"'
                              ' to-ports="31337"/>'
                              '</cross-domain-policy>\0').encode('utf-8'))
        else:
            self.wfile.write(("<html><body>_problem Path <b>{path}</b>"
                              " requested but not implemented.</body></html>"
                             ).format(path=self.path).encode('utf-8'))

with HTTPServer(('', 31337), KatanaHandler) as httpd:
    Thread(target=kathread).start()
    httpd.serve_forever()
