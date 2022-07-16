from sqlalchemy import Column
from clickhouse_sqlalchemy.types import DateTime64, UUID, String, Nullable
from app.databases.clickhouse import Base


class VkPhotoORM(Base):
    __tablename__ = "vk_photos"

    token = Column(UUID)
    user_name = Column(String)
    image_id = Column(UUID, primary_key=True)
    chat_id = Column(String)
    image_url = Column(String)
    image_path = Column(Nullable(String))
    image_date = Column(DateTime64(6, 'UTC'))
    updated_at = Column(DateTime64(6, 'UTC'))
    deleted_at = Column(Nullable(DateTime64(6, 'UTC')))

    def __repr__(self):
        return "<VkPhoto(image_id: %s)>" % (self.image_id,)