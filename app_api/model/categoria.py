from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Categoria(Base):
    __tablename__ = 'categoria'

    id = Column(Integer, primary_key=True)
    descricao_categoria = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre a categoria e um fornecedor.
    # Aqui está sendo definido a coluna 'categoria' que vai guardar
    # a referencia ao fornecedor, a chave estrangeira que relaciona
    # um fornecedor a categoria.
    fornecedor = Column(Integer, ForeignKey("fornecedor.pk_fornecedor"), nullable=False)

    def __init__(self, descricao_categoria:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Categoria

        Arguments:
            descricao_categoria: o texto descrevendo a categoria de produtos do forneedor
            data_insercao: data de quando o comentário foi feito ou inserido à base
        """
        self.descricao_categoria = descricao_categoria
        if data_insercao:
            self.data_insercao = data_insercao
