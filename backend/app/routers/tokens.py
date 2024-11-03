"""Users router."""

from datetime import timedelta

from fastapi import APIRouter, HTTPException, Request, status

from app.internal.data.tokens import AuthenticationTokenCreate, Scope, new_token
from app.internal.data.users import get_user_by_email
from app.internal.security import verify_password

router = APIRouter(prefix="/v1", tags=["tokens"])


@router.post(
    "/tokens/authentification",
    status_code=status.HTTP_201_CREATED,
)
async def create_authentication_token_handler(
    payload: AuthenticationTokenCreate,
    request: Request,
) -> dict[str, str]:
    """Create an authentication token."""
    async with request.app.async_pool.acquire() as conn:
        user = await get_user_by_email(conn, payload.email)

    if not verify_password(
        payload.password.get_secret_value(), user.password_hash.get_secret_value()
    ):
        msg = "Invalid credentials"
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=msg)

    async with request.app.async_pool.acquire() as conn:
        token = await new_token(
            conn, user_id=user.id, scope=Scope.AUTHENTICATION, ttl=timedelta(days=1)
        )

    return {
        "expiry": token.expiry.isoformat(),
        "token": token.plain_text.get_secret_value(),
    }
