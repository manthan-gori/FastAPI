from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from .utils import decode_token
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import UserService
from typing import List, Any
from src.db.models import User
from src.errors import InvalidToken, AccessTokenRequired, RefreshTokenRequired, InsufficientPermission

user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)
        if not token_data:  # Check if token_data is None
            raise InvalidToken()
        self.verify_token_data(token_data)
        return token_data

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        
        # Ensure the token is an access token.
        
        if token_data.get("refresh"): 
            raise AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if not token_data.get("refresh"):  
            raise RefreshTokenRequired()
        
async def get_current_user(
        token_details: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_session)
        ):
    user_email = token_details["user"]["email"]
    user = await user_service.get_user_by_email(user_email , session)
    return user

class RoleChecker:
    def __init__(self,allowed_roles:List[str]) -> None:
        self.allowed_roled = allowed_roles

    def __call__(self, current_user: User= Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roled:
            return True
        
        raise InsufficientPermission()