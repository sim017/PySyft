# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/core/node/common/action/run_function_or_constructor.proto

# third party
from google.protobuf import descriptor as _descriptor
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
from syft.proto.core.pointer import (
    pointer_pb2 as proto_dot_core_dot_pointer_dot_pointer__pb2,
)

DESCRIPTOR = _descriptor.FileDescriptor(
    name="proto/core/node/common/action/run_function_or_constructor.proto",
    package="syft.core.node.common.action",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n?proto/core/node/common/action/run_function_or_constructor.proto\x12\x1csyft.core.node.common.action\x1a%proto/core/common/common_object.proto\x1a proto/core/pointer/pointer.proto\x1a\x1bproto/core/io/address.proto"\x8e\x03\n\x1eRunFunctionOrConstructorAction\x12\x0c\n\x04path\x18\x01 \x01(\t\x12(\n\x04\x61rgs\x18\x02 \x03(\x0b\x32\x1a.syft.core.pointer.Pointer\x12X\n\x06kwargs\x18\x03 \x03(\x0b\x32H.syft.core.node.common.action.RunFunctionOrConstructorAction.KwargsEntry\x12-\n\x0eid_at_location\x18\x04 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x05 \x01(\x0b\x32\x15.syft.core.io.Address\x12%\n\x06msg_id\x18\x06 \x01(\x0b\x32\x15.syft.core.common.UID\x12\x11\n\tis_static\x18\x07 \x01(\x08\x1aI\n\x0bKwargsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12)\n\x05value\x18\x02 \x01(\x0b\x32\x1a.syft.core.pointer.Pointer:\x02\x38\x01\x62\x06proto3',
    dependencies=[
        proto_dot_core_dot_common_dot_common__object__pb2.DESCRIPTOR,
        proto_dot_core_dot_pointer_dot_pointer__pb2.DESCRIPTOR,
        proto_dot_core_dot_io_dot_address__pb2.DESCRIPTOR,
    ],
)


_RUNFUNCTIONORCONSTRUCTORACTION_KWARGSENTRY = _descriptor.Descriptor(
    name="KwargsEntry",
    full_name="syft.core.node.common.action.RunFunctionOrConstructorAction.KwargsEntry",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="key",
            full_name="syft.core.node.common.action.RunFunctionOrConstructorAction.KwargsEntry.key",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="value",
            full_name="syft.core.node.common.action.RunFunctionOrConstructorAction.KwargsEntry.value",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=b"8\001",
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=525,
    serialized_end=598,
)

_RUNFUNCTIONORCONSTRUCTORACTION = _descriptor.Descriptor(
    name="RunFunctionOrConstructorAction",
    full_name="syft.core.node.common.action.RunFunctionOrConstructorAction",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="path",
            full_name="syft.core.node.common.action.RunFunctionOrConstructorAction.path",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="args",
            full_name="syft.core.node.common.action.RunFunctionOrConstructorAction.args",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="kwargs",
            full_name="syft.core.node.common.action.RunFunctionOrConstructorAction.kwargs",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="id_at_location",
            full_name="syft.core.node.common.action.RunFunctionOrConstructorAction.id_at_location",
            index=3,
            number=4,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="address",
            full_name="syft.core.node.common.action.RunFunctionOrConstructorAction.address",
            index=4,
            number=5,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="msg_id",
            full_name="syft.core.node.common.action.RunFunctionOrConstructorAction.msg_id",
            index=5,
            number=6,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="is_static",
            full_name="syft.core.node.common.action.RunFunctionOrConstructorAction.is_static",
            index=6,
            number=7,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[
        _RUNFUNCTIONORCONSTRUCTORACTION_KWARGSENTRY,
    ],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=200,
    serialized_end=598,
)

_RUNFUNCTIONORCONSTRUCTORACTION_KWARGSENTRY.fields_by_name[
    "value"
].message_type = proto_dot_core_dot_pointer_dot_pointer__pb2._POINTER
_RUNFUNCTIONORCONSTRUCTORACTION_KWARGSENTRY.containing_type = (
    _RUNFUNCTIONORCONSTRUCTORACTION
)
_RUNFUNCTIONORCONSTRUCTORACTION.fields_by_name[
    "args"
].message_type = proto_dot_core_dot_pointer_dot_pointer__pb2._POINTER
_RUNFUNCTIONORCONSTRUCTORACTION.fields_by_name[
    "kwargs"
].message_type = _RUNFUNCTIONORCONSTRUCTORACTION_KWARGSENTRY
_RUNFUNCTIONORCONSTRUCTORACTION.fields_by_name[
    "id_at_location"
].message_type = proto_dot_core_dot_common_dot_common__object__pb2._UID
_RUNFUNCTIONORCONSTRUCTORACTION.fields_by_name[
    "address"
].message_type = proto_dot_core_dot_io_dot_address__pb2._ADDRESS
_RUNFUNCTIONORCONSTRUCTORACTION.fields_by_name[
    "msg_id"
].message_type = proto_dot_core_dot_common_dot_common__object__pb2._UID
DESCRIPTOR.message_types_by_name[
    "RunFunctionOrConstructorAction"
] = _RUNFUNCTIONORCONSTRUCTORACTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RunFunctionOrConstructorAction = _reflection.GeneratedProtocolMessageType(
    "RunFunctionOrConstructorAction",
    (_message.Message,),
    {
        "KwargsEntry": _reflection.GeneratedProtocolMessageType(
            "KwargsEntry",
            (_message.Message,),
            {
                "DESCRIPTOR": _RUNFUNCTIONORCONSTRUCTORACTION_KWARGSENTRY,
                "__module__": "proto.core.node.common.action.run_function_or_constructor_pb2"
                # @@protoc_insertion_point(class_scope:syft.core.node.common.action.RunFunctionOrConstructorAction.KwargsEntry)
            },
        ),
        "DESCRIPTOR": _RUNFUNCTIONORCONSTRUCTORACTION,
        "__module__": "proto.core.node.common.action.run_function_or_constructor_pb2"
        # @@protoc_insertion_point(class_scope:syft.core.node.common.action.RunFunctionOrConstructorAction)
    },
)
_sym_db.RegisterMessage(RunFunctionOrConstructorAction)
_sym_db.RegisterMessage(RunFunctionOrConstructorAction.KwargsEntry)


_RUNFUNCTIONORCONSTRUCTORACTION_KWARGSENTRY._options = None
# @@protoc_insertion_point(module_scope)