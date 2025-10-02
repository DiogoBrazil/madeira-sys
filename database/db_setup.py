# database/db_setup.py
"""Configuração e inicialização do banco de dados"""
import sqlite3
import os
from config import DB_PATH, ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_CPF

def init_db():
    """Cria as tabelas e usuário admin padrão"""
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Tabela de usuários do sistema
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios_sistema (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_completo TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        cpf TEXT UNIQUE NOT NULL,
        telefone TEXT,
        senha TEXT NOT NULL,
        is_admin BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Tabela de clientes
    c.execute('''CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf_cnpj TEXT UNIQUE,
        telefone TEXT,
        endereco TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Tabela de pedidos
    c.execute('''CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE NOT NULL,
        data DATE NOT NULL,
        representante TEXT,
        cliente_id INTEGER,
        motorista TEXT,
        nota_fiscal TEXT,
        data_nota DATE,
        total_m3 REAL DEFAULT 0,
        valor_total REAL DEFAULT 0,
        usuario_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios_sistema(id)
    )''')
    
    # Tabela de itens do pedido
    c.execute('''CREATE TABLE IF NOT EXISTS itens_pedido (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER,
        descricao TEXT NOT NULL,
        quantidade REAL,
        valor_unitario REAL,
        valor_total REAL,
        FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE
    )''')
    
    # Tabela de romaneio
    c.execute('''CREATE TABLE IF NOT EXISTS romaneio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER,
        essencia TEXT NOT NULL,
        espessura REAL,
        largura REAL,
        comprimento REAL,
        quantidade INTEGER,
        m3_total REAL,
        percentual REAL,
        FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE
    )''')
    
    # Criar usuário admin padrão
    c.execute('''INSERT OR IGNORE INTO usuarios_sistema 
                 (nome_completo, email, cpf, senha, is_admin) 
                 VALUES (?, ?, ?, ?, ?)''',
              ('Administrador', ADMIN_EMAIL, ADMIN_CPF, ADMIN_PASSWORD, 1))
    
    conn.commit()
    conn.close()