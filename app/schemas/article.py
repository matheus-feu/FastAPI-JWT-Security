from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, validator


class ArticleBaseSchema(BaseModel):
    title: str
    description: str
    url_font: HttpUrl

    class Config:
        orm_mode = True

    @validator("title")
    def title_must_have_3_characters(cls, value):
        if len(value) < 3:
            raise ValueError("Título deve ter no mínimo 3 caracteres")
        return value

    @validator("description")
    def description_must_have_3_characters(cls, value):
        if len(value) < 3:
            raise ValueError("Descrição deve ter no mínimo 3 caracteres")
        return value


class ArticleCreateSchema(ArticleBaseSchema):
    pass


class ArticleUpdateSchema(ArticleBaseSchema):
    pass


class ArticleResponseSchema(ArticleBaseSchema):
    id: int
    title: str
    description: str
    url_font: HttpUrl
    user_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
