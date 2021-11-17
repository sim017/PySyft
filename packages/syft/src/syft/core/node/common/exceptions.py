from typing import Optional

"""Specific PyGrid exceptions."""


class PyGridError(Exception):
    status_code = 500

    def __init__(self, message: str) -> None:
        super().__init__(message)

class MissingDAAError(PyGridError):
    def __init__(self, message: Optional[str] = "", status_code: Optional[int] = 401) -> None:
        if not message:
            message = "You can't apply a new User without a DAA document!"
        super().__init__(message)


class AuthorizationError(PyGridError):
    def __init__(self, message: Optional[str] = "", status_code: Optional[int] = 401) -> None:
        if not message:
            message = "User is not authorized for this operation!"
        super().__init__(message)


class OwnerAlreadyExistsError(PyGridError):
    def __init__(self, message: Optional[str] = "", status_code: Optional[int] = 409) -> None:
        if not message:
            message = "This PyGrid domain already has an owner!"
        super().__init__(message)


class RoleNotFoundError(PyGridError):
    def __init__(self, message: Optional[str] = "", status_code: Optional[int] = 404) -> None:
        if not message:
            message = "Role ID not found!"
        super().__init__(message)


class WorkerNotFoundError(PyGridError):
    def __init__(self, message: Optional[str] = "", status_code: Optional[int] = 404) -> None:
        if not message:
            message = "Worker ID not found!"
        super().__init__(message)


class UserNotFoundError(PyGridError):
    def __init__(self, message: Optional[str] = "", status_code: Optional[int] = 404) -> None:
        if not message:
            message = "User not found!"
        super().__init__(message)


class EnvironmentNotFoundError(PyGridError):
    def __init__(self, message: Optional[str] = "", status_code: Optional[int] = 404) -> None:
        if not message:
            message = "Environment not found!"
        super().__init__(message)


class SetupNotFoundError(PyGridError):
    def __init__(self, message: Optional[str] = "", status_code: Optional[int] = 404) -> None:
        if not message:
            message = "Setup not found!"
        super().__init__(message)


class InvalidRequestKeyError(PyGridError):

    def __init__(self, message: Optional[str] = "", status_code: Optional[int] = 404) -> None:
        if not message:
            message = "Invalid request key!"
        super().__init__(message)


class InvalidCredentialsError(PyGridError):
    def __init__(self, message: Optional[str] = "", status_code: Optional[int] = 401) -> None:
        if not message:
            message = "Invalid credentials!"
        super().__init__(message)


class MissingRequestKeyError(PyGridError):
    def __init__(self, message: Optional[str] = "", status_code: Optional[int] = 400) -> None:
        if not message:
            message = "Missing request key!"
        super().__init__(message)


class AssociationRequestError(PyGridError):

    def __init__(self, message: Optional[str] = "", status_code: Optional[int] = 404) -> None:
        if not message:
            message = "Association Request ID not found!"
        super().__init__(message)


class AssociationNotFoundError(PyGridError):
    
    def __init__(self, message: Optional[str] = "", status_code: Optional[int] = 404) -> None:
        if not message:
            message = "Association ID not found!"
        super().__init__(message)


class RequestError(PyGridError):
    
    def __init__(self, message: Optional[str] = "", status_code: Optional[int] = 404) -> None:
        if not message:
            message = "Request ID not found!"
        super().__init__(message)


class DatasetNotFoundError(PyGridError):

    def __init__(self, message: Optional[str] = "", status_code: Optional[int] = 404) -> None:
        if not message:
            message = "Dataset ID not found!"
        super().__init__(message)


class InvalidParameterValueError(PyGridError):

    def __init__(self, message: Optional[str] = "", status_code: Optional[int] = 400) -> None:
        if not message:
            message = "Passed paramater value not valid!"
        super().__init__(message)
