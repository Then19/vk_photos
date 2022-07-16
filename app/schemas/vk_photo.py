from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from app.schemas import BaseModel


class VkPhoto(BaseModel):
    token: UUID
    user_name: str
    image_id: UUID
    chat_id: str
    image_url: str
    image_path: Optional[str]
    image_date: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]


class VkPhotoRequest(BaseModel):
    user_name: str
    chat_id: str
    image_url: str
    image_date: datetime

    def new_photo(self, token: UUID) -> VkPhoto:
        return VkPhoto(
            token=token,
            image_id=uuid4(),
            updated_at=datetime.now().astimezone(),
            **self.dict()
        )
