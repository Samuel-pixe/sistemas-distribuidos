from flask_restx import fields

usuario = {
    'nome_usuario': fields.String(required=True, description='Nome de usuário'),
    'email': fields.String(required=True, description='Endereço de e-mail'),
    'senha': fields.String(required=True, description='Senha'),
    'data_nascimento': fields.String(required=True, description='Data de nascimento no formato YYYY-MM-DD'),
}
