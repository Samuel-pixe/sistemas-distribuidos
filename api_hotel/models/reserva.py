from flask_restx import Resource, fields

# Modelo para os dados de reserva
reserva =  {
    'id_quarto': fields.Integer(required=True, description='ID do quarto'),
    'data_inicio': fields.Date(required=True, description='Data de início da reserva'),
    'data_fim': fields.Date(required=True, description='Data de fim da reserva'),
    'nome_cliente': fields.String(required=True, description='Nome do cliente'),
}
