from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('mercado.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_unidades_from_database():
    conn = sqlite3.connect('mercado.db')
    cursor = conn.cursor()

    cursor.execute('SELECT endereco, telefone, nome FROM UnidadeMercado')
    unidades = cursor.fetchall()
    conn.close()

    return unidades

def get_produtos_em_estoque_from_database():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    cursor.execute('SELECT Produto.nome, Estoque.quantidade, Produto.preco FROM Produto INNER JOIN Estoque ON Produto.idProduto = Estoque.idProduto')
    produtos = cursor.fetchall()

    conn.close()

    return render_template('produtos_em_estoque.html', produtos=produtos)


@app.route('/')
def index():
    conn = get_db_connection()
    produtos = conn.execute('SELECT * FROM Produto').fetchall()
    conn.close()
    return render_template('index.html', produtos=produtos)

@app.route('/produtos_em_estoque')
def produtos_em_estoque():
    produtos = get_produtos_em_estoque_from_database()
    return render_template('produtos_em_estoque.html', produtos=produtos)

@app.route('/unidades_cadastradas')
def unidades_cadastradas():
    unidades = get_unidades_from_database()
    return render_template('unidades_cadastradas.html', unidades=unidades)

@app.route('/add_produto', methods=['GET', 'POST'])
def add_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        quantidade = request.form['quantidade']

        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()

        # Inserindo o novo produto na tabela "Produto"
        cursor.execute('INSERT INTO Produto (nome, preco) VALUES (?, ?)', (nome, preco))
        novo_produto_id = cursor.lastrowid

        # Inserindo a quantidade do novo produto na tabela "Estoque"
        cursor.execute('INSERT INTO Estoque (idProduto, quantidade) VALUES (?, ?)', (novo_produto_id, quantidade))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_produto.html')


@app.route('/comprar/<int:idProduto>', methods=('GET', 'POST'))
def comprar(idProduto):
    if request.method == 'POST':
        quantidade = int(request.form['quantidade'])
        idMercado = int(request.form['idMercado'])

        conn = get_db_connection()
        produto = conn.execute('SELECT * FROM Produto WHERE idProduto = ?', (idProduto,)).fetchone()
        estoque = conn.execute('SELECT * FROM Estoque WHERE idProduto = ?', (idProduto,)).fetchone()

        if produto and estoque and estoque['quantidade'] >= quantidade:
            nova_quantidade = estoque['quantidade'] - quantidade
            conn.execute('UPDATE Estoque SET quantidade = ? WHERE idProduto = ?', (nova_quantidade, idProduto))
            conn.execute('INSERT INTO Log (idProduto, idMercado, quantidade) VALUES (?, ?, ?)', (idProduto, idMercado, quantidade))
            conn.commit()

        conn.close()
        return redirect(url_for('index'))

    conn = get_db_connection()
    mercados = conn.execute('SELECT * FROM UnidadeMercado').fetchall()
    conn.close()
    return render_template('comprar.html', idProduto=idProduto, mercados=mercados)

@app.route('/add_mercado', methods=('GET', 'POST'))
def add_mercado():
    if request.method == 'POST':
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        nome = request.form['nome']

        conn = get_db_connection()
        conn.execute('INSERT INTO UnidadeMercado (endereco, telefone, nome) VALUES (?, ?, ?)', (endereco, telefone, nome))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_mercado.html')

@app.route('/excluir_produto/<int:id_produto>')
def excluir_produto(id_produto):
    conn = sqlite3.connect('mercado.db')  # Conectar ao banco de dados 'mercado.db'
    cursor = conn.cursor()

    # Excluir o produto pelo ID
    cursor.execute('DELETE FROM Produto WHERE idProduto = ?', (id_produto,))
    conn.commit()

    # Redirecionar de volta para a página inicial
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
