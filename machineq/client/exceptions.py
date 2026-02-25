"""API exceptions and error handling for MachineQ client."""

from __future__ import annotations

from typing import Any


class MachineQError(Exception):
    """Base exception for all MachineQ client errors."""

    pass


class APIError(MachineQError):
    """Base exception for API errors."""

    def __init__(
        self,
        message: str,
        code: int | None = None,
        details: list[Any] | None = None,
        status_code: int | None = None,
    ):
        """Initialize APIError.

        Args:
            message: Error message
            code: gRPC error code
            details: gRPC error details
            status_code: HTTP status code
        """
        self.message = message
        self.code = code
        self.details = details or []
        self.status_code = status_code
        super().__init__(message)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r}, code={self.code}, status_code={self.status_code})"


class ValidationError(APIError):
    """Raised when request validation fails (gRPC code 3)."""

    pass


class NotFound(APIError):
    """Raised when a resource is not found (gRPC code 5)."""

    pass


class PermissionDenied(APIError):
    """Raised when user lacks permission (gRPC code 7)."""

    pass


class InvalidArgument(APIError):
    """Raised when an argument is invalid (gRPC code 3)."""

    pass


class Unauthorized(APIError):
    """Raised when authentication fails (gRPC code 16)."""

    pass


class Unauthenticated(APIError):
    """Raised when user is not authenticated."""

    pass


class InternalServerError(APIError):
    """Raised when server encounters an error (gRPC code 13)."""

    pass


class ServiceUnavailable(APIError):
    """Raised when service is unavailable (gRPC code 14)."""

    pass


class RateLimited(APIError):
    """Raised when rate limit is exceeded."""

    pass


# gRPC code to exception mapping
GRPC_CODE_TO_EXCEPTION: dict[int, type[APIError]] = {
    3: ValidationError,  # INVALID_ARGUMENT
    5: NotFound,  # NOT_FOUND
    7: PermissionDenied,  # PERMISSION_DENIED
    13: InternalServerError,  # INTERNAL
    14: ServiceUnavailable,  # UNAVAILABLE
    16: Unauthorized,  # UNAUTHENTICATED
}

# HTTP status code to exception mapping
HTTP_STATUS_TO_EXCEPTION: dict[int, type[APIError]] = {
    400: ValidationError,
    401: Unauthorized,
    403: PermissionDenied,
    404: NotFound,
    429: RateLimited,
    500: InternalServerError,
    503: ServiceUnavailable,
}


def parse_error_response(data: dict[str, Any], status_code: int | None = None) -> APIError:
    """Parse gRPC error response into appropriate exception.

    Args:
        data: Response JSON (should contain 'code', 'message', 'details')
        status_code: HTTP status code (optional)

    Returns:
        Appropriate APIError subclass instance
    """
    message = data.get("message", "Unknown error")
    code = data.get("code")
    details = data.get("details", [])

    # Determine exception class
    exception_class = APIError

    # Try gRPC code first (more specific)
    if code is not None and isinstance(code, int):
        exception_class = GRPC_CODE_TO_EXCEPTION.get(code, APIError)
    # Fall back to HTTP status code
    elif status_code is not None:
        exception_class = HTTP_STATUS_TO_EXCEPTION.get(status_code, APIError)

    return exception_class(
        message=message,
        code=code,
        details=details,
        status_code=status_code,
    )
