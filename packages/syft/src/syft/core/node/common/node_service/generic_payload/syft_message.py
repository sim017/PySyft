# stdlib
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

# third party
from nacl.signing import VerifyKey

# relative
from .....common.message import ImmediateSyftMessage
from .....common.message import SignedMessage
from .....common.uid import UID
from .....io.address import Address
from ....abstract.node_service_interface import NodeServiceInterface
from ....common.exceptions import AuthorizationError


class NewSyftMessage(ImmediateSyftMessage):
    """A base class from which all message classes should inherit.

    Note:
        This will eventually replace the old `SyftMessage` class.
    """

    __attr_allowlist__ = ["id", "payload", "address", "reply_to", "msg_id", "kwargs"]

    signed_type = SignedMessage

    def __init__(
        self,
        address: Address,
        kwargs: Optional[Dict[str, Any]] = None,
        msg_id: Optional[UID] = None,
        reply_to: Optional[Address] = None,
    ) -> None:
        super().__init__(address=address, msg_id=msg_id)
        self.reply_to = reply_to
        self.kwargs = kwargs if kwargs else {}

    def run(
        self, node: NodeServiceInterface, verify_key: Optional[VerifyKey] = None
    ) -> Dict[str, Any]:
        raise NotImplementedError

    def get_permissions(self) -> List:
        """Returns the list of permission classes applicable to the given message."""
        raise NotImplementedError

    def check_permissions(
        self, node: NodeServiceInterface, verify_key: Optional[VerifyKey] = None
    ) -> None:
        """Check if the user has relevant permissions to run this message.

        Args:
            node (NodeServiceInterface): node interface used to invoke this message.
            verify_key (Optional[VerifyKey], optional): user signed verification key. Defaults to None.

        Raises:
            AuthorizationError: Error when one of the permission is denied.
        """
        for permission_class in self.get_permissions():
            if not permission_class().has_permission(
                msg=self, node=node, verify_key=verify_key
            ):
                raise AuthorizationError(
                    f"You don't have access to perform {self} action."
                )
