from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


#Inicialização de extensões
jwt = JWTManager()
db = SQLAlchemy()