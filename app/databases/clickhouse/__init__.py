from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session
from clickhouse_sqlalchemy import get_declarative_base, make_session

from app.settings import settings


engine = create_engine(settings.clickhouse_dsn.replace('clickhouse://', 'clickhouse+native://'), pool_recycle=3600)
metadata = MetaData(bind=engine)
Base = get_declarative_base(metadata=metadata)


def get_db() -> Session:
    session = make_session(engine)
    try:
        yield session
    finally:
        session.close()
