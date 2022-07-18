from uuid import UUID

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from app.databases.clickhouse import get_db, crud
from app.exceptions.default import DefaultHTTPException
from app.schemas.user import User

router = APIRouter(prefix='/users')


@router.get(
    '/user', response_model=User,
    responses={
        403: {'model': DefaultHTTPException, 'description': "Пользователь не зарегистрирован"},
        405: {'model': DefaultHTTPException, 'description': "Пользователь заблокирован"}
    }
)
def get_user(
        token: UUID = Query(...),

        db: Session = Depends(get_db)
) -> User:
    """Возвращает карточку пользователя по токену"""
    user = crud.get_user_by_token(db=db, token=token)

    if not user:
        raise HTTPException(403, detail='Пользователь с таким токен не найден')

    if user.blocked_at:
        raise HTTPException(405, detail="Пользователь заблокирован")

    return user
