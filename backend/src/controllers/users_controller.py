from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.helpers.logger import logger
from src.models.user_models import UserResponse
from src.services.users_service import get_user_by_id

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_me(request: Request, db: Session = Depends(get_db)):
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    logger.info("GET /api/users/me accessed by user %s", user_id)
    return user
