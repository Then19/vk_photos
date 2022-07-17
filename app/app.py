from fastapi import FastAPI, Depends
from app.routers import photos, users
from clickhouse_driver import connect
from app.settings import settings


app = FastAPI(
    title="VkPhotoAPI",
    version='0.0.1'
)

app.include_router(photos.router, tags=['Photos'])
app.include_router(users.router, tags=['Users'])


@app.on_event("startup")
def startup_event():
    conn = connect(settings.clickhouse_dsn)
    cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS vk_photos (
            telegram_id String NOT NULL,
            user_name String NOT NULL,
            image_id UUID NOT NULL,
            chat_id String NOT NULL,
            chat_name Nullable(String),
            image_url String NOT NULL,
            image_path Nullable(String),
            image_date DateTime64(6, 'UTC') NOT NULL,
            updated_at DateTime64(6, 'UTC') NOT NULL,
            deleted_at Nullable(DateTime64(6, 'UTC')))
            ENGINE=ReplacingMergeTree(updated_at) ORDER BY (telegram_id, image_url)"""
    )

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        telegram_id String NOT NULL,
        user_name String NOT NULL,
        token UUID NOT NULL,
        limit UInt32 NOT NULL,
        refs_count UInt32 NOT NULL,
        blocked_at Nullable(DateTime64(6, 'UTC')),
        updated_at DateTime64(6, 'UTC') NOT NULL)
        ENGINE=MergeTree() ORDER BY (telegram_id, user_name, limit, refs_count) PRIMARY KEY telegram_id""")

    # cursor.execute("""DROP TABLE users""")
    # cursor.execute("""DROP TABLE vk_photos""")
