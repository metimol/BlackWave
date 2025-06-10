"""
Exception handling for the Blackwave Bot Service.
Defines custom exceptions and exception handlers.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


class BlackwaveException(Exception):
    """Base exception for Blackwave Bot Service."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class APIError(BlackwaveException):
    """Exception raised for errors in the API."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message, status_code)


class LLMError(BlackwaveException):
    """Exception raised for errors in LLM interactions."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message, status_code)


class BotError(BlackwaveException):
    """Exception raised for errors in bot operations."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message, status_code)


class DatabaseError(BlackwaveException):
    """Exception raised for errors in database operations."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message, status_code)


async def blackwave_exception_handler(request: Request, exc: BlackwaveException):
    """Handler for BlackwaveException."""
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler for validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": str(exc)}
    )


def setup_exception_handlers(app):
    """Register exception handlers with the FastAPI app."""
    app.add_exception_handler(BlackwaveException, blackwave_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
