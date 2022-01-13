#!/bin/bash
./node_modules/.bin/browserify index.js -t @techteamer/browserify-protbuf -s converter > client.js
