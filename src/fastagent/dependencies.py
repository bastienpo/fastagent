"""Dependencies."""

from app.internal.data.users import is_anonymous
from fastapi import Depends, HTTPException, Request, status


def require_auth(request: Request) -> None:
    """Raise an error if the user is anonymous.

    Args:
        request: The request.

    Raises:
        HTTPException: If the user is anonymous.
    """
    if request.state.context is None or is_anonymous(request.state.context.user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


require_auth_dependency = Depends(require_auth)
