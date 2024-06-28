from fastapi import HTTPException, status
from motor.motor_asyncio import (AsyncIOMotorClient, AsyncIOMotorCollection,
                                 AsyncIOMotorDatabase)

from log import logger

DB_URL = 'mongodb+srv://conectaadriano74:8gf0arvUHsUz0gmH@cluster0.ixsr3mu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'


# DB_URL = 'localhost'
# PORTA = '27017'


class BancoDados():
    def __init__(self) -> None:
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
            if not self.checar_servidor_on():
                return
            logger.error(
                f'Falha ao configurar o cliente para o MongoDB : {e}')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Falha ao configurar o cliente para o MongoDB'
            )
        return

    async def checar_servidor_on(self):
        """
        Checa se o serviço do MongoDB está acessível.
        O teste é feito através do método ping do MongoDB
        """
        try:
            await self.db.command('ping')
            logger.info('Conexão ao MongoDB bem sucedida!')
            return True
        except Exception as e:
            logger.error(
                f'Falha de REDE ao conectar ao servidor do MongoDB: {e}'
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail='Serviço do banco de dados indisponível'
            )
        return

    async def fechar_conexao(self):
        if self.client:
            self.client.close()
            logger.info('Cliente MongoDB fechado com sucesso!')
        return


"""
async def main():
    banco = BancoDados()
    await banco.conectar_banco()
    sleep(10)
    await banco.checar_servidor_on()
    sleep(10)
    await banco.fechar_conexao()

if __name__ == '__main__':
    asyncio.run(main())
"""
