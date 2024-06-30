from fastapi import HTTPException, status
from motor.motor_asyncio import (AsyncIOMotorClient, AsyncIOMotorCollection,
                                 AsyncIOMotorDatabase)

from core.log import logger

DB_URL = 'mongodb+srv://conectaadriano74:8gf0arvUHsUz0gmH@cluster0.ixsr3mu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'


# DB_URL = 'localhost'
# PORTA = '27017'


class BancoDados():
    def __init__(self) -> None:
        """
        Cria automaticamente o banco e a collection se não existirem
        """
        self.client: AsyncIOMotorClient = None
        self.db: AsyncIOMotorDatabase = None
        self.collection: AsyncIOMotorCollection = None

    async def conectar_banco(self):
        """
        Abre uma conexão com o servidor MongoDB, seleciona o banco de dados e coleção
        """
        try:
            self.client = AsyncIOMotorClient(DB_URL)
            # client = AsyncIOMotorClient(f'mongodb://{DB_URL}:{PORTA}')
            self.db = self.client.elegantiaDB
            self.collection = self.db.receber
            logger.info('Conexão com o MongoDB estabelecida!')
        except Exception as e:
            logger.error(
                f'Falha ao configurar o cliente para o MongoDB : {e}')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Falha ao configurar o cliente para o MongoDB'
            )
        return

    async def desconectar_banco(self):
        if self.client:
            self.client.close()
            logger.info('Cliente MongoDB fechado com sucesso!')
        return
