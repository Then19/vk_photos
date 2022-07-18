from sqlalchemy import Column
from clickhouse_sqlalchemy.types import DateTime64, UUID, String, Nullable, UInt32
from app.databases.clickhouse import Base


class UserORM(Base):
    __tablename__ = "users"

    telegram_id = Column(String, primary_key=True)
    user_name = Column(String)
    token = Column(UUID)
    limit = Column(UInt32)
    refs_count = Column(UInt32)
    blocked_at = Column(Nullable(DateTime64(6, 'UTC')))
    created_at = Column(DateTime64(6, 'UTC'))
    updated_at = Column(DateTime64(6, 'UTC'))

    def __repr__(self):
        return "<User(telegram_id: %s)>" % (self.image_id,)
