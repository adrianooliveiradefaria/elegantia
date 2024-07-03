from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('ObjectId inválido!')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, handler):
        schema.update(type='string')
        return schema


class ContaReceberModel(BaseModel):
    id: Optional[PyObjectId] = Field(
        default_factory=PyObjectId,
        alias='_id'
    )
    nome: str
    cpf: Optional[str]
    telefone: str
    valor: float
    vencimento: datetime
    cadastro: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={
            ObjectId: str,
            datetime: lambda dt: dt.strftime('%d/%m/%Y')
        }
    )
