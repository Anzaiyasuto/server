from flask import Flask, request, render_template
from websocket_server import WebsocketServer
import logging
import math
app = Flask(__name__)
file_path = "./sensor_data.csv"
port_num = 18011
state = ""

@app.route('/', methods=['GET'])
def get_html():
    return render_template('./index.html')

@app.route('/lux', methods=['POST'])
def update_lux():
    flag = ['vacant', 'occupied'] #flag = 0 -> vacant | flag = 1 -> occupied 
    time = request.form["time"]
    lux = request.form["lux"]
    #print(type(lux))
    
    lux = float(lux)

    alpha = None
    beta = None
    theta = None #str lux
    delta = None #occupied or vacant
    ganma = None #float lux
    temp = None
    try:
        f = open(file_path, 'r')
        for row in f:
            alpha = row
        beta = alpha.split(',')
        theta = float(beta[1])
        delta = beta[2]

    except Exception as e:
        print(e)
    finally:
        f.close()
    #print(type(alpha))
    #print(type(beta))
    #print(type(theta))
    #print(type(delta))
    #print("debug")
    if(abs(lux-theta) < 150):
        temp = delta
    else:
        if(delta == flag[0]):
            temp = flag[1]
        else:
            temp = flag[0]    

    try:
        f = open(file_path, 'w')
        f.write(time + "," + str(lux) + "," + temp)
        return "succeeded to write"
    except Exception as e:
        print(e)
        return "failed to write"
    finally:
        f.close()

@app.route('/lux', methods=['GET'])
def get_lux():
    try:
        f = open(file_path, 'r')
        for row in f:
            lux = row
    except Exception as e:
        print(e)
    finally:
        f.close()
        return lux

#@app.route('/remind', methods=["POST"])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = port_num)

"""

class Websocket_Server():

    def __init__(self, host, port):
        self.server = WebsocketServer(port, host=host, loglevel=logging.DEBUG)

    # クライアント接続時に呼ばれる関数
    def new_client(self, client, server):
        print("new client connected and was given id {}".format(client['id']))
        # 全クライアントにメッセージを送信
        self.server.send_message_to_all("hurry up!!!")

    # クライアント切断時に呼ばれる関数
    def client_left(self, client, server):
        print("client({}) disconnected".format(client['id']))

    # クライアントからメッセージを受信したときに呼ばれる関数
    def message_received(self, client, server, message):
        print("client({}) said: {}".format(client['id'], message))
        # 全クライアントにメッセージを送信
        self.server.send_message_to_all(message)
    
    # サーバーを起動する
    def run(self):
        # クライアント接続時のコールバック関数にself.new_client関数をセット
        self.server.set_fn_new_client(self.new_client)
        # クライアント切断時のコールバック関数にself.client_left関数をセット
        self.server.set_fn_client_left(self.client_left)
    # メッセージ受信時のコールバック関数にself.message_received関数をセット
        self.server.set_fn_message_received(self.message_received) 
        self.server.run_forever()

IP_ADDR = "192.168.0.8" # IPアドレスを指定
PORT=9001 # ポートを指定
ws_server = Websocket_Server(IP_ADDR, PORT)
ws_server.run()

"""

