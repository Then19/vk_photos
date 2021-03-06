from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.databases.clickhouse import crud, get_db
from app.exceptions.default import DefaultHTTPException
from app.routers.users import get_user
from app.schemas import PaginatedList
from app.schemas.sorted_photo import SortedPhoto
from app.schemas.vk_photo import VkPhotoRequest, VkPhoto

router = APIRouter(prefix='/photo')


@router.post(
    '/new',
    responses={
        403: {'model': DefaultHTTPException, 'description': "Пользователь не зарегистрирован"},
        405: {'model': DefaultHTTPException, 'description': "Пользователь заблокирован"},
        410: {'model': DefaultHTTPException, 'description': "Превышен лимит фотографий"}
    }
)
def add_new_photos(
        photos: list[VkPhotoRequest],
        token: UUID = Query(...),

        db: Session = Depends(get_db)
) -> UUID:
    """Добавить новые фотографии"""
    user = get_user(token=token, db=db)

    count_photos = crud.get_photo_count(db=db, telegram_id=user.telegram_id)
    if user.limit - len(photos) < count_photos:
        raise HTTPException(410, detail=f"Превышен лимит фотографий, доступно: {user.limit - count_photos}")

    crud.update_cards(db, [photo.new_photo(user.telegram_id) for photo in photos])
    return token


@router.get(
    '/random',
    response_model=VkPhoto,
    responses={
        403: {'model': DefaultHTTPException, 'description': "Пользователь не зарегистрирован"},
        405: {'model': DefaultHTTPException, 'description': "Пользователь заблокирован"},
        404: {'model': DefaultHTTPException, 'description': "Фото по таким параметрам не найдено"},
    }
)
def get_random_photo(
        token: UUID = Query(...),
        ignore_groups: bool = Query(False, alias="ignoreGroups"),

        db: Session = Depends(get_db)
) -> VkPhoto:
    """Возвращает случайную фотографию пользователя"""
    user = get_user(token=token, db=db)

    photo = crud.get_random_photo(db=db, telegram_id=user.telegram_id, ignore_groups=ignore_groups)
    if not photo:
        raise HTTPException(404, detail="Фото по таким параметрам не найдено")

    return photo


@router.get(
    '/photos', response_model=PaginatedList[VkPhoto],
    responses={
        403: {'model': DefaultHTTPException, 'description': "Пользователь не зарегистрирован"},
        405: {'model': DefaultHTTPException, 'description': "Пользователь заблокирован"}
    }
)
def get_user_photos(
        token: UUID = Query(...),
        sort: Optional[SortedPhoto] = Query(None),
        include_deleted: Optional[bool] = Query(False, alias="includeDeleted"),
        date_from: Optional[datetime] = Query(None, alias="dateFrom"),
        date_till: Optional[datetime] = Query(None, alias="dateTill"),
        chat_id: Optional[int] = Query(None, alias="chatId"),
        user_name: Optional[str] = Query(None, alias="userName"),
        limit: int = 50,
        offset: int = 0,

        db: Session = Depends(get_db)
) -> PaginatedList[VkPhoto]:
    """Возвращает фото с пагинацией"""
    user = get_user(token=token, db=db)
    return crud.get_user_photo_list(
        db=db,
        telegram_id=user.telegram_id,
        sort=sort,
        include_deleted=include_deleted,
        date_from=date_from,
        date_till=date_till,
        chat_id=chat_id,
        user_name=user_name,
        limit=limit,
        offset=offset
    )
