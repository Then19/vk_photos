from typing import Optional
from uuid import UUID

from sqlalchemy import tuple_, func
from sqlalchemy.orm import Session

from app.databases.clickhouse.modeles.user import UserORM
from app.schemas.user import User


def get_user_by_token(db: Session, token: UUID) -> Optional[User]:
    data = db.query(UserORM).filter(
        UserORM.token == token,
        tuple_(UserORM.telegram_id, UserORM.updated_at).in_(
            db.query(UserORM.telegram_id, func.max(UserORM.updated_at)).group_by(UserORM.telegram_id)
        )
    ).first()

    return User.from_orm(data) if data else None
