from flask import Flask
#from flask_jwt_extended import JWTManager

from .routes.livros import livros_ns 
from .routes.autores import autores_ns 
from flask_restx import Api
from sqlalchemy import text
from app.extensions import db




def create_app():
    app = Flask(__name__)
    api = Api(app, title='API de Livraria', version='1.0', description='API simples de Livraria')

    

     # Configurações da aplicação
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:higorlucas016@localhost:5432/livrariaDB'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta'

    #Inicializa extensões
    #jwt.init_app(app)
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


    return app