# database/models.py
"""Funções de acesso ao banco de dados"""
import sqlite3
from config import DB_PATH

def get_db():
    """Retorna uma conexão com o banco"""
    return sqlite3.connect(DB_PATH)

# ===== USUÁRIOS =====
def get_user_by_credentials(email, password):
    """Busca usuário por email e senha"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, nome_completo, is_admin FROM usuarios_sistema WHERE email=? AND senha=?',
              (email, password))
    user = c.fetchone()
    conn.close()
    return user

def get_all_users():
    """Retorna todos os usuários"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, nome_completo, email, cpf, telefone, is_admin FROM usuarios_sistema')
    users = c.fetchall()
    conn.close()
    return users

def create_user(nome_completo, email, cpf, telefone, senha, is_admin):
    """Cria um novo usuário"""
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute('''INSERT INTO usuarios_sistema 
                     (nome_completo, email, cpf, telefone, senha, is_admin) 
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (nome_completo, email, cpf, telefone, senha, is_admin))
        conn.commit()
        success = True
    except:
        success = False
    conn.close()
    return success

# ===== CLIENTES =====
def get_all_clientes():
    """Retorna todos os clientes"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM clientes ORDER BY nome')
    clientes = c.fetchall()
    conn.close()
    return clientes

def create_cliente(nome, cpf_cnpj, telefone, endereco):
    """Cria um novo cliente"""
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO clientes (nome, cpf_cnpj, telefone, endereco) VALUES (?, ?, ?, ?)',
              (nome, cpf_cnpj, telefone, endereco))
    conn.commit()
    conn.close()

# ===== PEDIDOS =====
def get_all_pedidos():
    """Retorna todos os pedidos com informações do cliente"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT p.id, p.codigo, p.data, c.nome, p.motorista, p.total_m3, p.valor_total
                 FROM pedidos p 
                 LEFT JOIN clientes c ON p.cliente_id = c.id
                 ORDER BY p.data DESC''')
    pedidos = c.fetchall()
    conn.close()
    return pedidos

def create_pedido(codigo, data, representante, cliente_id, motorista, nota_fiscal, 
                  data_nota, total_m3, valor_total, usuario_id):
    """Cria um novo pedido"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''INSERT INTO pedidos 
                 (codigo, data, representante, cliente_id, motorista, nota_fiscal, 
                  data_nota, total_m3, valor_total, usuario_id)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (codigo, data, representante, cliente_id, motorista, nota_fiscal, 
               data_nota, total_m3, valor_total, usuario_id))
    pedido_id = c.lastrowid
    conn.commit()
    conn.close()
    return pedido_id

def create_item_pedido(pedido_id, descricao, quantidade, valor_unitario, valor_total):
    """Cria um item de pedido"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''INSERT INTO itens_pedido 
                 (pedido_id, descricao, quantidade, valor_unitario, valor_total) 
                 VALUES (?, ?, ?, ?, ?)''',
              (pedido_id, descricao, quantidade, valor_unitario, valor_total))
    conn.commit()
    conn.close()

# ===== ESTATÍSTICAS =====
def get_dashboard_stats():
    """Retorna estatísticas para o dashboard"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM pedidos')
    total_pedidos = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM clientes')
    total_clientes = c.fetchone()[0]
    
    c.execute('SELECT SUM(total_m3) FROM pedidos')
    total_m3 = c.fetchone()[0] or 0
    
    c.execute('SELECT SUM(valor_total) FROM pedidos')
    total_valor = c.fetchone()[0] or 0
    
    conn.close()
    
    return {
        'total_pedidos': total_pedidos,
        'total_clientes': total_clientes,
        'total_m3': total_m3,
        'total_valor': total_valor
    }