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

@app.route('/cadastrar-filme')
def cadastra_filme():
    return render_template('cadastro-filme.html')

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
    usuario = data['usuario']

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
    ''', (usuario, filme_id))
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

if __name__ == '__main__':
    app.run(debug=True)
