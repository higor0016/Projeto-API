from flask import Flask
from .routes.livros import livros_ns 
from .routes.autores import autores_ns 
from .routes.login import login_ns
from flask_restx import Api
from sqlalchemy import text
from app.extensions import db
from app.extensions import jwt
import os
import datetime

# Para ler as chaves:
from cryptography.hazmat.primitives import serialization


def create_app():
    app = Flask(__name__)
    api = Api(app, title='API de Livraria', version='1.0', description='API simples de Livraria')

    #Lendo chave privada
    private_key = open('.ssh/higor', 'r').read()
    pr_key = serialization.load_ssh_private_key(private_key.encode(), password=b'teste')

    #Lendo chave publica
    public_key = open('.ssh/higor.pub', 'r').read()
    pubKey = serialization.load_ssh_public_key(public_key.encode())


     # Configurações da aplicação
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:higorlucas016@localhost:5432/livrariaDB'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #JWT config
    app.config['JWT_SECRET_KEY'] = pr_key
    app.config["JWT_PRIVATE_KEY"] = pr_key
    app.config["JWT_PUBLIC_KEY"] = pubKey
    app.config['JWT_ALGORITHM'] = 'RS256'

    #Tempo de expiração do token
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=1)

    #Inicializa extensões
    jwt.init_app(app)
    db.init_app(app)
    from app.models.models import Livro

    with app.app_context():
        try:
            # Testa a conexão tentando acessar a sessão do banco
            db.session.execute(text('SELECT 1'))
            print("Conexão com o banco de dados estabelecida com sucesso.")
            db.create_all()
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
       

    #Registro de Rotas
    api.add_namespace(livros_ns)
    api.add_namespace(autores_ns)
    api.add_namespace(login_ns, path='/login')

    #api.add_namespace(login_ns)


    return app