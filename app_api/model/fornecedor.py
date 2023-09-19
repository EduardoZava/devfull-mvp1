from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Categoria


class Fornecedor(Base):
    __tablename__ = 'fornecedor'

    id = Column("pk_fornecedor", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    descricao = Column(String(200))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o produto e categoria.
    # Essa relação é implicita, não está salva na tabela 'fornecedor',
    # mas SQLAlchemy tem a responsabilidade de reconstruir esse relacionamento.
    categorias = relationship("Categoria")

    def __init__(self, nome:str, descricao:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Produto

        Arguments:
            nome: nome do fornecedor.
            descricao: descricao do que o fornecedor vende
            valor: valor esperado para o produto
            data_insercao: data de quando o fornecedor foi inserido à base
        """
        self.nome = nome
        self.descricao = descricao

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_categoria(self, categoria:Categoria):
        """ Adiciona uma nova categoria ao fornecedor 
        """
        self.categorias.append(categoria)
