from flask_restx import Namespace, Resource, fields
from flask import request
from app.extensions import db
from app.models.models import Livro

#Definindo namespace para organziar as rotas
livros_ns = Namespace('livros', description='Operações relacionadas a livros')
livro_model = livros_ns.model('Livro', {
    'id': fields.Integer,
    'titulo': fields.String,
    'autor': fields.String,
    'ano_publicacao': fields.String,
})

@livros_ns.route('/')
class LivrosList(Resource):
    #Manipulação da Lista de Livros
    @livros_ns.doc('listar_livros')
    @livros_ns.marshal_list_with(livro_model)

    #função get para pegar os livros
    def get(self):
        livros = Livro.query.all()
        return [{'id': livro.id, 'titulo': livro.titulo, 'autor': livro.autor, 'ano_publicacao': livro.ano_publicacao} for livro in livros]

    #Função para criar um novo livro
    def post(self):
        data = request.get_json()
        novo_livro = Livro(titulo=data['titulo'],autor=data['autor'], ano_publicacao=data['ano_publicacao'] )
        db.session.add(novo_livro)
        db.session.commit()
        return {'Message': 'Livro Criado com Sucesso!'}, 201