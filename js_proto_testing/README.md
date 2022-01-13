# Syft JS Client Prototype

## Setup

Do everything in the js_proto_testing folder
```
$ cd js_proto_testing
```

Create a virtualenv and activate
```
$ python3 -m venv ./.venv
$ source ./.venv/bin/activate
```

Install Python dependencies
```
$ pip install -r requirements.txt
```

Initialize Node project
```
$ npm install
```

## Building Browser JS

Run the browserify script
```
$ ./browser.sh
```

## Python Server
Run the python server with
```
./server.sh
```

## Open the web page
[Syft JS Client Sandbox](http://127.0.0.1:5001/js)
