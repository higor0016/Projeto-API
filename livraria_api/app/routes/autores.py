from flask_restx import Namespace, Resource, fields
from flask import request
from app.models.models import Autor
from app.extensions import db



#Definindo namespace para organziar as rotas
autores_ns = Namespace('autores', description='Operações relacionadas a autores')

autor_model = autores_ns.model('Livro', {
    'id': fields.Integer,
    'nome': fields.String,
    'biografia': fields.String,
})

@autores_ns.route('/')
class AutoresList(Resource):
    #Manipulação da lista de Autores
    @autores_ns.doc('listar_autores')
    @autores_ns.marshal_list_with(autor_model)

    #Função para pegar os autores
    def get(self):
        autores = Autor.query.all()
        return [{'id': autor.id, 'nome': autor.nome, 'biografia': autor.biografia} for autor in autores]

    #Função para criar um novo autor
    def post(self):
        data = request.get_json()
        novo_autor = Autor(nome=data['nome'], biografia=data['biografia'])
        db.session.add(novo_autor)
        db.session.commit()
        return {'Message': 'Autor Criado com Sucesso!'}, 201
        