from flask_restx import Namespace, Resource, fields
from flask import request
from app.models.models import Autor
from app.extensions import db
from flask_jwt_extended import jwt_required



#Definindo namespace para organziar as rotas
autores_ns = Namespace('autores', description='Operações relacionadas a autores')

autor_model = autores_ns.model('Livro', {
    'id': fields.Integer,
    'nome': fields.String,
    'biografia': fields.String,
})

@jwt_required()
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
        

@autores_ns.route('/update/<int:id>')
class AutoresUpdate(Resource):

    #Função para atualizar um autores
    def put(self, id):
        autor = Autor.query.get(id)
        if not autor:
            return {"Mensagem":"Autor não encontrado"}, 404
        
        dados = autores_ns.payload

        try:
            autor.nome = dados.get('nome', autor.nome)
            autor.biografia = dados.get('biografia', autor.biografia)

            db.session.commit()
            return {"Mensagem":"Autor atualizado com sucesso!"},200
        
        except Exception as e:
            db.session.rollback() # Para reverter as alterações em caso de problemas
            return {"Mensagem": f"Erro ao atualizar autor: {str(e)}"},500
        

@autores_ns.route('/delete/<int:id>')
class AutorDelete(Resource):
    def delete(self, id):
        autor = Autor.query.get(id)
        if not autor:
            return {"Mensagem":"Autor não encontrado"}, 404

        try:  
            db.session.delete(autor)
            db.session.commit()
            return {"Mensagem":"Autor excluído com sucesso"}, 200
        except Exception as e:
            db.session.rollback()
            return {"Mensagem": f"Erro ao excluir o Autor: {str(e)}"},500