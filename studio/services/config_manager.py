from pathlib import Path
import json
from sqlmodel import Session

from studio.services.crud import get_user_config, set_user_config

DEFAULT_CFG = json.loads(Path("config_default.json").read_text())

def load_user_config_db(session: Session, user_id: int, default: dict) -> dict:
    cfg = get_user_config(session, user_id)
    return {**default, **cfg}

def save_user_config_db(session: Session, user_id: int, data: dict) -> dict:
    return set_user_config(session, user_id, data)

