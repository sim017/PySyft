# future
from __future__ import annotations

# stdlib
import json
import os
import re
import time
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

# third party
from nacl.signing import VerifyKey
import requests
from typing_extensions import final

# relative
from .....common.serde.serializable import serializable
from .....node.domain.enums import RequestAPIFields, RestAPICodes
from ....abstract.node import AbstractNode
from ..generic_payload.crud_messages import CreateObjectMessage
from ..generic_payload.crud_messages import CreateObjectReplyMessage
from ..generic_payload.crud_messages import UpdateObjectMessage
from ..generic_payload.crud_messages import UpdateObjectReplyMessage
from ..generic_payload.crud_messages import DeleteObjectMessage
from ..generic_payload.crud_messages import DeleteObjectReplyMessage
from ..generic_payload.crud_messages import RetrieveObjectMessage
from ..generic_payload.crud_messages import RetrieveObjectReplyMessage
from ..generic_payload.crud_messages import ErrorReplyMessage
from ..generic_payload.messages import GenericPayloadMessageWithReply
from ...exceptions import PyGridError, MissingDAAError

# CREATE User
@serializable(recursive_serde=True)
@final
class CreateUserReplyMessage(CreateObjectReplyMessage):
    ...

@serializable(recursive_serde=True)
@final
class CreateUserMessage(GenericPayloadMessageWithReply):
    message_type = CreateObjectMessage
    message_reply_type = CreateObjectReplyMessage
    
    def run(
        self, node: AbstractNode, verify_key: VerifyKey
    ) -> CreateUserReplyMessage:
        # 1 - Check if node requires daa document
        if node.setup.first(domain_name=node.name).daa and not msg.daa_pdf:
            raise MissingDAAError
        
        # 2 -  Create User Application
        app_id = node.users.create_user_application(
            name=msg.name,
            email=msg.email,
            password=msg.password,
            daa_pdf=msg.daa_pdf,
            institution=msg.institution,
            website=msg.website,
            budget=msg.budget,
        )

        # 3 - Check if current user can also create new users
        # It'll skip the applicant approval step
        user_role_id = node.users.role(verify_key=verify_key).id
        if node.roles.can_create_users(role_id=user_role_id):
            node.users.process_user_application(
                candidate_id=app_id, status="accepted", verify_key=verify_key
            )
            
        # Prepare Response
        self.kwargs  = {
            RequestAPIFields.STATUS : RestAPICodes.CREATED,
            RequestAPIFields.MESSAGE : "User creation success!"
        }
        
        return CreateUserReplyMessage(address=node.address, payload=self)


# UPDATE User
@serializable(recursive_serde=True)
@final
class UpdateUserReplyMessage(CreateObjectReplyMessage):
    ...


@serializable(recursive_serde=True)
@final
class UpdateUserMessage(GenericPayloadMessageWithReply):
    message_type = UpdateObjectMessage
    message_reply_type = UpdateObjectReplyMessage

    def run(
        self, node: AbstractNode, verify_key: Optional[VerifyKey] = None
    ) -> UpdateUserReplyMessage:
        return UpdateUserReplyMessage(address=node.address, payload=self)


# RETRIEVE User
@serializable(recursive_serde=True)
@final
class RetrieveUserReplyMessage(CreateObjectReplyMessage):
    ...

@serializable(recursive_serde=True)
@final
class RetrieveUserMessage(GenericPayloadMessageWithReply):
    message_type = RetrieveObjectMessage
    message_reply_type = RetrieveObjectReplyMessage

    def run(
        self, node: AbstractNode, verify_key: Optional[VerifyKey] = None
    ) -> RetrieveUserReplyMessage:
        return RetrieveUserReplyMessage(address=node.address, payload=self)



# DELETE User
@serializable(recursive_serde=True)
@final
class DeleteUserReplyMessage(CreateObjectReplyMessage):
    ...

@serializable(recursive_serde=True)
@final
class DeleteUserMessage(GenericPayloadMessageWithReply):
    message_type = DeleteObjectMessage
    message_reply_type = DeleteObjectReplyMessage

    def run(
        self, node: AbstractNode, verify_key: Optional[VerifyKey] = None
    ) -> DeleteUserReplyMessage:
        return DeleteUserReplyMessage(address=node.address, payload=self)
