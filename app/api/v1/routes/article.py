from typing import List, Dict

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.deps import get_current_user, get_session
from app.models.article import ArticleModel
from app.models.user import UserModel
from app.schemas.article import ArticleBaseSchema, ArticleCreateSchema, ArticleResponseSchema, ArticleUpdateSchema

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ArticleResponseSchema)
async def create_article(article: ArticleCreateSchema, current_user: UserModel = Depends(get_current_user),
                         db: AsyncSession = Depends(get_session)):
    """POST - Artigo, criar um artigo para o usuário logado"""
    new_article: ArticleModel = ArticleModel(title=article.title,
                                             description=article.description,
                                             url_font=article.url_font,
                                             user_id=current_user.id)

    db.add(new_article)
    await db.commit()

    return new_article


@router.get("/", response_model=List[ArticleResponseSchema])
async def get_articles(db: AsyncSession = Depends(get_session)):
    """GET - Artigo, retorna todos os artigos"""
    async with db as session:
        query = select(ArticleModel)
        result = await session.execute(query)
        articles: List[ArticleModel] = result.scalars().unique().all()

        return articles


@router.get("/{article_id}", response_model=ArticleResponseSchema, status_code=status.HTTP_200_OK)
async def get_article(article_id: int, db: AsyncSession = Depends(get_session)):
    """GET - Artigo, retorna um artigo pelo id"""
    async with db as session:
        query = select(ArticleModel).where(ArticleModel.id == article_id)
        result = await session.execute(query)
        article: ArticleModel = result.scalars().unique().one()

        if article:
            return article
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado")


@router.put("/{article_id}", response_model=ArticleResponseSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_article(article_id: int, article: ArticleUpdateSchema,
                         current_user: UserModel = Depends(get_current_user),
                         db: AsyncSession = Depends(get_session)):
    """PUT - Artigo, atualiza um artigo pelo id, somente os usuários(autenticados) logados podem atualizar seus artigos"""

    async with db as session:
        query = select(ArticleModel).where(ArticleModel.id == article_id).filter(
            ArticleModel.user_id == current_user.id)
        result = await session.execute(query)
        article_updt: ArticleModel = result.scalars().unique().one()

        if article_updt:
            if article.title:
                article_updt.title = article.title
            if article.description:
                article_updt.description = article.description
            if article.url_font:
                article_updt.url_font = article.url_font
            if current_user.id == article_updt.user_id:
                article_updt.user_id = current_user.id

            await session.commit()

            return article_updt
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado")


@router.delete("/{article_id}")
async def delete_article(article_id: int, db: AsyncSession = Depends(get_session),
                         current_user: UserModel = Depends(get_current_user)):
    """DELETE - Artigo, deleta um artigo pelo id, somente os usuários(autenticados) logados podem deletar seus artigos"""

    # Dois filtros para garantir que o usuário logado só possa deletar seus artigos
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == article_id).filter(
            ArticleModel.user_id == current_user.id)
        result = await session.execute(query)
        article_del: ArticleModel = result.scalars().unique().one_or_none()

        if article_del:
            await session.delete(article_del)
            await session.commit()

            return article_del
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado")
