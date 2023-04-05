from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import UserModel
from app.schemas.user import UserBaseSchema


class CheckFieldsExists:

    @staticmethod
    async def check_cpf_exists(db: AsyncSession, user: UserBaseSchema):
        async with db as session:
            query = select(UserModel).where(UserModel.cpf == user.cpf)
            result = await session.execute(query)

            if result.scalars().unique().all():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CPF já cadastrado")

    @staticmethod
    async def check_email_exists(db: AsyncSession, user: UserBaseSchema):
        async with db as session:
            query = select(UserModel).where(UserModel.email == user.email)
            result = await session.execute(query)

            if result.scalars().unique().all():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")

    @staticmethod
    async def check_telephone_exists(db: AsyncSession, user: UserBaseSchema):
        async with db as session:
            query = select(UserModel).where(UserModel.telephone == user.telephone)
            result = await session.execute(query)

            if result.scalars().unique().all():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Telefone já cadastrado")
