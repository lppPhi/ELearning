from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.auth.auth_handler import verify_jwt

class AuthBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            return credentials
        raise HTTPException(status_code=403, detail="Invalid authentication credentials")

async def auth_required(credentials: HTTPAuthorizationCredentials = Depends(AuthBearer())):
    try:
        payload = verify_jwt(credentials.credentials)
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")