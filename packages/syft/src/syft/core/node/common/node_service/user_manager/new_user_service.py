# stdlib
from typing import List
from typing import Optional
from typing import Type
from typing import Union

# third party
from nacl.signing import VerifyKey

# relative
from ......util import traceback_and_raise
from ....abstract.node_service_interface import NodeServiceInterface
from ..auth import service_auth
from ..node_service import ImmediateNodeServiceWithReply
from ..generic_payload.crud_messages import CreateObjectMessage
from ..generic_payload.crud_messages import CreateObjectReplyMessage
from ..generic_payload.crud_messages import UpdateObjectMessage
from ..generic_payload.crud_messages import UpdateObjectReplyMessage
from ..generic_payload.crud_messages import RetrieveObjectMessage
from ..generic_payload.crud_messages import RetrieveObjectReplyMessage
from ..generic_payload.crud_messages import DeleteObjectMessage
from ..generic_payload.crud_messages import DeleteObjectReplyMessage
from ..generic_payload.crud_messages import ErrorReplyMessage
from ..generic_payload.messages import GenericPayloadReplyMessage
from ...exceptions import PyGridError


def process_service(
    node: NodeServiceInterface,
    msg: CreateObjectMessage,
    verify_key: Optional[VerifyKey] = None
) -> Type[GenericPayloadReplyMessage]:
    # 1 - Try Happy Path!
    try:
        result = msg.payload.run(node=node, verify_key=verify_key)

    # 2 - Handle PyGrid related exceptions/errors (Auth errors, Obj Not Found, Missing parameters, etc)
    except PyGridError as pygrid_error:
        # Prepare Response
        msg.kwargs = { RequestAPIFields.STATUS : pygrid_error.status_code,
                    RequestAPIFields.ERROR : pygrid_error.message }

    # 3 - Unexpected Exceptions
    except Exception as e:
        # Prepare Response
        msg.kwargs = {
            RequestAPIFields.STATUS : 500, # Internal Server Error
            RequestAPIFields.ERROR : str(e)
        }
        return ErrorReplyMessage(address=node.address, payload=msg)


class CreateObjectService(ImmediateNodeServiceWithReply):
    
    @staticmethod
    @service_auth(guests_welcome=True)
    def process(
        node: NodeServiceInterface,
        msg: CreateObjectMessage,
        verify_key: Optional[VerifyKey] = None,
    ) -> Union[CreateObjectReplyMessage, ErrorReplyMessage]:
        return process_service(node=node,msg=msg,verify_key=verify_key)

    @staticmethod
    def message_handler_types() -> List[Type[CreateObjectMessage]]:
        return [CreateObjectMessage]


class UpdateObjectService(ImmediateNodeServiceWithReply):

    @staticmethod
    @service_auth(guests_welcome=True)
    def process(
        node: NodeServiceInterface,
        msg: UpdateObjectMessage,
        verify_key: Optional[VerifyKey] = None,
    ) -> Union[UpdateObjectReplyMessage, ErrorReplyMessage]:
        return process_service(node=node,msg=msg,verify_key=verify_key)

    @staticmethod
    def message_handler_types() -> List[Type[UpdateObjectMessage]]:
        return [UpdateObjectMessage]

class RetrieveObjectService(ImmediateNodeServiceWithReply):

    @staticmethod
    @service_auth(guests_welcome=True)
    def process(
        node: NodeServiceInterface,
        msg: RetrieveObjectMessage,
        verify_key: Optional[VerifyKey] = None,
    ) -> Union[RetrieveObjectReplyMessage, ErrorReplyMessage]:
        return process_service(node=node,msg=msg,verify_key=verify_key)

    @staticmethod
    def message_handler_types() -> List[Type[RetrieveObjectMessage]]:
        return [RetrieveObjectMessage]

class DeleteObjectService(ImmediateNodeServiceWithReply):

    @staticmethod
    @service_auth(guests_welcome=True)
    def process(
        node: NodeServiceInterface,
        msg: DeleteObjectMessage,
        verify_key: Optional[VerifyKey] = None,
    ) -> Union[DeleteObjectReplyMessage, ErrorReplyMessage]:
        return process_service(node=node,msg=msg,verify_key=verify_key)

    @staticmethod
    def message_handler_types() -> List[Type[DeleteObjectMessage]]:
        return [DeleteObjectMessage]
