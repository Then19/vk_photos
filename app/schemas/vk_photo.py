from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import validator

from app.schemas import BaseModel


class VkPhoto(BaseModel):
    telegram_id: int
    user_name: str
    image_id: UUID
    chat_id: int
    chat_name: str
    image_url: str
    image_path: Optional[str]
    image_date: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]


class VkPhotoRequest(BaseModel):
    user_name: str
    chat_id: int
    image_url: str
    chat_name: str
    image_date: datetime

    @validator('image_url')
    def name_must_contain_space(cls, v: str):
        if not v.startswith('https://sun9'):
            raise ValueError('bad url')
        return v

    def new_photo(self, telegram_id: int) -> VkPhoto:
        return VkPhoto(
            telegram_id=telegram_id,
            image_id=uuid4(),
            updated_at=datetime.now().astimezone(),
            **self.dict()
        )
