from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel as SCBaseModel
from pydantic import ConfigDict, Field, field_serializer, field_validator


class ContaReceberCreateSchema(SCBaseModel):
    nome: str = Field(..., example='João da Silva')
    cpf: Optional[str] = Field(..., example='123.456.789-00')
    telefone: str = Field(..., example='(21) 91234-5678')
    valor: float = Field(..., example=1500.75)
    vencimento: datetime = Field(..., example='31/12/2024')

    @field_validator('vencimento', mode='before')
    def convert_date_to_datetime(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%d/%m/%Y')
            except ValueError:
                raise ValueError('Formato de data inválido! Use DD/MM/AAAA')
        if isinstance(v, date) and not isinstance(v, datetime):
            return datetime(v.year, v.month, v.day)
        return v


class ContaReceberResponseSchema(SCBaseModel):
    id: str
    nome: str
    cpf: Optional[str]
    telefone: str
    valor: float
    vencimento: datetime
    cadastro: datetime

    @field_validator('vencimento', 'cadastro', mode='before')
    def convert_date_to_datetime(cls, v):
        if isinstance(v, date) and not isinstance(v, datetime):
            return datetime(v.year, v.month, v.day)
        return v

    @field_serializer('vencimento')
    def serialize_vencimento(self, v):
        return v.strftime('%d/%m/%Y')

    @field_serializer('cadastro')
    def serialize_cadastro(self, v):
        return v.strftime('%d/%m/%Y %H:%M:%S')

    model_config = ConfigDict(
        from_attributes=True,
    )


class ContaReceberUpdateSchema(SCBaseModel):
    id: str = Field(frozen=True, exclude=True)
    nome: str = Field(..., example='João da Silva')
    cpf: Optional[str] = Field(..., example='123.456.789-00')
    telefone: str = Field(..., example='(21) 91234-5678')
    valor: float = Field(..., example=1500.75)
    vencimento: datetime = Field(..., example='31/12/2024')

    @field_validator('vencimento', mode='before')
    def convert_date_to_datetime(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%d/%m/%Y')
            except ValueError:
                raise ValueError('Formato de data inválido! Use DD/MM/AAAA')
        if isinstance(v, date) and not isinstance(v, datetime):
            return datetime(v.year, v.month, v.day)
        return v

    @field_serializer('vencimento')
    def serialize_vencimento(self, v):
        return v.strftime('%d/%m/%Y')

    model_config = ConfigDict(
        from_attributes=True,
    )
