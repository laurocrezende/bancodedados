import sqlite3

def init_db_mercado():
    conn = sqlite3.connect('mercado.db')
    c = conn.cursor()

    # Criação das tabelas no banco de dados 'mercado.db'
    c.execute('''
    CREATE TABLE IF NOT EXISTS Produto (
        idProduto INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        preco REAL NOT NULL
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS Estoque (
        idProduto INTEGER,
        quantidade INTEGER NOT NULL,
        FOREIGN KEY (idProduto) REFERENCES Produto(idProduto)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS UnidadeMercado (
        idMercado INTEGER PRIMARY KEY,
        endereco TEXT NOT NULL,
        telefone TEXT NOT NULL,
        nome TEXT NOT NULL
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS Log (
        idLog INTEGER PRIMARY KEY,
        idProduto INTEGER,
        idMercado INTEGER,
        quantidade INTEGER NOT NULL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (idProduto) REFERENCES Produto(idProduto),
        FOREIGN KEY (idMercado) REFERENCES UnidadeMercado(idMercado)
    )
    ''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db_mercado()
   