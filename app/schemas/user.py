from datetime import datetime
from uuid import UUID

from app.schemas import BaseModel


class User(BaseModel):
    telegram_id: str
    user_name: str
    token: UUID
    limit: int
    refs_count: int
    blocked_at: datetime
    updated_at: datetime
