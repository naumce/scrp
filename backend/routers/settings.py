from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from db.database import get_session
from db.models import Setting
from schemas.base import ok
from services.settings_service import DEFAULTS, get_all_settings

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("")
def get_settings():
    return ok(get_all_settings())


@router.put("")
def update_settings(
    data: dict,
    session: Session = Depends(get_session),
):
    for key, value in data.items():
        if key not in DEFAULTS:
            continue
        existing = session.get(Setting, key)
        if existing:
            existing.value = str(value)
            session.add(existing)
        else:
            session.add(Setting(key=key, value=str(value)))
    session.commit()
    return ok(get_all_settings())
