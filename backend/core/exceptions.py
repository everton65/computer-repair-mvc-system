from fastapi import HTTPException, status
from typing import Any, Optional


class AppException(Exception):
    """Base exception for application errors."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Any] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)

    def to_dict(self) -> dict:
        result = {"error": self.message}
        if self.details:
            result["details"] = self.details
        return result


class NotFoundException(AppException):
    """Exception for resource not found errors."""

    def __init__(self, resource: str, identifier: str = None):
        message = f"{resource} não encontrado"
        if identifier:
            message = f"{resource} com ID '{identifier}' não encontrado"
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class ValidationException(AppException):
    """Exception for validation errors."""

    def __init__(self, message: str, details: Any = None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, details)


class DatabaseException(AppException):
    """Exception for database errors."""

    def __init__(self, message: str = "Erro no banco de dados"):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


def exception_handler(exc: AppException) -> HTTPException:
    """Convert AppException to FastAPI HTTPException."""
    return HTTPException(
        status_code=exc.status_code,
        detail=exc.to_dict()
    )