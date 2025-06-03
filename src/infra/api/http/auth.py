import os
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()
public_key = f"-----BEGIN PUBLIC KEY-----\n{os.getenv('KEYCLOAK_PUBLIC_KEY')}\n-----END PUBLIC KEY-----\n"


def authenticate(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(security),
    ],
) -> None:
    encoded = credentials.credentials
    try:
        jwt.decode(
            jwt=encoded,
            key=public_key,
            algorithms=["RS256"],
            audience="account",
        )
    except jwt.PyJWKError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        ) from e
