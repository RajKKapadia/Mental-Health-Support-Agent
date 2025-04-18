from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from src import config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def verify_api_key(api_key: str = Depends(oauth2_scheme)) -> bool:
    if api_key:
        if config.SERVER_API_KEY == api_key:
            return True
        else:
            HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
            )
    else:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Provide API key",
        )
