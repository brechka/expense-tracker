from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.helpers.logger import logger
from src.helpers.security import decode_refresh_token
from src.models.user_models import UserCreate, UserLogin, TokenResponse, MessageResponse
from src.models.reset_code_models import ForgotPasswordRequest, ForgotPasswordResponse, RestorePasswordRequest, RestorePasswordResponse
from src.services.users_service import create_user, authenticate_user, get_user_by_email, get_user_by_id, change_password
from src.services.auth_service import issue_tokens, rotate_refresh, revoke_refresh, revoke_all_user_tokens
from src.services.reset_code_service import create_reset_code, generate_reset_link, validate_reset_code, consume_reset_code
from src.helpers.email import email_service
from src.config import REFRESH_TOKEN_EXPIRE_DAYS, ENV

router = APIRouter(prefix="/api/auth", tags=["auth"])

_REFRESH_MAX_AGE = REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60


def _set_refresh_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key="refresh_token", value=token,
        httponly=True, samesite="lax", max_age=_REFRESH_MAX_AGE, secure=ENV == "production", path="/",
    )


def _clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(key="refresh_token", path="/", samesite="lax")


@router.post("/sign-up", response_model=TokenResponse, status_code=201)
def sign_up(body: UserCreate, response: Response, db: Session = Depends(get_db)):
    if get_user_by_email(db, body.email):
        logger.warning("Sign-up failed: email already registered: %s", body.email)
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, body.email, body.name, body.password)
    access, refresh = issue_tokens(db, user.id)
    _set_refresh_cookie(response, refresh)
    logger.info("User signed up: %s", user.email)
    return TokenResponse(access_token=access)


@router.post("/sign-in", response_model=TokenResponse)
def sign_in(body: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = authenticate_user(db, body.email, body.password)
    if not user:
        logger.warning("Sign-in failed: invalid credentials for %s", body.email)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access, refresh = issue_tokens(db, user.id)
    _set_refresh_cookie(response, refresh)
    logger.info("User signed in: %s", user.email)
    return TokenResponse(access_token=access)


@router.post("/token", response_model=TokenResponse)
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    old_token = request.cookies.get("refresh_token")
    if not old_token:
        logger.warning("Token refresh failed: no refresh token cookie present")
        raise HTTPException(status_code=401, detail="Refresh token not found")

    user_id, error = decode_refresh_token(old_token)
    if error or not user_id:
        logger.warning("Token refresh failed: invalid or expired refresh token")
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    result = rotate_refresh(db, old_token)
    if not result:
        logger.warning("Token refresh failed: token not found in database for user %s", user_id)
        raise HTTPException(status_code=401, detail="Refresh token revoked or expired")

    access, new_refresh = result
    _set_refresh_cookie(response, new_refresh)
    logger.info("Token refreshed successfully for user %s", user_id)
    return TokenResponse(access_token=access)


@router.get("/logout", response_model=MessageResponse)
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    if token:
        revoke_refresh(db, token)
        logger.info("User logged out from current device")
    _clear_refresh_cookie(response)
    return MessageResponse(message="Logged out")


@router.get("/logoutAll", response_model=MessageResponse)
def logout_all(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        logger.warning("LogoutAll: no refresh token cookie")
        _clear_refresh_cookie(response)
        return MessageResponse(message="Logged out from all devices")

    user_id, error = decode_refresh_token(token)
    if error or not user_id:
        logger.warning("LogoutAll: invalid or expired token")
        _clear_refresh_cookie(response)
        return MessageResponse(message="Logged out from all devices")

    count = revoke_all_user_tokens(db, user_id)
    _clear_refresh_cookie(response)
    logger.info("User %s logged out from all devices (%d sessions revoked)", user_id, count)
    return MessageResponse(message=f"Logged out from all devices ({count} sessions ended)")


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password(body: ForgotPasswordRequest, db: Session = Depends(get_db)):
    response_msg = ForgotPasswordResponse(message="If your email is registered, you will receive a reset code.")
    user = get_user_by_email(db, body.email)
    if not user:
        logger.warning("Forgot-password: email not found: %s", body.email)
        return response_msg

    code = create_reset_code(db, user.id)
    link = generate_reset_link(code)
    sent = await email_service.send_password_reset_email(
        to_email=user.email, reset_code=code, reset_link=link, user_name=user.name,
    )
    if not sent:
        logger.error("Forgot-password: failed to send email to %s", user.email)
        raise HTTPException(status_code=500, detail="Failed to send reset email")

    logger.info("Forgot-password: reset email sent to %s", user.email)
    return response_msg


@router.post("/restore-password", response_model=RestorePasswordResponse)
def restore_password(body: RestorePasswordRequest, db: Session = Depends(get_db)):
    logger.info("Restore-password attempt with code %s...", body.reset_code[:3])
    rc = validate_reset_code(db, body.reset_code)
    if not rc:
        logger.warning("Restore-password failed: invalid or expired code")
        raise HTTPException(status_code=400, detail="Invalid or expired reset code")

    user = get_user_by_id(db, rc.user_id)
    if not user:
        logger.error("Restore-password: user not found for code")
        raise HTTPException(status_code=404, detail="User not found")

    if not change_password(db, user.id, body.new_password):
        logger.error("Restore-password: failed to update password for user %s", user.email)
        raise HTTPException(status_code=500, detail="Failed to update password")

    consume_reset_code(db, rc)
    logger.info("Restore-password: password reset successfully for %s", user.email)
    return RestorePasswordResponse(message="Password has been successfully reset")
