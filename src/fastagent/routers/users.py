"""Users router."""

from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, HTTPException, Request, status

from app.internal.data.users import UserCreate, insert_user

router = APIRouter(prefix="/v1", tags=["users"])


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
)
async def register_user_handler(
    payload: UserCreate,
    request: Request,
) -> dict[str, str]:
    """Register a user."""
    async with request.app.async_pool.acquire() as conn:
        try:
            await insert_user(conn, payload)
        except UniqueViolationError as e:
            msg = "User already exists"
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg) from e

    return {"message": "User registered"}
