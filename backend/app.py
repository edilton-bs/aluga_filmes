from flask import Flask, render_template, jsonify, request
import mysql.connector


app = Flask(__name__)


def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='mysql5525',
        database='database'
    )
    return connection


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consulta')
def consulta():
    return render_template('consulta.html')

@app.route('/cadastro')
def cadastra_filme():
    return render_template('cadastro.html')

@app.route('/api/filmes', methods=['GET'])
def get_filmes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM filmes')
    filmes = cursor.fetchall()
    conn.close()
    return jsonify(filmes)

@app.route('/api/alugar', methods=['POST'])
def alugar_filme():
    data = request.get_json()
    filme_id = data['filme_id']
    usuario_id = data['usuario']  # Recebe o ID do usuário do dropdown

    conn = get_db_connection()
    cursor = conn.cursor()

    # Atualiza a quantidade disponível do filme
    cursor.execute('''
        UPDATE filmes
        SET quantidade_disponivel = quantidade_disponivel - 1
        WHERE id = %s AND quantidade_disponivel > 0
    ''', (filme_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'message': 'Erro: Filme não disponível'}), 400

    # Registra o aluguel
    cursor.execute('''
        INSERT INTO emprestimos (id_usuario, id_filme, data_emprestimo, status)
        VALUES (%s, %s, CURDATE(), 'emprestado')
    ''', (usuario_id, filme_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Filme alugado com sucesso!'})


@app.route('/api/filmes-disponiveis', methods=['GET'])
def listar_filmes_disponiveis():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT * FROM filmes
        WHERE quantidade_disponivel > 0
    ''')
    filmes = cursor.fetchall()
    conn.close()
    return jsonify(filmes)


@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, nome FROM usuarios')  # Busca apenas o ID e o nome dos usuários
    usuarios = cursor.fetchall()
    conn.close()
    return jsonify(usuarios)


@app.route('/api/cadastrar-filme', methods=['POST'])
def cadastrar_filme():
    data = request.get_json()
    titulo = data['titulo']
    genero = data['genero']
    quantidade = data['quantidade']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO filmes (titulo, genero, quantidade_total, quantidade_disponivel)
        VALUES (%s, %s, %s, %s)
    ''', (titulo, genero, quantidade, quantidade))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Filme cadastrado com sucesso!'})

@app.route('/api/cadastrar-usuario', methods=['POST'])
def cadastrar_usuario():
    data = request.get_json()
    nome = data['nome']
    email = data['email']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nome, email)
        VALUES (%s, %s)
    ''', (nome, email))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Usuário cadastrado com sucesso!'})



if __name__ == '__main__':
    app.run(debug=True)
