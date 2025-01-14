from flask import Flask, render_template, jsonify
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

@app.route('/api/filmes', methods=['GET'])
def get_filmes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM filmes')
    filmes = cursor.fetchall()
    conn.close()
    return jsonify(filmes)

if __name__ == '__main__':
    app.run(debug=True)
