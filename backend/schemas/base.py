from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    meta: Optional[dict] = None


def ok(data: T, meta: Optional[dict] = None) -> dict:
    return ApiResponse(success=True, data=data, meta=meta).model_dump()


def err(message: str) -> dict:
    return ApiResponse(success=False, error=message).model_dump()
