# third party
from flask import Flask
from flask import request
from flask import send_from_directory
from python_proto.tensor_pb2 import Tensor as Tensor_PB

app = Flask(__name__)


def make_tensor(tag, dtype):
    return Tensor_PB(tag_name=tag, public_dtype=dtype)


@app.route("/rcv")
def message():
    print("RECIEVE")
    x = make_tensor("x", "np.int32")
    print(type(x))
    blob = x.SerializeToString()
    print(blob)
    headers = {"content-type": "application/octect-stream"}
    return blob, 200, headers


@app.route("/send", methods=["POST"])
def rcv_message():
    print("SEND")
    print(request.headers)
    body = request.get_data()
    print("data", body)
    print("type", type(body))
    tensor = Tensor_PB()
    print("Tensor_PB", tensor, type(tensor))
    tensor.ParseFromString(body)
    print("type", tensor)
    print("tensor", tensor)
    return "Echo"


@app.route("/js")
def index_js():
    return send_from_directory("./", "index.html")


@app.route("/client.js")
def client_js():
    return send_from_directory("./", "client.js")


# @app.route("/tensor_pb.js")
# def tensor_js():
#     return send_from_directory("./js_proto", "tensor_pb.js")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
