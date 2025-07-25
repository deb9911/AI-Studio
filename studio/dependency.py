from fastapi import Depends, Request, HTTPException

from fastapi import Depends, Request, HTTPException
from sqlmodel import Session
from studio.services.db import get_session
from studio.services.crud import get_user_by_id


def get_current_user(
    request: Request,
    session: Session = Depends(get_session)
):
    uid = request.session.get("user_id")
    if not uid:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = get_user_by_id(session, uid)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
