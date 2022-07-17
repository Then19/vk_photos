from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from app.schemas import BaseModel


class VkPhoto(BaseModel):
    telegram_id: UUID
    user_name: str
    image_id: UUID
    chat_id: str
    chat_name: Optional[str]
    image_url: str
    image_path: Optional[str]
    image_date: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]


class VkPhotoRequest(BaseModel):
    user_name: str
    chat_id: str
    image_url: str
    chat_name: Optional[str]
    image_date: datetime

    def new_photo(self, telegram_id: str) -> VkPhoto:
        return VkPhoto(
            telegram_id=telegram_id,
            image_id=uuid4(),
            updated_at=datetime.now().astimezone(),
            **self.dict()
        )
