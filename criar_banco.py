import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

# Conecta/cria o banco
conn = sqlite3.connect(DB_PATH)

# Criação da tabela anúncios
conn.execute("""
CREATE TABLE IF NOT EXISTS anuncios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    anunciante TEXT NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT,
    preco TEXT NOT NULL,
    whatsapp TEXT NOT NULL,
    imagem TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Banco de dados criado com sucesso!")