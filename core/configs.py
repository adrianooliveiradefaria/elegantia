from pydantic import BaseModel


class Settings(BaseModel):
    """
    Configurações gerais da aplicação
    """

    API_V1: str = '/api/v1'

    class Config:
        case_sensitive = True


settings = Settings()
