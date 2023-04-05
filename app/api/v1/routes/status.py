from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.core.settings import settings
from app.models.user import UserModel

router = APIRouter()


@router.get("/status")
async def status(current_user: UserModel = Depends(get_current_user)):
    """GET - Status, rota para verificar se a API está rodando"""
    if current_user:
        return {"sucess": True,
                "version": settings.app_version,
                "user": current_user.email,
                "status": "API is running",
                "message": "Welcome to the API"}
