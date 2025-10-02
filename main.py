# main.py
"""Aplicação principal do MadeiraSys"""
from fasthtml.common import *
from database.db_setup import init_db
from auth.middleware import bware
from routes.auth_routes import setup_auth_routes
from routes.dashboard import setup_dashboard_routes
from routes.clientes import setup_clientes_routes
from routes.pedidos import setup_pedidos_routes
from routes.pedidos_view import setup_pedido_view_route
from routes.romaneio import setup_romaneio_routes
from routes.usuarios import setup_usuarios_routes
from config import APP_NAME

# Inicializar banco de dados
init_db()

# CSS customizado inline
custom_css = Style("""
    :root {
        --primary-color: #2c5530;
        --secondary-color: #6b8e23;
        --accent-color: #8b4513;
        --bg-light: #f5f5dc;
    }
    
    body {
        background-color: var(--bg-light);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .header-custom {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .card-custom {
        background: white;
        border-radius: 0.5rem;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    .btn-primary-custom {
        background-color: var(--primary-color);
        border-color: var(--primary-color);
    }
    
    .btn-primary-custom:hover {
        background-color: var(--secondary-color);
        border-color: var(--secondary-color);
    }
    
    .table-responsive {
        overflow-x: auto;
    }
    
    @media (max-width: 768px) {
        .header-custom h1 {
            font-size: 1.5rem;
        }
        
        .card-custom {
            padding: 1rem;
        }
        
        table {
            font-size: 0.9rem;
        }
    }
    
    .dashboard-card {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .dashboard-card h3 {
        color: var(--primary-color);
        font-size: 2.5rem;
        margin: 0;
    }
    
    .dashboard-card p {
        color: #666;
        margin: 0.5rem 0 0 0;
    }
    
    .logo {
        display: inline-block;
        font-weight: bold;
        font-size: 1.5rem;
    }
    
    .version {
        font-size: 0.8rem;
        opacity: 0.8;
    }
""")

# Criar aplicação FastHTML
app = FastHTML(
    before=bware,
    hdrs=(
        picolink,
        custom_css,
        Script(src="https://unpkg.com/htmx.org@1.9.10"),
    )
)

rt = app.route

# Configurar todas as rotas
setup_auth_routes(rt)
setup_dashboard_routes(rt)
setup_clientes_routes(rt)
setup_pedidos_routes(rt)
setup_pedido_view_route(rt)
setup_romaneio_routes(rt)
setup_usuarios_routes(rt)

# Iniciar servidor
if __name__ == "__main__":
    serve()
