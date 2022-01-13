from flask import Flask
from flask import request
from flask import Response
from python_proto.tensor_pb2 import Tensor as Tensor_PB

app = Flask(__name__)

def make_tensor(tag, dtype):
    return Tensor_PB(tag_name=tag, public_dtype=dtype)

@app.route("/rcv")
def message():
    x = make_tensor("x", "np.int32")
    print(type(x))
    blob = x.SerializeToString()
    print(blob)
    headers = {"content-type": "application/octect-stream"}
    return blob, 200, headers

@app.route("/send", methods=["POST"])
def rcv_message():
    body = request.get_data()
    print(body)
    print(type(body))
    return "Echo"
