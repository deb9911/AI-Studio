from sqlmodel import select, Session
from passlib.hash import bcrypt
from studio.services.models import User, UserConfig

def create_user(session: Session, email: str, password: str, role: str = "user") -> User:
    hashed = bcrypt.hash(password)
    user = User(email=email, password_hash=hashed, role=role)
    session.add(user)
    session.commit()
    session.refresh(user)
    # also create empty config
    cfg = UserConfig(user_id=user.id, data={})
    session.add(cfg)
    session.commit()
    return user

def authenticate_user(session: Session, email: str, password: str) -> User | None:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        return None
    if not bcrypt.verify(password, user.password_hash):
        return None
    return user

def get_user_by_id(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)

def get_user_config(session: Session, user_id: int) -> dict:
    cfg = session.exec(select(UserConfig).where(UserConfig.user_id == user_id)).first()
    return cfg.data if cfg else {}

def set_user_config(session: Session, user_id: int, data: dict):
    cfg = session.exec(select(UserConfig).where(UserConfig.user_id == user_id)).first()
    if not cfg:
        cfg = UserConfig(user_id=user_id, data=data)
        session.add(cfg)
    else:
        cfg.data = data
    session.commit()
    session.refresh(cfg)
    return cfg.data

