from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.databases.clickhouse import get_db, crud
from app.schemas.user import User

router = APIRouter(prefix='/users')


@router.get('/user')
def get_user(
        token: UUID = Query(...),

        db: Session = Depends(get_db)
) -> Optional[User]:
    """Возвращает карточку пользователя по токену"""
    return crud.get_user_by_token(db=db, token=token)
