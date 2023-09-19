from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Fornecedor, Categoria
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
fornecedor_tag = Tag(name="Fornecedor", description="Adição, visualização e remoção de fornecedores à base")
categoria_tag = Tag(name="Categoria", description="Adição de uma categoria à um forncedor cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/fornecedor', tags=[fornecedor_tag],
          responses={"200": FornecedorViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_fornecedor(form: FornecedorSchema):
    """Adiciona um novo Fornecedor à base de dados

    Retorna uma representação dos fornecedoress e categorias associados.
    """
    fornecedor = Fornecedor(
        nome=form.nome,
        descricao=form.descricao)
    logger.debug(f"Adicionando fornecedor de nome: '{fornecedor.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando fornecedor
        session.add(fornecedor)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado fornecedor de nome: '{fornecedor.nome}'")
        return apresenta_fornecedor(fornecedor), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Fornecedor de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar fornecedor '{fornecedor.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar fornecedor '{fornecedor.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/fornecedores', tags=[fornecedor_tag],
         responses={"200": ListagemFornecedoresSchema, "404": ErrorSchema})
def get_fornecedores():
    """Faz a busca por todos os Fornecedores cadastrados

    Retorna uma representação da listagem de fornecedores.
    """
    logger.debug(f"Coletando fornecedores ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    fornecedores = session.query(Fornecedor).all()

    if not fornecedores:
        # se não há fornecedores cadastrados
        return {"fornecedor": []}, 200
    else:
        logger.debug(f"%d fornecedores encontrados" % len(fornecedores))
        # retorna a representação de produto
        print(fornecedores)
        return apresenta_fornecedores(fornecedores), 200


@app.get('/fornecedor', tags=[fornecedor_tag],
         responses={"200": FornecedorViewSchema, "404": ErrorSchema})
def get_fornecedor(query: FornecedorBuscaSchema):
    """Faz a busca por um Fornecedor a partir do id do fornecedor

    Retorna uma representação dos fornecedores e categorias associados.
    """
    fornecedor_id = query.id
    logger.debug(f"Coletando dados sobre fornecedor #{fornecedor_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    fornecedor = session.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()

    if not fornecedor:
        # se o fornecedor não foi encontrado
        error_msg = "Fornecedor não encontrado na base :/"
        logger.warning(f"Erro ao buscar fornecedor '{fornecedor_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Fornecedor encontrado: '{fornecedor.nome}'")
        # retorna a representação de fornecedor
        return apresenta_fornecedor(fornecedor), 200


@app.delete('/fornecedor', tags=[fornecedor_tag],
            responses={"200": FornecedorDelSchema, "404": ErrorSchema})
def del_produto(query: FornecedorBuscaSchema):
    """Deleta um Produto a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    fornecedor_nome = unquote(unquote(query.nome))
    print(fornecedor_nome)
    logger.debug(f"Deletando dados sobre produto #{fornecedor_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Fornecedor).filter(Fornecedor.nome == fornecedor_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto #{fornecedor_nome}")
        return {"mesage": "Fornecedor removido", "id": fornecedor_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao deletar fornecedor #'{fornecedor_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/categoria', tags=[categoria_tag],
          responses={"200": FornecedorViewSchema, "404": ErrorSchema})
def add_categoria(form: CategoriaSchema):
    """Adiciona de uma nova à um fornecedor cadastrado na base identificado pelo id

    Retorna uma representação dos produtos e comentários associados.
    """
    fornecedor_id  = form.fornecedor_id
    logger.debug(f"Adicionando categoria ao fornecedor #{fornecedor_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo produto
    fornecedor = session.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()

    if not fornecedor:
        # se fornecedor não encontrado
        error_msg = "Fornecedor não encontrado na base :/"
        logger.warning(f"Erro ao adicionar categoria ao fornecedor '{fornecedor_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    categoria = Categoria(texto)

    # adicionando o categoria ao fornecedor
    fornecedor.adiciona_categoria(categoria)
    session.commit()

    logger.debug(f"Adicionado categoria ao fornecedor #{fornecedor_id}")

    # retorna a representação de fornecedor
    return apresenta_fornecedor(fornecedor), 200
