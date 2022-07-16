from pydantic import BaseModel


class DefaultHTTPException(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }
