# routes/dashboard.py
"""Rota do dashboard principal"""
from fasthtml.common import *
from database.models import get_dashboard_stats
from config import APP_NAME, APP_TAGLINE

def setup_dashboard_routes(rt):
    @rt("/")
    def get(sess):
        auth = sess.get('auth')
        stats = get_dashboard_stats()
        
        header = Div(
            Grid(
                Div(
                    H1(Span("🌲 "), Span(APP_NAME), style="margin: 0;"),
                    P(APP_TAGLINE, style="margin: 0; opacity: 0.9;"),
                ),
                Div(
                    P(f"Bem-vindo, {auth['nome']}", style="margin: 0;"),
                    A("Sair", href="/logout", style="color: white; text-decoration: underline;"),
                    style="text-align: right;"
                )
            ),
            cls='header-custom'
        )
        
        stat_cards = Grid(
            Div(H3(str(stats['total_pedidos'])), P("Total de Pedidos"), cls='dashboard-card'),
            Div(H3(str(stats['total_clientes'])), P("Clientes Cadastrados"), cls='dashboard-card'),
            Div(H3(f"{stats['total_m3']:.2f} m³"), P("Volume Total"), cls='dashboard-card'),
            Div(H3(f"R$ {stats['total_valor']:,.2f}"), P("Valor Total"), cls='dashboard-card'),
        )
        
        menu = Div(
            Grid(
                A("➕ Novo Pedido", href="/pedidos/novo", role="button", cls='btn-primary-custom'),
                A("📋 Ver Pedidos", href="/pedidos", role="button"),
                A("👥 Clientes", href="/clientes", role="button"),
                A("👤 Usuários", href="/usuarios", role="button") if auth.get('is_admin') else Div(),
            ),
            cls='card-custom'
        )
        
        return Title(APP_NAME), Container(header, stat_cards, menu)