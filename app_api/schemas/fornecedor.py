from pydantic import BaseModel
from typing import Optional, List
from model.fornecedor import Fornecedor

from schemas import CategoriaSchema


class FornecedorSchema(BaseModel):
    """ Define como um novo fornecedor a ser inserido deve ser representado
    """
    nome: str = "Deposito Bebidas Brasil"
    descricao: str = "Deposito de bebidas em geral"


class FornecedorBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do fornecedor.
    """
    nome: str = "Teste"


class ListagemFornecedoresSchema(BaseModel):
    """ Define como uma listagem de fornecedor será retornada.
    """
    fornecedor:List[FornecedorSchema]


def apresenta_fornecedores(fornecedores: List[Fornecedor]):
    """ Retorna uma representação do fornecedor seguindo o schema definido em
        FornecedorViewSchema.
    """
    result = []
    for fornecedor in fornecedores:
        result.append({
            "nome": fornecedor.nome,
            "descricao": fornecedor.descricao
        })

    return {"fornecedor": result}


class FornecedorViewSchema(BaseModel):
    """ Define como um fornecedor será retornado: fornecedor + categorias.
    """
    id: int = 1
    nome: str = "Deposito Bebidas Brasil"
    descricao: str = "Deposito especializado em bebidas"
    total_categorias: int = 1
    categorias:List[CategoriaSchema]


class FornecedorDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_fornecedor(fornecedor: Fornecedor):
    """ Retorna uma representação do fornecedor seguindo o schema definido em
        FornecedorViewSchema.
    """
    return {
        "id": fornecedor.id,
        "nome": fornecedor.nome,
        "descricao": fornecedor.descricao,
        "total_categoriass": len(fornecedor.categorias),
        "categorias": [{"texto": c.texto} for c in fornecedor.categorias]
    }
