import requests
import json
import cgi
import os
import sys

def get_ip():
    try:
        return "localhost"
#        return cgi.escape(os.environ["REMOTE_ADDR"])
    except:
        return "127.0.0.1"


def verify(token):
    ip = get_ip()
    if ip == '127.0.0.1' or ip == 'localhost':
        return True
    url = 'https://www.google.com/recaptcha/api/siteverify'
    data = {
        'secret': '6LchHMIUAAAAAEo-cR1-LOif8D4Cg4_SgwJk09YS',
        'response': token,
        'remoteip': ip
    }
    req = requests.post(url=url, data=data)
    data = json.loads(req.text)
    if ('success' not in data) or ('score' not in data):
        return False
    if not data['success']:
        return False
    return data['score'] > 0.5
