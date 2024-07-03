import re
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel as SCBaseModel
from pydantic import ConfigDict, Field, field_serializer, field_validator


class ContaReceberCreateSchema(SCBaseModel):
    nome: str = Field(..., example='Nome Completo')
    cpf: Optional[str] = Field(..., example='123.456.789-00')
    telefone: str = Field(..., example='(21)91234-5678')
    valor: float = Field(..., example=1500.75)
    vencimento: datetime = Field(..., example='31/12/2024')

    @field_validator('nome', mode='before')
    def limpa_nome(cls, v):
        if isinstance(v, str):
            return re.sub(r'\s+', ' ', v).strip()

    @field_validator('telefone', mode='before')
    def limpa_telefone(cls, v):
        if isinstance(v, str):
            # Remove todos os caracteres que não seja digitos 0-9
            return re.sub(r'\D', '', v)

    @field_validator('cpf', mode='before')
    def limpa_cpf(cls, v):
        if isinstance(v, str):
            # Remove todos os caracteres que não seja digitos 0-9
            return re.sub(r'\D', '', v)

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
    nome: str = Field(..., example='Nome Completo')
    cpf: Optional[str] = Field(..., example='123.456.789-00')
    telefone: str = Field(..., example='(21)91234-5678')
    valor: float = Field(..., example=1500.75)
    vencimento: datetime = Field(..., example='31/12/2024')
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
    nome: str = Field(..., example='Nome Completo')
    cpf: Optional[str] = Field(..., example='123.456.789-00')
    telefone: str = Field(..., example='(21)91234-5678')
    valor: float = Field(..., example=1500.75)
    vencimento: datetime = Field(..., example='31/12/2024')

    @field_validator('nome', mode='before')
    def limpa_nome(cls, v):
        if isinstance(v, str):
            return re.sub(r'\s+', ' ', v).strip()

    @field_validator('cpf', mode='before')
    def limpa_cpf(cls, v):
        if isinstance(v, str):
            # Remove todos os caracteres que não seja digitos 0-9
            return re.sub(r'\D', '', v)

    @field_validator('telefone', mode='before')
    def limpa_telefone(cls, v):
        if isinstance(v, str):
            # Remove todos os caracteres que não seja digitos 0-9
            return re.sub(r'\D', '', v)

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

    model_config = ConfigDict(
        from_attributes=True,
    )
