import os
from flask import Flask, jsonify, render_template, send_from_directory,request
from flask_restx import Api, Resource, fields
from models.usuario import usuario
from models.reserva import reserva
from dotenv import load_dotenv
import mysql.connector



# Carregar variáveis de ambiente a partir do arquivo .env
load_dotenv()

app = Flask(__name__)
api = Api(app, version="1.0", title="API de Hotel", description="API para cadastro de usuários e reservas em um hotel", doc='/doc')#doc='/doc'

""" 
# Configuração da conexão
config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_DATABASE'),
    'raise_on_warnings': True
}

# Criação da conexão
db_connection = mysql.connector.connect(**config)
""" 
db_connection = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "hotel_db")
)

# Dados de exemplo para testes
"""
usuarios = [
    {'id': 1, 'nome_usuario': "Usuário 1 do hotel", 'email': "email1@gmail.com", 'senha': "123456", 'data_nascimento': "1999-02-02"},
    {'id': 2, 'nome_usuario': "Usuário 2 do hotel", 'email': "email2@gmail.com", 'senha': "123456", 'data_nascimento': "1999-02-02"},
    {'id': 3, 'nome_usuario': "Usuário 3 do hotel", 'email': "email3@gmail.com", 'senha': "123456", 'data_nascimento': "1999-02-02"},
    {'id': 4, 'nome_usuario': "Usuário 4 do hotel", 'email': "email4@gmail.com", 'senha': "123456", 'data_nascimento': "1999-02-02"},
]
"""
usuarios = []

# Rota para a página inicial
@app.route('/index')
def index():
    return render_template('index.html')

# Rota para a página de cadastro de usuário
@app.route('/usuario_hotel')
def usuario_hotel():
    return render_template('usuario_hotel.html')

# Rota para a página de reserva de quarto
@app.route('/reserva_hotel')
def reserva_hotel():
    return render_template('reserva_hotel.html')

@app.route('/listar_usuario')
def listar_usuario():
    return render_template('listar_usuario.html')

@app.route('/listar_reserva')
def listar_reserva():
    return render_template('listar_reserva.html')

# Rota para servir arquivos estáticos (como imagens)
@app.route('/imagens/<path:filename>')
def serve_image(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'imagem'), filename)

ns = api.namespace('hotel-hospedes', description='Operações hospede')

@ns.route("/doc")
class ListaUsuarios(Resource):
    @api.doc("listar_usuarios")
    def get(self):
        '''Retorna uma lista de todos os usuários registrados'''
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_usuarios")
        result = cursor.fetchall()
        cursor.close()
        return jsonify({'usuarios': result})

    @api.doc("adicionar_usuario")
    @api.expect(api.model('UsuarioModel', usuario))
    def post(self):
        '''Cadastra um novo usuário no hotel'''
        novo_usuario = {
            'id': len(usuarios) + 1,
            'nome_usuario': request.json['nome_usuario'],
            'email': request.json['email'],
            'senha': request.json['senha'],
            'data_nascimento': request.json['data_nascimento'],
        }

        # Adicionar usuário ao banco de dados
        cursor = db_connection.cursor()
        insert_query = "INSERT INTO tb_usuarios (nome_usuario, email, senha, data_nascimento) VALUES (%s, %s, %s, %s)"
        user_data = (novo_usuario['nome_usuario'], novo_usuario['email'], novo_usuario['senha'], novo_usuario['data_nascimento'])
        cursor.execute(insert_query, user_data)
        db_connection.commit()
        cursor.close()

        usuarios.append(novo_usuario)
        return jsonify({'resposta': 'Usuário cadastrado com sucesso.'})
    
@ns.route("/<int:item_id>")
@api.response(200, "Item retornado com sucesso.")
@api.response(404, "Item não encontrado.")
class Item(Resource):
    @api.doc("retornar_um_item")
    def get(self, item_id):
        '''Retorna um único item da lista a partir do ID'''
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_usuarios WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        cursor.close()
        if item:
            return jsonify({'item': item})
        else:
            api.abort(404, 'Item não encontrado.')
        
    @api.doc("atualizar_itens_usuario")
    @api.expect(api.model('UsuarioModel', {'nome_usuario': fields.String, 'email': fields.String, 'senha': fields.String, 'data_nascimento': fields.String}))
    def put(self, item_id):
        '''Atualizar itens de um usuário específico'''
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_usuarios WHERE id = %s", (item_id,))
        user = cursor.fetchone()
        if user:
            user_data = {
                'nome_usuario': request.json['nome_usuario'],
                'email': request.json['email'],
                'senha': request.json['senha'],
                'data_nascimento': request.json['data_nascimento'],
            }

            update_query = "UPDATE tb_usuarios SET nome_usuario = %s, email = %s, senha = %s, data_nascimento = %s WHERE id = %s"
            update_data = (user_data['nome_usuario'], user_data['email'], user_data['senha'], user_data['data_nascimento'], item_id)

            cursor.execute(update_query, update_data)
            db_connection.commit()

            cursor.close()
            return jsonify({'user': user_data})
        else:
            cursor.close()
            api.abort(404, 'Usuário não encontrado.')

    @api.doc("excluir_usuario")
    def delete(self, item_id):
        '''Excluir um usuário da tabela'''
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("DELETE FROM tb_usuarios WHERE id = %s", (item_id,))
        db_connection.commit()
        # Verificar se algum registro foi excluído
        if cursor.rowcount > 0:
            cursor.close()
            return jsonify({'resposta': 'Usuário excluído com sucesso.'})
        else:
            cursor.close()
            api.abort(404, 'Usuário não encontrado.')

ns2 = api.namespace('hotel-Quartos', description='Operações quarto')

@ns2.route("/doc")
class ListaQuartos(Resource):
    @api.doc("listar_quartos")
    def get(self):
        '''Retorna uma lista de todos os quartos cadastrados'''
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_quartos")
        result = cursor.fetchall()
        cursor.close()
        return jsonify({'quartos': result})

ns3 = api.namespace('hotel-Reservas', description='Operações reserva')

@ns3.route("/doc")
class Reserva(Resource):
    @api.doc("listar_reservas")
    def get(self):
        '''Retorna uma lista de todas as reservas'''
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_reserva")
        result = cursor.fetchall()
        cursor.close()
        return jsonify({'reservas': result})

    @api.doc("adicionar_reserva")
    @api.expect(api.model('ReservaModel', reserva))
    def post(self):
        '''Cadastra uma nova reserva'''
        nova_reserva = {
            'id': len(reserva) + 1,
            'id_quarto': request.json['id_quarto'],
            'data_inicio': request.json['data_inicio'],
            'data_fim': request.json['data_fim'],
            'nome_cliente': request.json['nome_cliente'],
        }

        # Adicionar reserva ao banco de dados
        cursor = db_connection.cursor()
        insert_query = "INSERT INTO tb_reserva (id_quarto, data_inicio, data_fim, nome_cliente) VALUES (%s, %s, %s, %s)"
        reserva_data = (nova_reserva['id_quarto'], nova_reserva['data_inicio'], nova_reserva['data_fim'], nova_reserva['nome_cliente'])
        cursor.execute(insert_query, reserva_data)
        db_connection.commit()
        cursor.close()

        return jsonify({'resposta': 'Reserva cadastrada com sucesso.'})

@ns3.route("/<int:item_id>")
@api.response(200, "Reserva retornada com sucesso.")
@api.response(404, "Reserva não encontrada.")
class Item(Resource):
    @api.doc("retornar_uma_reserva")
    def get(self, item_id):
        '''Retorna uma única reserva a partir do ID'''
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_reserva WHERE id = %s", (item_id,))
        reserva = cursor.fetchone()
        cursor.close()
        if reserva:
            return jsonify({'reserva': reserva})
        else:
            api.abort(404, 'Reserva não encontrada.')

    @api.doc("atualizar_itens_reserva")
    @api.expect(api.model('ReservaModel', {'id_quarto': fields.Integer, 'data_inicio': fields.String, 'data_fim': fields.String, 'nome_cliente': fields.String}))
    def put(self, item_id):
        '''Atualizar itens de uma reserva específica'''
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_reserva WHERE id = %s", (item_id,))
        reserva = cursor.fetchone()
        if reserva:
            reserva_data = {
                'id_quarto': request.json['id_quarto'],
                'data_inicio': request.json['data_inicio'],
                'data_fim': request.json['data_fim'],
                'nome_cliente': request.json['nome_cliente'],
            }

            update_query = "UPDATE tb_reserva SET id_quarto = %s, data_inicio = %s, data_fim = %s, nome_cliente = %s WHERE id = %s"
            update_data = (reserva_data['id_quarto'], reserva_data['data_inicio'], reserva_data['data_fim'], reserva_data['nome_cliente'], item_id)

            cursor.execute(update_query, update_data)
            db_connection.commit()

            cursor.close()
            return jsonify({'reserva': reserva_data})
        else:
            cursor.close()
            api.abort(404, 'Reserva não encontrada.')

    @api.doc("excluir_reserva")
    def delete(self, item_id):
        '''Excluir uma reserva da tabela'''
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("DELETE FROM tb_reserva WHERE id = %s", (item_id,))
        db_connection.commit()
        # Verificar se algum registro foi excluído
        if cursor.rowcount > 0:
            cursor.close()
            return jsonify({'resposta': 'Reserva excluída com sucesso.'})
        else:
            cursor.close()
            api.abort(404, 'Reserva não encontrada.')

if __name__ == '__main__':
    app.run(debug=True, port=5000)#5239