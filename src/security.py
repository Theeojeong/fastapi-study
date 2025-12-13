from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


def get_access_token(
    auth_header: HTTPAuthorizationCredentials | None = Depends(HTTPBearer()),
) -> str:
    if auth_header is None:
        raise HTTPException(status_code=401, detail="인증 실패")

    return auth_header.credentials
