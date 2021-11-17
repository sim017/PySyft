# stdlib
from enum import Enum


class PyGridClientEnums(str, Enum):
    ENCODING = "ISO-8859-1"


class RestAPICodes(int, Enum):
    CREATED = 201
    SUCCESS = 200
    UNAUTHORIZED = 401
    BAD_REQUEST = 400
    CONFLICT = 409
    NOT_FOUND = 404

class RequestAPIFields(str, Enum):
    ADDRESS = "address"
    UID = "uid"
    POINTABLE = "pointable"
    QUERY = "query"
    CONTENT = "content"
    REPLY_TO = "reply_to"
    MESSAGE = "message"
    ERROR = "error"
    RESPONSE = "response"
    SOURCE = "source"
    TARGET = "target"
    NODE = "node"
    REQUESTED_DATE = "requested_date"
    STATUS = "status"


class AssociationRequestResponses(str, Enum):
    ACCEPT = "ACCEPTED"
    DENY = "REJECTED"
    PENDING = "PENDING"


class ResponseObjectEnum(str, Enum):
    ASSOCIATION_REQUEST = "association-request"
    DATASET = "dataset"
    GROUP = "group"
    ROLE = "role"
    USER = "user"
    WORKER = "worker"
    DATA = "data"
