from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from flask_jwt_extended import create_access_token
#from app.models.models import Autor
#from app.extensions import db
#from flask_jwt_extended import jwt_required


#Definindo namespace para organziar as rotas
login_ns = Namespace('login', description='Operações relacionadas ao login')

autor_model = login_ns.model('Login', {
    'id': fields.Integer,
    'user': fields.String,
    'password': fields.String,
})

@login_ns.route('/')
class Login(Resource):
    def post(self):
        username = request.json.get("username", None)
        #usernametest = request.get_json("username", None)
        print(username)
       # print(usernametest)
        password = request.json.get("password", None)

        if username != "test" or password != "test":
            return jsonify({"msg":"Usuário ou senha incorretos"}), 401

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)


