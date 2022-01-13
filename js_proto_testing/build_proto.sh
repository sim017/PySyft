#!/bin/bash
# protoc --proto_path=proto --js_out=library=syft,binary:js_proto/ proto/*
mkdir -p js_proto python_proto
protoc --proto_path=proto --js_out=import_style=commonjs,binary:js_proto/ proto/*
protoc --proto_path=proto --python_out=python_proto proto/*
