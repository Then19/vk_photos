from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import tuple_, func

from app.databases.clickhouse.modeles.vk_photo import VkPhotoORM
from app.schemas import PaginatedList
from app.schemas.sorted_photo import SortedPhoto
from app.schemas.vk_photo import VkPhoto


def get_photo_count(db: Session, telegram_id: str) -> int:
    count = db.query(VkPhotoORM.image_id).filter(VkPhotoORM.telegram_id == telegram_id)\
        .group_by(VkPhotoORM.image_id).count()
    return count


def get_user_photo_list(
        db: Session,
        telegram_id: str,
        sort: Optional[SortedPhoto] = None,
        include_deleted: bool = False,
        date_from: Optional[datetime] = None,
        date_till: Optional[datetime] = None,
        chat_id: Optional[str] = None,
        user_name: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
) -> PaginatedList[VkPhoto]:
    filters = (
        VkPhotoORM.telegram_id == telegram_id,
        VkPhotoORM.deleted_at.is_(None) if not include_deleted else True,

        date_from <= VkPhotoORM.image_date if date_from is not None else True,
        date_till >= VkPhotoORM.image_date if date_till is not None else True,

        VkPhotoORM.chat_id == chat_id if chat_id else True,
        VkPhotoORM.user_name == user_name if user_name else True,

        tuple_(VkPhotoORM.image_id, VkPhotoORM.updated_at).in_(
            db.query(VkPhotoORM.image_id, func.max(VkPhotoORM.updated_at)).group_by(VkPhotoORM.image_id)
        )
    )

    data = db.query(VkPhotoORM)\
        .order_by(sort.get_sorted_key() if sort else VkPhotoORM.image_date.desc())\
        .filter(*filters).limit(limit).offset(offset).all()

    count = db.query(VkPhotoORM.image_id).filter(*filters).count()

    return PaginatedList(
        limit=limit,
        offset=offset,
        count=count,
        items=[
            VkPhoto.from_orm(photo)
            for photo in data
        ]
    )


def get_random_photo(db: Session, telegram_id: str) -> Optional[VkPhoto]:
    data = db.query(VkPhotoORM).order_by(func.random()).filter(
        VkPhotoORM.telegram_id == telegram_id,
        tuple_(VkPhotoORM.image_id, VkPhotoORM.updated_at).in_(
            db.query(VkPhotoORM.image_id, func.max(VkPhotoORM.updated_at)).group_by(VkPhotoORM.image_id)
        ),
        VkPhotoORM.deleted_at.is_(None)
    ).first()
    return VkPhoto.from_orm(data) if data else None
