from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, validator

from app.schemas.article import ArticleBaseSchema

"""
 É criado alguns schemas para o usuário, devido ao retorno das informações,
 se for para retornar as informações do usuário criado ou atualizado, a senha não deve ser retornada,
 por isso é criado um schema para cada situação.
"""


class UserBaseSchema(BaseModel):
    """Schema base para o usuário, este schema é herdado por outros schemas"""
    name_complete: str
    date_of_birth: date
    email: EmailStr
    telephone: str
    cpf: str
    is_admin: bool = False

    class Config:
        orm_mode = True

    @validator("name_complete")
    def name_complete_must_have_3_characters(cls, value):
        if len(value) < 3:
            raise ValueError("Nome completo deve ter no mínimo 3 caracteres")
        return value.capitalize()

    @validator("cpf")
    def cpf_must_have_11_digits(cls, value):
        if len(value) != 11:
            raise ValueError("CPF deve ter 11 dígitos")
        return value

    @validator("email")
    def email_should_be_valid(cls, value):
        if "@" not in value:
            raise ValueError("E-mail inválido")
        return value


class UserCreateSchema(UserBaseSchema):
    """Herda do UserBaseSchema, este schema é para retornar
    uma informação específica que é a senha"""

    password: str


class UserArticleSchema(UserBaseSchema):
    """Este schema retora um usuário e os artigos que ele criou,
    caso seja chamado o usuário, os artigos serão retornados"""

    articles: Optional[List[ArticleBaseSchema]]


class UserUpdateSchema(UserBaseSchema):
    """Schema para atualizar o usuário, as informações de editar cadastro são Opcionais
    pois o usuário pode não querer atualizar todas as informações"""

    name_complete: Optional[str]
    date_of_birth: Optional[date]
    email: Optional[EmailStr]
    telephone: Optional[str]
    cpf: Optional[str]
    password: Optional[str]
    is_admin: Optional[bool]


class UserResponseSchema(UserBaseSchema):
    """Schema para retornar a mensagem de sucesso ou erro"""
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    send_email = "Olá seu cadastro foi realizado com sucesso, enviaremos um e-mail de confirmação"

    class Config:
        orm_mode = True
