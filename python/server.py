# coding:utf-8

from flask import Flask, render_template, request, jsonify, send_file, redirect
from flask_cors import CORS

from line_pay import LinePay
import uuid
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import json
from serialio import SerialIO
import csvreader
import atexit

import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

LINE_PAY_URL = 'https://sandbox-api-pay.line.me'
LINE_PAY_CHANNEL_ID = os.environ.get("LINE_PAY_CHANNEL_ID")
LINE_PAY_CHANNEL_SECRET = os.environ.get("LINE_PAY_CHANNEL_SECRET_KEY")
LINE_PAY_CONFIRM_URL = os.environ.get("NGROK_ROOT_URL") + '/pay/confirm'
pay = LinePay(channel_id=LINE_PAY_CHANNEL_ID, channel_secret=LINE_PAY_CHANNEL_SECRET,
              line_pay_url=LINE_PAY_URL, confirm_url=LINE_PAY_CONFIRM_URL)

serialio = SerialIO()

app = Flask(__name__, static_folder="./templates/products/static", template_folder="./templates")
CORS(app)

ws_list = set()

@app.route("/", methods=["GET"])
def index():
  return render_template('products/index.html')

@app.route("/api/mst/products", methods=["GET"])
def mst_products():
    return jsonify(csvreader.loadMasterData())

@app.route("/videochat", methods=["GET"])
def videochat():
    return render_template('videochat.html')

@app.route("/payment", methods=['GET'])
def payment():
    return render_template('payment.html')

# 進むコマンド
@app.route("/serial", methods=['GET'])
def serial():
    command = request.args.get('command')
    print(command)
    send_result = serialio.send(command + "\n")
    return jsonify({"status": send_result})

@app.route("/commander", methods=['GET'])
def commander():
    return render_template('commander.html')

@app.route("/images/mst/<path:path>")
def products_images(path):
    fullpath = "./images/mst/" + path
    return send_file(fullpath, mimetype='image/png')

@app.route('/pay/product/<string:product_id>', methods=['GET'])
def pay_product(product_id):
    mst_dics_list = csvreader.loadMasterData()
    product = None
    for mst_product in mst_dics_list:
        print(mst_product)
        if mst_product["id"] == product_id:
            product = mst_product
            break
    if product is None:
        return "NG"

    (order_id, response) = pay.request_payments(
        product_name=product["name"],
        amount=product["price"],
        currency=product["currency"],
        product_image_url=product["image_url"],
    )
    transaction_id = response["info"]["transactionId"]
    redirect_url = response["info"]["paymentUrl"]["web"]
    return redirect(redirect_url)

@app.route("/pay/reserve", methods=['POST'])
def pay_reserve():
    mst_dics_list = csvreader.loadMasterData()

    (order_id, response) = pay.request_payments(
        product_name=mst_dics_list[0]["name"],
        amount=mst_dics_list[0]["price"],
        currency=mst_dics_list[0]["currency"],
        product_image_url=mst_dics_list[0]["image_url"],
    )
    print(response["returnCode"])
    print(response["returnMessage"])
    print(response["info"])

    transaction_id = response["info"]["transactionId"]
    print(order_id, transaction_id)
    redirect_url = response["info"]["paymentUrl"]["web"]
    return redirect(redirect_url)


@app.route("/pay/confirm", methods=['GET'])
def pay_confirm():
    transaction_id = request.args.get('transactionId')
    print(transaction_id)
    for s in ws_list:
        try:
            s.send(json.dumps({"action": "payment", "status": "success"}))
        except Exception:
            print("error")
    return "お買い上げありがとうございます!!"

@app.route('/pipe')
def pipe():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        ws_list.add(ws)

        while True:
            message = ws.receive()
            if message is None:
                break
            remove = set()
            for s in ws_list:
                try:
                    s.send(message)
                except Exception:
                    remove.add(s)
            for s in remove:
                ws_list.remove(s)

if __name__ == "__main__":
    # flaskがkillされた時に呼ぶ
    def close_running_threads():
        serialio.close()
    atexit.register(close_running_threads)

    app.debug = True
    app.host = '0.0.0.0'
    app.threaded = True
    server = pywsgi.WSGIServer(("", 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()