const root = require('./proto/tensor.proto')
const tensor_pb = root.lookupType('syft.Tensor')
console.log("tensor_pb", tensor_pb)

const API_URL = "http://127.0.0.1:5001"

async function run() {
    // get protobuf message bytes from server
    const response = await fetch(`${API_URL}/rcv`)
    const bytes = await response.arrayBuffer()
    const data = new Uint8Array(bytes)
    console.log("Bytes", bytes, "Data", data)

    // decode into Tensor object
    var tensor = tensor_pb.decode(data)
    console.log("Tensor", tensor)

    // change data
    tensor.tagName = "y"
    tensor.bad = "no"

    console.log("final output", tensor)
    // Encode a message to an Uint8Array (browser) or Buffer (node)
    var buffer = tensor_pb.encode(tensor).finish()
    console.log("output", buffer)

    const response2 = await fetch(`${API_URL}/send`, {
        method: "POST",
        headers: {"content-type": "application/octect-stream"},
        body: buffer,
    })
    console.log("finished posting", response2)

}
run()
