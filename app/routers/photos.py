from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.databases.clickhouse import crud, get_db
from app.exceptions.default import DefaultHTTPException
from app.routers.users import get_user
from app.schemas.vk_photo import VkPhotoRequest

router = APIRouter(prefix='/photo')


@router.post(
    '/new/{token}',
    responses={
        403: {'model': DefaultHTTPException, 'description': "Пользователь не зарегистрирован"},
        405: {'model': DefaultHTTPException, 'description': "Пользователь заблокирован"},
        410: {'model': DefaultHTTPException, 'description': "Превышен лимит фотографий"}
    }
)
def add_new_photos(
        token: UUID,
        photos: list[VkPhotoRequest],

        db: Session = Depends(get_db)
) -> UUID:
    """Добавить новые фотографии"""
    user = get_user(token=token, db=db)
    if not user:
        raise HTTPException(403, detail='Пользователь с таким токен не найден')

    if user.blocked_at:
        raise HTTPException(405, detail="Пользователь заблокирован")

    count_photos = crud.get_photo_count(db, token)
    if user.limit - len(photos) < count_photos:
        raise HTTPException(410, detail=f"Превышен лимит фотографий, доступно: {user.limit - count_photos}")

    crud.update_cards(db, [photo.new_photo(token) for photo in photos])
    return token
