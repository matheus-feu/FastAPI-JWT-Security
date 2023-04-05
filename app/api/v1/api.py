from app.api.v1.routes import auth, user, article, status
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(status.router, prefix="/status", tags=["Status"])
api_router.include_router(user.router, prefix="/usuarios", tags=["Usuários"])
api_router.include_router(article.router, prefix="/artigos", tags=["Artigos"])
