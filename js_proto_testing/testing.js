import fetch from "node-fetch"
import protobuf from "protobufjs"

const root = await protobuf.load("./proto/tensor.proto")


// // Obtain a message type
var tensor_pb = root.lookupType("syft.Tensor");
console.log("Loading", tensor_pb)


console.log("Outside", tensor)
const response = await fetch("http://localhost:5000/rcv") 
const bytes =  await response.arrayBuffer()
const data = new Uint8Array(bytes)
console.log("Bytes", bytes, "Data", data)
var tensor = tensor_pb.decode(data)
console.log("Tensor", tensor)
