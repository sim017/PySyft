import fetch from "node-fetch";
import protobuf from "protobufjs";

const API_URL = "http://127.0.0.1:5001";

// get protobuf definition
const root = await protobuf.load("./proto/tensor.proto");
var tensor_pb = root.lookupType("syft.Tensor");
console.log("Tensor PB", tensor_pb);

// get protobuf message bytes from server
const response = await fetch(`${API_URL}/rcv`);
const bytes = await response.arrayBuffer();
const data = new Uint8Array(bytes);
console.log("Bytes", bytes, "Data", data);

// decode into Tensor object
var tensor = tensor_pb.decode(data);
console.log("Tensor", tensor);

// change data
tensor.tagName = "y";
tensor.bad = "no";

console.log("final output", tensor);
// Encode a message to an Uint8Array (browser) or Buffer (node)
var buffer = tensor_pb.encode(tensor).finish();
console.log("output", buffer);
// ... do something with buffer

const response2 = await fetch(`${API_URL}/send`, {
  method: "POST",
  headers: {"content-type": "application/octect-stream"},
  body: buffer,
});
