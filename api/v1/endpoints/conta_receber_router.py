from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Response, status

from core.database import BancoDados
from core.deps import get_db
from core.log import logger
from core.utils import normalizacao
from models.conta_receber_model import PyObjectId
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
    description='Lista ordenada por "nome" em ordem de alfabética',
    summary='Lista o cadastro de Contas a Receber',
    response_description='Contas a Receber listadas com sucesso!'
)
async def read_contas_receber(
    db: BancoDados = Depends(get_db)
):
    lista_contas_receber = await db.collection.find().sort('nome', 1).to_list(length=None)
    # Convertendo ObjectId para string
    for conta in lista_contas_receber:
        conta['id'] = str(conta['_id'])
        del conta['_id']

    return lista_contas_receber


@router.get(
    '/{id_conta}',
    status_code=status.HTTP_200_OK,
    response_model=ContaReceberResponseSchema,
    description='Retorna o cadastro de uma Conta a Receber',
    summary='Busca Conta a Receber',
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
    description='Atualiza o cadastro de uma Conta a Receber pelo ID',
    summary='Atualiza Conta a Receber',
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
    description='Deleta o cadastro de uma Conta a Receber',
    summary='Deleta uma Conta a Receber',
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
        logger.info(f'Conta a Receber ID: {id_conta} deletada com sucesso!')
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f'Erro ao deletar conta a receber: {e}'
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    '/drop',
    status_code=status.HTTP_204_NO_CONTENT,
    description='Deleta todos os documentos da coleção',
    summary='Deleta todo o cadastro',
    response_description='Coleção sem Documentos'
)
async def delete_all_contas_receber(
    db: BancoDados = Depends(get_db)
):
    try:
        zera_colecao = await db.collection.delete_many({})
        logger.info(f'Coleção zerada com sucesso!')
    except Exception as e:
        logger.error(f'Erro ao zerar Collection: {e}')
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
