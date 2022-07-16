from sqlalchemy.orm import Session

from app.databases.clickhouse.modeles.vk_photo import VkPhotoORM
from app.schemas.vk_photo import VkPhoto


def update_cards(db: Session, photos: list[VkPhoto]):
    table = VkPhotoORM.__table__
    db.execute(table.insert(), [i.dict() for i in photos])
