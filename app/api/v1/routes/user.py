from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.deps import get_session, get_current_user
from app.core.security import get_password_hash
from app.helpers.send_email import SendConfirmationEmail
from app.helpers.validations import CheckFieldsExists
from app.models.user import UserModel
from app.schemas.user import UserBaseSchema, UserCreateSchema, UserUpdateSchema, UserArticleSchema, UserResponseSchema

router = APIRouter()
send_email_confirmation = SendConfirmationEmail()


@router.get("/me", response_model=UserBaseSchema)
def get_authenticated_user(current_user: UserModel = Depends(get_current_user)):
    """GET - me, rota para retornar o usuário autenticado"""
    return current_user


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
async def create_user(user: UserCreateSchema, db: AsyncSession = Depends(get_session)):
    """POST - signup, rota para criar/cadastrar um novo usuário e enviar um email de confirmação"""

    db_user: UserModel = UserModel(**user.dict())
    db_user.password = get_password_hash(db_user.password)

    # Validações
    await CheckFieldsExists.check_cpf_exists(db, db_user)
    await CheckFieldsExists.check_email_exists(db, db_user)
    await CheckFieldsExists.check_telephone_exists(db, db_user)

    async with db as session:
        session.add(db_user)
        await session.commit()

        send_email_confirmation.send_email(
            db_user.email,
            title_email="Confirmação de cadastro",
            body=f"Olá {db_user.name_complete}, seu cadastro foi realizado com sucesso!\n Faça login em nosso sistema com seu email: {db_user.email} e senha: {db_user.password}")

        return db_user


@router.get("/", response_model=List[UserBaseSchema])
async def get_users(db: AsyncSession = Depends(get_session)):
    """GET - Usuários, rota para retornar todos os usuários"""

    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserBaseSchema] = result.scalars().unique().all()

        return users


@router.get("/{user_id}", response_model=UserArticleSchema, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    """GET - Usuário, rota para retornar um usuário"""

    async with db as session:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserArticleSchema = result.scalars().unique().one_or_none()

        if user:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")


@router.put("/{user_id}", response_model=UserResponseSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id: int, user: UserUpdateSchema, db: AsyncSession = Depends(get_session)):
    """PUT - Usuário, rota para atualizar um usuário"""

    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_updt: UserUpdateSchema = result.scalars().unique().one_or_none()

        if user_updt:
            if user.name_complete:
                user_updt.name_complete = user.name_complete
            if user.date_of_birth:
                user_updt.date_of_birth = user.date_of_birth
            if user.email:
                user_updt.email = user.email
            if user.telephone:
                user_updt.telephone = user.telephone
            if user.cpf:
                user_updt.cpf = user.cpf
            if user.is_admin:
                user_updt.is_admin = user.is_admin
            if user.password:
                user_updt.password = get_password_hash(user.password)

            await session.commit()

            return user_updt
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    """DELETE - Usuário, rota para deletar um usuário"""
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_del: UserArticleSchema = result.scalars().unique().one_or_none()

        if user_del:
            await session.delete(user_del)
            await session.commit()

            return user_del
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
