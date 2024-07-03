from core.database import BancoDados


async def get_db() -> BancoDados:
    db = BancoDados()
    await db.conectar_banco()
    try:
        yield db
    finally:
        await db.desconectar_banco()
