import sqlite3

def init_db_estoque():
    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()

    # Criação das tabelas no banco de dados 'estoque.db'
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

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db_estoque()
