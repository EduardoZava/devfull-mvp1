from pydantic import BaseModel


class CategoriaSchema(BaseModel):
    """ Define como uma nova categoria a ser inserido deve ser representado
    """
    fornecedor_id: int = 1
    descricao_categoria: str = "Bebidas ,refrigerantes, agua e sucos no geral"
