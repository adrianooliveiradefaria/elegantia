import json
import logging

import httpx
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)


class PostWebhookMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print('################### Estou na IDA ########################')
        print(f'URL API: {request.url.path}')
        response = await call_next(request)
        if request.method == "POST" and request.url.path == "/api/v1/contas/receber/":
            response_body = b"".join([chunk async for chunk in response.body_iterator])
            response_body_json = json.loads(response_body.decode("utf-8"))
            await self.send_to_webhook(response_body_json)
            response = Response(
                response_body, status_code=response.status_code, headers=dict(response.headers))
        return response

    async def send_to_webhook(self, data):
        webhook_url = "http://conectasolucoes.dyndns.org:5678/webhook-test/elegantia"
        async with httpx.AsyncClient() as client:
            try:
                if 'cadastro' in data:
                    data['cadastro'] = data['cadastro']
                response = await client.post(webhook_url, json=data)
                response.raise_for_status()
                logger.info('Dados enviados ao webhook com sucesso!')
            except httpx.HTTPStatusError as exc:
                logger.error(f"Erro ao enviar dados ao webhook: {
                             exc.response.status_code} - {exc.response.text}")
            except Exception as exc:
                logger.error(
                    f"Erro inesperado ao enviar dados ao webhook: {exc}")
