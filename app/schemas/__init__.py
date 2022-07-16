import humps
import pydantic
from typing import TypeVar, Generic, List
from pydantic.generics import GenericModel

T = TypeVar('T')


class PaginatedList(GenericModel, Generic[T]):
    offset: int
    limit: int
    count: int
    items: List[T]


class BaseModel(pydantic.BaseModel):
    class Config:
        orm_mode = True
        alias_generator = humps.camelize
        allow_population_by_field_name = True
