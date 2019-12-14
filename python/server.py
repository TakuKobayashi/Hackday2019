# coding:utf-8

from flask import Flask, render_template, request, jsonify, send_file
import uuid
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import json
import smtplib

import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
  return render_template('index.html', title='input words page')

@app.route('/pipe')
def pipe():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']

        while True:
            message = ws.receive()
            if message is None:
                break
            print(message)
            ws.send(json.dumps({message: message}))

if __name__ == "__main__":
  app.debug = True
  app.host = '0.0.0.0'
  app.threaded = True
  server = pywsgi.WSGIServer(("", 5000), app, handler_class=WebSocketHandler)
  server.serve_forever()