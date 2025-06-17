from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from src.books.routes import book_router
from src.db.main import init_db
from src.auth.routes import auth_router
from src.reviews import review_router
from .errors import (
    create_exception_handler,
    InvalidToken,
    RevokedToken,
    AccessTokenRequired,
    RefreshTokenRequired,
    UserAlreadyExists,
    InvalidCredentials,
    InsufficientPermission,
    UserNotFound,
    BookNotFound,
    AccountNotVerified
)
from .middleware import register_middleware

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting ...")
    await init_db()
    yield
    print(f"server has been stopped")

version ="v1"

app = FastAPI(
    title="bookly",
    description="A Rest API for a book review web service",
    version= version
)

app.add_exception_handler(
    InvalidToken,
    create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        initial_detail={
            "message":"The provided token is invalid.",
            "error_code":"Invalid Token"
        }
    )
)

app.add_exception_handler(
    InvalidCredentials,
    create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        initial_detail={
            "message":"The provided credentials are incorrect.",
            "error_code":"Invalid Credentials"
        }
    )
)

app.add_exception_handler(
    UserAlreadyExists,
    create_exception_handler(
        status_code=status.HTTP_409_CONFLICT,
        initial_detail={
            "message":"User already exists.",
            "error_code":"User Exists"
        }
    )
)

app.add_exception_handler(
    UserNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message":"The requested user could not be found.",
            "error_code":"User Not Found"
        }
    )
)

app.add_exception_handler(
    BookNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message":"The requested book does not exist.",
            "error_code":"Book Not Found"
        }
    )
)

app.add_exception_handler(
    InsufficientPermission,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message":"You do not have sufficient permissions to access this resource.",
            "error_code":"Insufficient Permission"
        }
    )
)

app.add_exception_handler(
    AccountNotVerified,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message":"The account has not been verified yet.",
            "error_code":"Account Not Verified"
        }
    )
)

app.add_exception_handler(
    RevokedToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message":"The token has been revoked and cannot be used.",
            "error_code":"Revoked Token"
        }
    )
)

app.add_exception_handler(
    AccessTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message":"An access token is required for authentication.",
            "error_code":"Access Token Required"
        }
    )
)

app.add_exception_handler(
    RefreshTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message":"A refresh token is required to obtain a new access token.",
            "error_code":"Refresh Token Required"
        }
    )
)

@app.exception_handler(500)
async def internal_server_error(requent, exc):
    return JSONResponse(
        content={"message":"Oops! something went wrong","error_code":"server error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

register_middleware(app)


app.include_router(book_router , prefix=f"/api/{version}/books" , tags=["books"])
app.include_router(auth_router , prefix=f"/api/{version}/auth" , tags=["auth"])
app.include_router(review_router , prefix=f"/api/{version}/review" , tags=["review"])