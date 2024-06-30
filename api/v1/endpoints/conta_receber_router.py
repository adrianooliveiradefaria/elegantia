from datetime import datetime
from typing import Any, Dict, List, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Response, status

from core.database import BancoDados
from core.deps import get_db
from core.log import logger
from core.utils import normalizacao
from models.conta_receber_model import ContaReceberModel, PyObjectId
from schemas.conta_receber_schema import (ContaReceberCreateSchema,
                                          ContaReceberResponseSchema,
                                          ContaReceberUpdateSchema)

router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=ContaReceberCreateSchema,
    description='Cadastra uma Conta a Receber ao banco de dados',
    summary='Nova Conta a Receber',
    response_description='Conta a Receber cadastrada com sucesso!'
)
async def create_conta_receber(
    conta_receber: ContaReceberCreateSchema,
    db: BancoDados = Depends(get_db)
):
    conta_receber_dict = conta_receber.model_dump()

    try:
        # Insere o campo obrigatório do modelo com o valor esperado
        conta_receber_dict['cadastro'] = datetime.now()
        resultado = await db.collection.insert_one(conta_receber_dict)
        conta_receber_dict['id'] = str(resultado.inserted_id)
        del conta_receber_dict['_id']
        logger.info('Cadastro de conta a receber efeuado com sucesso!')
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f'Erro ao cadastrar conta a receber: {e}'
        )

    return conta_receber_dict


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[ContaReceberResponseSchema],
    description='Lista todas as Contas a Receber',
    summary='Lista de Contas a Receber',
    response_description='Contas a Receber listadas com sucesso!'
)
async def read_contas_receber(
    db: BancoDados = Depends(get_db)
):
    list_contas_receber = await db.collection.find().to_list(length=None)
    # Convertendo ObjectId para string
    for conta in list_contas_receber:
        conta['id'] = str(conta['_id'])
        del conta['_id']

    return list_contas_receber


@router.get(
    '/{id_conta}',
    status_code=status.HTTP_200_OK,
    response_model=ContaReceberResponseSchema,
    description='Retorna uma Conta a Receber',
    summary='Retorna Conta pelo ID',
    response_description='Conta a Receber encontrada.'
)
async def read_conta_receber_id(
    id_conta: str,
    db: BancoDados = Depends(get_db)
):
    if not ObjectId.is_valid(id_conta):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='ID inválido!'
        )

    conta_receber = await db.collection.find_one({'_id': ObjectId(id_conta)})

    if not conta_receber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Conta a Receber não encontrada!'
        )

    return normalizacao.id_documento(conta_receber)


@router.put(
    '/{id_conta}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ContaReceberUpdateSchema,
    description='Atualiza uma Conta a Receber',
    summary='Parâmetro de atualização ID',
    response_description='Conta a Receber atualizada com sucesso!'
)
async def update_conta_receber(
    id_conta: str,
    conta_receber: ContaReceberUpdateSchema,
    db: BancoDados = Depends(get_db)
):
    if not ObjectId.is_valid(id_conta):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='ID inválido!'
        )

    conta_receber_busca = await db.collection.find_one({'_id': ObjectId(id_conta)})

    if not conta_receber_busca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Conta a Receber não encontrada!'
        )

    conta_receber_dict = conta_receber.model_dump()

    # Remove o campo 'id' se presente
    conta_receber_dict.pop('id', None)

    try:
        resultado = await db.collection.update_one(
            {'_id': ObjectId(id_conta)},
            {'$set': conta_receber_dict}
        )

        # Adiciona o campo 'id' no dicionário de resposta
        conta_receber_dict['id'] = str(id_conta)
        logger.info('Atualização efetuada com sucesso!')
    except Exception as e:
        error_code = getattr(e, 'code', None)
        if error_code == 304:
            logger.warning(
                f'Nenhuma modificação feita na Conta a Receber ID: {id_conta}'
            )
            raise HTTPException(
                status_code=status.HTTP_304_NOT_MODIFIED,
                detail='Dados não modificados.'
            )
        elif error_code in (501,):
            logger.error(f'Erro ao atualizar Conta a Receber {id_conta}: {e}')
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail=f'Erro ao atualizar Conta a Receber: {e}'
            )
        else:
            logger.error(f'Erro ao atualizar Conta a Receber: {e}')

    return conta_receber_dict


@router.delete(
    '/{id_conta}',
    status_code=status.HTTP_204_NO_CONTENT,
    description='Deleta uma Conta a Receber',
    summary='Deleta Conta pelo ID',
    response_description='Conta a Receber deletada com sucesso!'
)
async def delete_conta_receber(
    id_conta: str,
    db: BancoDados = Depends(get_db)
):
    if not ObjectId.is_valid(id_conta):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='ID inválido!'
        )

    conta_receber_busca = await db.collection.find_one({'_id': ObjectId(id_conta)})

    if not conta_receber_busca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Conta a Receber não encontrada!'
        )

    try:
        resultado = await db.collection.delete_one({'_id': ObjectId(id_conta)})
        if resultado.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Conta a Receber não encontrada!'
            )
        logger.info('Conta a Receber deletada com sucesso!')
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f'Erro ao deletar conta a receber: {e}'
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
