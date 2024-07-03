from fastapi import APIRouter

from api.v1.endpoints import conta_receber_router

api_router = APIRouter()
api_router.include_router(
    conta_receber_router.router,
    prefix='/contas/receber',
    tags=['Controle de Contas a Receber']
)
