# stdlib
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import Union

# third party
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from nacl.signing import VerifyKey
from typing_extensions import final

# relative
from .....common.serde.serializable import serializable
from ....abstract.node_service_interface import NodeServiceInterface
from ....domain.domain_interface import DomainInterface
from ....domain.registry import DomainMessageRegistry
from ...exceptions import AuthorizationError
from ...exceptions import MissingRequestKeyError
from ...exceptions import UserNotFoundError
from ...node_table.utils import model_to_json
from ..generic_payload.syft_message import NewSyftMessage
from ..permissions import BasePermission
from .user_permissions import IsNodeDaaEnabled
from .user_permissions import UserCanCreateUsers
from .user_permissions import UserCanTriageRequest
from .user_permissions import UserIsOwner


@serializable(recursive_serde=True)
@final
class GetUserMessage(NewSyftMessage, DomainMessageRegistry):
    def run(
        self, node: NodeServiceInterface, verify_key: Optional[VerifyKey] = None
    ) -> Dict[str, Any]:

        # Extract User Columns
        user = node.users.first(id=self.kwargs["user_id"])  # type: ignore
        _msg = model_to_json(user)

        # Use role name instead of role ID.
        _msg["role"] = node.roles.first(id=_msg["role"]).name  # type: ignore

        # Remove private key
        del _msg["private_key"]

        # Get budget spent
        _msg["budget_spent"] = node.acc.user_budget(  # type: ignore
            user_key=VerifyKey(user.verify_key.encode("utf-8"), encoder=HexEncoder)
        )
        return _msg

    def get_permissions(self) -> List[Type[BasePermission]]:
        return [UserCanTriageRequest]


@serializable(recursive_serde=True)
@final
class GetUsersMessage(NewSyftMessage, DomainMessageRegistry):
    def run(
        self, node: NodeServiceInterface, verify_key: Optional[VerifyKey] = None
    ) -> Dict[str, Any]:
        users = node.users.all()
        _msg = []
        for user in users:
            _user_json = model_to_json(user)
            # Use role name instead of role ID.
            _user_json["role"] = node.roles.first(id=_user_json["role"]).name

            # Remove private key
            del _user_json["private_key"]

            # Remaining Budget
            # TODO: Rename it from budget_spent to remaining budget
            _user_json["budget_spent"] = node.acc.get_remaining_budget(  # type: ignore
                user_key=VerifyKey(user.verify_key.encode("utf-8"), encoder=HexEncoder),
                returned_epsilon_is_private=False,
            )
            _msg.append(_user_json)

        _msgs = {"users": _msg}
        return _msgs

    def get_permissions(self) -> List[Type[BasePermission]]:
        return [UserCanTriageRequest]


@serializable(recursive_serde=True)
@final
class UpdateUserMessage(NewSyftMessage, DomainMessageRegistry):
    @staticmethod
    def __validate_message(message: object) -> bool:
        _valid_parameters = (
            hasattr(message, "email")
            or hasattr(message, "password")
            or hasattr(message, "role")
            or hasattr(message, "groups")
            or hasattr(message, "name")
            or hasattr(message, "budget")
        )
        return _valid_parameters

    def run(
        self, node: NodeServiceInterface, verify_key: Optional[VerifyKey] = None
    ) -> Dict[str, Any]:

        msg = type("message", (object,), self.kwargs.upcast())()

        # Change own information
        if msg.user_id == 0:
            msg.user_id = int(node.users.get_user(verify_key).id)  # type: ignore

        _valid_user = node.users.contain(id=msg.user_id)

        if not self.__validate_message(msg):
            raise MissingRequestKeyError(
                "Missing json fields (email, password, role, groups, name)"
            )

        if not _valid_user:
            raise UserNotFoundError

        if hasattr(msg, "institution"):
            node.users.set(user_id=str(msg.user_id), institution=msg.institution)

        if hasattr(msg, "website"):
            node.users.set(user_id=str(msg.user_id), website=msg.website)

        if hasattr(msg, "budget"):
            node.users.set(user_id=str(msg.user_id), budget=msg.budget)

        # Change Email Request
        elif hasattr(msg, "email"):
            node.users.set(user_id=str(msg.user_id), email=msg.email)

        # Change Password Request
        elif hasattr(msg, "password"):
            node.users.set(user_id=str(msg.user_id), password=msg.password)

        # Change Name Request
        elif hasattr(msg, "name"):
            node.users.set(user_id=str(msg.user_id), name=msg.name)

        # Change Role Request
        elif hasattr(msg, "role"):
            target_user = node.users.first(id=msg.user_id)
            _allowed = (
                msg.role != node.roles.owner_role.name  # Target Role != Owner
                and target_user.role
                != node.roles.owner_role.id  # Target User Role != Owner
                and node.users.can_create_users(
                    verify_key=verify_key
                )  # Key Permissions
            )

            # If all premises were respected
            if _allowed:
                new_role_id = node.roles.first(name=msg.role).id
                node.users.set(user_id=msg.user_id, role=new_role_id)  # type: ignore
            elif (  # Transfering Owner's role
                msg.role == node.roles.owner_role.name  # target role == Owner
                and node.users.role(verify_key=verify_key).name
                == node.roles.owner_role.name  # Current user is the current node owner.
            ):
                new_role_id = node.roles.first(name=msg.role).id
                node.users.set(user_id=str(msg.user_id), role=new_role_id)
                current_user = node.users.get_user(verify_key=verify_key)
                node.users.set(user_id=current_user.id, role=node.roles.admin_role.id)  # type: ignore
                # Updating current node keys
                root_key = SigningKey(
                    current_user.private_key.encode("utf-8"), encoder=HexEncoder  # type: ignore
                )
                node.signing_key = root_key
                node.verify_key = root_key.verify_key
                # IDK why, but we also have a different var (node.root_verify_key)
                # defined at ...common.node.py that points to the verify_key.
                # So we need to update it as well.
                node.root_verify_key = root_key.verify_key
            elif target_user.role == node.roles.owner_role.id:
                raise AuthorizationError(
                    "You're not allowed to change Owner user roles!"
                )
            else:
                raise AuthorizationError("You're not allowed to change User roles!")

        return {"resp_msg": "User updated successfully!"}

    def get_permissions(self) -> List[Union[Type[BasePermission], Any]]:
        return [UserCanCreateUsers | UserIsOwner]


@serializable(recursive_serde=True)
@final
class CreateUserMessage(NewSyftMessage, DomainMessageRegistry):
    def run(  # type: ignore[override]
        self, node: DomainInterface, verify_key: Optional[VerifyKey] = None
    ) -> Dict[str, Any]:

        msg = type("message", (object,), dict(self.kwargs.upcast()))()  # type: ignore

        # Check if email/password fields are empty
        if not getattr(msg, "email", "") or not getattr(msg, "password", ""):
            raise MissingRequestKeyError(
                message="Invalid request payload, empty fields (email/password)!"
            )

        # Check if this email was already registered
        try:
            node.users.first(email=msg.email)
            # If the email has already been registered, raise exception
            raise AuthorizationError(
                message="You can't create a new User using this email!"
            )
        except UserNotFoundError:
            # If email not registered, a new user can be created.
            pass

        app_id = node.users.create_user_application(
            name=msg.name,
            email=msg.email,
            password=msg.password,
            daa_pdf=msg.daa_pdf,
            institution=msg.institution,
            website=msg.website,
            budget=msg.budget,
        )

        node.users.process_user_application(
            candidate_id=app_id, status="accepted", verify_key=verify_key
        )

        return {"resp_msg": "User created successfully!"}

    def get_permissions(self) -> List[Type[BasePermission]]:
        return [UserCanCreateUsers, IsNodeDaaEnabled]


@serializable(recursive_serde=True)
@final
class DeleteUserMessage(NewSyftMessage, DomainMessageRegistry):
    def run(  # type: ignore
        self, node: NodeServiceInterface, verify_key: Optional[VerifyKey] = None
    ) -> Dict[str, Any]:

        msg = type("message", (object,), dict(self.kwargs))()
        node.users.delete(id=msg.user_id)

        return {"resp_msg": "User deleted successfully!"}

    def get_permissions(self) -> Union[Type[BasePermission], Any]:
        return [UserCanCreateUsers, ~UserIsOwner]
