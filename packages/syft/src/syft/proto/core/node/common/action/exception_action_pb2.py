# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/core/node/common/action/exception_action.proto
"""Generated protocol buffer code."""
# third party
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


# syft absolute
from syft.proto.core.common import (
    common_object_pb2 as proto_dot_core_dot_common_dot_common__object__pb2,
)
from syft.proto.core.io import address_pb2 as proto_dot_core_dot_io_dot_address__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n4proto/core/node/common/action/exception_action.proto\x12\x1dsyft.core.node.common.service\x1a%proto/core/common/common_object.proto\x1a\x1bproto/core/io/address.proto"\xc9\x01\n\x10\x45xceptionMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x37\n\x18msg_id_causing_exception\x18\x03 \x01(\x0b\x32\x15.syft.core.common.UID\x12\x16\n\x0e\x65xception_type\x18\x04 \x01(\t\x12\x15\n\rexception_msg\x18\x05 \x01(\tb\x06proto3'
)


_EXCEPTIONMESSAGE = DESCRIPTOR.message_types_by_name["ExceptionMessage"]
ExceptionMessage = _reflection.GeneratedProtocolMessageType(
    "ExceptionMessage",
    (_message.Message,),
    {
        "DESCRIPTOR": _EXCEPTIONMESSAGE,
        "__module__": "proto.core.node.common.action.exception_action_pb2"
        # @@protoc_insertion_point(class_scope:syft.core.node.common.service.ExceptionMessage)
    },
)
_sym_db.RegisterMessage(ExceptionMessage)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _EXCEPTIONMESSAGE._serialized_start = 156
    _EXCEPTIONMESSAGE._serialized_end = 357
# @@protoc_insertion_point(module_scope)
