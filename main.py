import locale

import uvicorn
from fastapi import FastAPI

from api.v1.api import api_router
from core.configs import settings

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

app = FastAPI(
    title='Elegantia Moda',
    description='Além de gerenciamento empresarial total do negócio, esta API embarca automatização de processos (RPA), IA para atendimento e tomada de decisão e provê informações para bots de atendimento.',
    summary='Controle empresarial',
    version='0.1.0'
)
app.include_router(api_router, prefix=settings.API_V1)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_level='info',
        reload=True
    )
