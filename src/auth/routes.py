from fastapi import APIRouter, Depends, status, Form
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from datetime import timedelta , datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .schemas import UserCreateModel, UserModel, UserLoginModel, UserBooksModel, EmailModel, PasswordResetRequestModel, PasswordResetConfirmModel
from .service import UserService
from .utils import create_access_token, verify_password, create_url_safe_token, decode_url_safe_token, generate_passwd_hash
from .dependencies import RefreshTokenBearer , get_current_user, RoleChecker
from src.errors import UserAlreadyExists, InvalidCredentials, RevokedToken, UserNotFound
from src.mail import mail, create_message
from src.config import Config
from src.db.main import get_session


auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin","user"])

REFRESH_TOKEN_EXPIRY = 2

@auth_router.post("/send_mail")
async def send_mail(emails:EmailModel):
    emails = emails.addresses
    html = "<h1>Welcome to the app.</h1>"

    message = create_message(
        recipients=emails,
        subject="Welcome",
        body=html
    )
    await mail.send_message(message)
    return {"message":"Email Sent Successfully"}

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await user_service.user_exixts(email, session)
    if user_exists:
        raise UserAlreadyExists()
    new_user = await user_service.create_user(user_data, session)
    token = create_url_safe_token({"email":email})
    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"
    html_message = f"""
    <h1>Verify your email</h1>
    <p>Please click this <a href="{link}">link</a> to verify email.</p>
    """
    message = create_message(
        recipients=[email],
        subject="Verify your email",
        body=html_message
    )
    await mail.send_message(message)
    return {
        "message":"Your Account has been created! Please check email to verify your account",
        "user":new_user
    }

@auth_router.get("/verify/{token}")
async def verify_user_account(token:str, session: AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")
    if user_email:
        user = await user_service.get_user_by_email(user_email, session)
        if not user:
            raise UserNotFound()
        await user_service.update_user(user, {"is_verified":True}, session)
        return JSONResponse(content={
            "message":"Account Verified Successfully."
        }, status_code=status.HTTP_200_OK)
    return JSONResponse(content={
        "message":"Error occured during verification"
    }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@auth_router.post("/login")
async def login_users(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password
    user = await user_service.get_user_by_email(email, session)
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.user_id), "role":user.role},
                refresh=False,
                expiry=timedelta(minutes=15)
            )
            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.user_id)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )
            return JSONResponse(
                content={
                    "message": "Login Successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.user_id)}
                }
            )
    raise InvalidCredentials()


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details["user"]
        )
        return JSONResponse (content={"access_token":new_access_token})
    raise RevokedToken()

@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(user = Depends(get_current_user), _:bool=Depends(role_checker)):
    return user


# @auth_router.get("/logout")
# async def revoke_token(token_details : dict = Depends(AccessTokenBearer())):
#     jti = token_details["jti"]
#     await add_jti_to_blocklist(jti)
#     return JSONResponse(
#         content={"message":"Logged out Successfully"}, status_code=status.HTTP_200_OK
#     )  ............. redis part

@auth_router.post("/password-reset-request")
async def pass_reset_request(email_data: PasswordResetRequestModel):
    email = email_data.email
    token = create_url_safe_token({"email":email})
    link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"
    html_message = f"""
    <h1>Reset your Password</h1>
    <p>Please click this <a href="{link}">link</a> to reset your Password.</p>
    """
    message = create_message(
        recipients=[email],
        subject="Reset your Password",
        body=html_message
    )
    await mail.send_message(message)
    return JSONResponse(
        content={
            "message":"Please check your email to reset password."
        },status_code=status.HTTP_200_OK
    )

# @auth_router.get("/password-reset-confirm/{token}")
# async def show_password_reset_form(token: str):
#     # You can return a simple message or HTML form here
#     return JSONResponse(
#         content={"message": "Please submit your new password via POST to this URL."},
#         status_code=status.HTTP_200_OK
#     )

@auth_router.get("/password-reset-confirm/{token}", response_class=HTMLResponse)
async def show_password_reset_form(token: str):
    return f"""
    <html>
        <head>
            <title>Reset Password</title>
        </head>
        <body>
            <h2>Reset your password</h2>
            <form action="/api/v1/auth/password-reset-confirm/{token}" method="post">
                <label>New Password:</label><br>
                <input type="password" name="new_password" required><br>
                <label>Confirm New Password:</label><br>
                <input type="password" name="confirm_new_password" required><br><br>
                <input type="submit" value="Reset Password">
            </form>
        </body>
    </html>
    """

# @auth_router.post("/password-reset-confirm/{token}")
# async def reset_account_password(token:str, passwords: PasswordResetConfirmModel, session: AsyncSession = Depends(get_session)):
#     new_password = passwords.new_password
#     confirm_password = passwords.confirm_new_password
#     if new_password != confirm_password:
#         raise HTTPException(detail="Password does not match", status_code=status.HTTP_400_BAD_REQUEST)
#     token_data = decode_url_safe_token(token)
#     user_email = token_data.get("email")
#     if user_email:
#         user = await user_service.get_user_by_email(user_email, session)
#         if not user:
#             raise UserNotFound()
#         passwd_hash = generate_passwd_hash(new_password)
#         await user_service.update_user(user, {"password_hash": passwd_hash}, session)
#         return JSONResponse(content={
#             "message":"Password Reset Successfully."
#         }, status_code=status.HTTP_200_OK)
#     return JSONResponse(content={
#         "message":"Error occured during password reset."
#     }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@auth_router.post("/password-reset-confirm/{token}")
async def reset_account_password(
    token: str,
    new_password: str = Form(...),
    confirm_new_password: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    if new_password != confirm_new_password:
        return HTMLResponse(content="<h3>Password does not match.</h3>", status_code=400)
    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email") if token_data else None
    if user_email:
        user = await user_service.get_user_by_email(user_email, session)
        if not user:
            return HTMLResponse(content="<h3>User not found.</h3>", status_code=404)
        passwd_hash = generate_passwd_hash(new_password)
        await user_service.update_user(user, {"password_hash": passwd_hash}, session)
        return HTMLResponse(content="<h3>Password Reset Successfully.</h3>", status_code=200)
    return HTMLResponse(content="<h3>Error occurred during password reset.</h3>", status_code=500)