# database/models_extended.py
"""Funções adicionais de acesso ao banco de dados"""
from config import DB_PATH
import sqlite3

def get_db():
    """Retorna uma conexão com o banco"""
    return sqlite3.connect(DB_PATH)

def get_pedido_by_id(pedido_id):
    """Retorna um pedido específico com todos os detalhes"""
    conn = get_db()
    c = conn.cursor()
    
    # Buscar dados do pedido
    c.execute('''SELECT p.*, c.nome as cliente_nome, c.cpf_cnpj, c.telefone, c.endereco,
                        u.nome_completo as usuario_nome
                 FROM pedidos p
                 LEFT JOIN clientes c ON p.cliente_id = c.id
                 LEFT JOIN usuarios_sistema u ON p.usuario_id = u.id
                 WHERE p.id = ?''', (pedido_id,))
    pedido = c.fetchone()
    
    # Buscar itens do pedido
    c.execute('SELECT * FROM itens_pedido WHERE pedido_id = ?', (pedido_id,))
    itens = c.fetchall()
    
    # Buscar romaneio
    c.execute('SELECT * FROM romaneio WHERE pedido_id = ? ORDER BY essencia', (pedido_id,))
    romaneio = c.fetchall()
    
    conn.close()
    
    return {
        'pedido': pedido,
        'itens': itens,
        'romaneio': romaneio
    }

def create_romaneio_item(pedido_id, essencia, espessura, largura, comprimento, 
                         quantidade, m3_total, percentual):
    """Cria um item de romaneio"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''INSERT INTO romaneio 
                 (pedido_id, essencia, espessura, largura, comprimento, 
                  quantidade, m3_total, percentual)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (pedido_id, essencia, espessura, largura, comprimento, 
               quantidade, m3_total, percentual))
    conn.commit()
    conn.close()

def delete_cliente(cliente_id):
    """Deleta um cliente"""
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
        conn.commit()
        success = True
    except:
        success = False
    conn.close()
    return success

def get_cliente_by_id(cliente_id):
    """Retorna um cliente específico"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,))
    cliente = c.fetchone()
    conn.close()
    return cliente
