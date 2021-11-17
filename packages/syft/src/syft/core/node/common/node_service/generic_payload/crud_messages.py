# future
from __future__ import annotations

# stdlib
from typing import Any
from typing import Dict
from typing import Optional

# third party
from nacl.signing import VerifyKey
from typing_extensions import final

# relative
from .....common.serde.serializable import serializable
from .messages import GenericPayloadMessage
from .messages import GenericPayloadMessageWithReply
from .messages import GenericPayloadReplyMessage



@serializable(recursive_serde=True)
@final
class ErrorReplyMessage(GenericPayloadReplyMessage):
    ...


# CREATE
@serializable(recursive_serde=True)
@final
class CreateObjectMessage(GenericPayloadMessage):
    ...

@serializable(recursive_serde=True)
@final
class CreateObjectReplyMessage(GenericPayloadReplyMessage):
    ...


# UPDATE
@serializable(recursive_serde=True)
@final
class UpdateObjectMessage(GenericPayloadMessage):
    ...

@serializable(recursive_serde=True)
@final
class UpdateObjectReplyMessage(GenericPayloadReplyMessage):
    ...


# DELETE
@serializable(recursive_serde=True)
@final
class DeleteObjectMessage(GenericPayloadMessage):
    ...

@serializable(recursive_serde=True)
@final
class DeleteObjectReplyMessage(GenericPayloadReplyMessage):
    ...


# RETRIEVE
@serializable(recursive_serde=True)
@final
class RetrieveObjectMessage(GenericPayloadMessage):
    ...

@serializable(recursive_serde=True)
@final
class RetrieveObjectReplyMessage(GenericPayloadReplyMessage):
    ...
