from uuid import UUID

from sqlalchemy.orm import Session

from app.databases.clickhouse.modeles.vk_photo import VkPhotoORM


def get_photo_count(db: Session, token: UUID) -> int:
    count = db.query(VkPhotoORM).filter(VkPhotoORM.token == token).group_by(VkPhotoORM.image_id).count()
    return count
