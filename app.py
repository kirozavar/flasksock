from flask import Flask, render_template
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

@app.route('/')
def index():
    return "testtttt"

@app.route('/test2')
def test():
    return "testtttt"

@sock.route('/echo')
def echo(ws):
    while True:
        data = ws.receive()
        print(f"Received message: {data}")
        ws.send(f"Echo: {data}")

if __name__ == "__main__":
    app.run(debug=True)
