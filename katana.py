#! /usr/bin/env python3
from inputs import get_gamepad
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from math import atan2, degrees, hypot, copysign

poll_values = { 'joystick/L/X' : 0
              , 'joystick/L/Y' : 0
              , 'joystick/R/X' : 0
              , 'joystick/R/Y' : 0
              , 'angle/L' : 90
              , 'angle/R' : 90
              }

buttonMap = { 'KEY_E'          : 'button/\u25B2'
            , 'KEY_D'          : 'button/\u25BC'
            , 'KEY_S'          : 'button/\u25C0'
            , 'KEY_F'          : 'button/\u25B6'
            , 'KEY_K'          : 'button/\u2A2F'
            , 'KEY_L'          : 'button/\u25CB'
            , 'KEY_I'          : 'button/\u25B3'
            , 'KEY_J'          : 'button/\u25A1'
            , 'KEY_R'          : 'button/L1'
            , 'KEY_T'          : 'button/L2'
            , 'KEY_G'          : 'button/L3'
            , 'KEY_U'          : 'button/R1'
            , 'KEY_Y'          : 'button/R2'
            , 'KEY_H'          : 'button/R3'
            , 'KEY_V'          : 'joystick/L/X'
            , 'KEY_N'          : 'joystick/R/X'
            , 'KEY_C'          : 'button/\u25AC'
            , 'KEY_COMMA'      : 'button/\u25BA'
            , 'BTN_DPAD_UP'    : 'button/\u25B2'
            , 'BTN_DPAD_DOWN'  : 'button/\u25BC'
            , 'BTN_DPAD_LEFT'  : 'button/\u25C0'
            , 'BTN_DPAD_RIGHT' : 'button/\u25B6'
            , 'BTN_SOUTH'      : 'button/\u2A2F'
            , 'BTN_EAST'       : 'button/\u25CB'
            , 'BTN_NORTH'      : 'button/\u25B3'
            , 'BTN_WEST'       : 'button/\u25A1'
            , 'BTN_TL'         : 'button/L1'
            , 'BTN_TL2'        : 'button/L2'
            , 'BTN_THUMBL'     : 'button/L3'
            , 'BTN_TR'         : 'button/R1'
            , 'BTN_TR2'        : 'button/R2'
            , 'BTN_THUMBR'     : 'button/R3'
            , 'ABS_X'          : 'joystick/L/X'
            , 'ABS_Y'          : 'joystick/L/Y'
            , 'ABS_RX'         : 'joystick/R/X'
            , 'ABS_RY'         : 'joystick/R/Y'
            , 'BTN_SELECT'     : 'button/\u25AC'
            , 'BTN_START'      : 'button/\u25BA'
            , 'BTN_MODE'       : 'analog'
            }

def joystick(stick):
    return stick[9]

def magnitude(key_x, key_y):
    return hypot(poll_values[key_x], poll_values[key_y])

def deadzone(stick, val):
    dz = 13
    mag = abs(val)
    if mag <= dz:
        stickX = 'joystick/{0}/X'.format(joystick(stick))
        stickY = 'joystick/{0}/Y'.format(joystick(stick))
        if magnitude(stickX, stickY) <= dz:
            poll_values[stickX] = 0
            poll_values[stickY] = 0
        return 0
    else:
        return round(copysign(100 * (mag - dz)/(127.5 - dz), val))

def compass(stick):
    if 'L' in stick:
        x = poll_values['joystick/L/X']
        y = poll_values['joystick/L/Y']
    else:
        x = poll_values['joystick/R/X']
        y = poll_values['joystick/R/Y']
    if x == 0 and y == 0:
        if 'L' in stick:
            compass = poll_values['angle/L']
        else:
            compass = poll_values['angle/R']
    else:
        compass = round(180 - degrees(atan2(y,x)))
    return compass

def kathread():
    global poll_values
    while True:
        es = get_gamepad()
        for e in es:
            if e.ev_type == 'Key':
                poll_values[buttonMap[e.code]] = ['false', 'true', 'true'
                                                 ][ e.state]
            elif e.ev_type == 'Absolute':
                if 'Y' in e.code:
                    e.state = 128 - e.state
                else:
                    e.state = e.state - 127
                poll_values[buttonMap[e.code]] = deadzone(buttonMap[e.code],
                    e.state)
                poll_values['angle/'+joystick(buttonMap[e.code])] = compass(
                    buttonMap[e.code])

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
