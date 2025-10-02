# routes/pedidos_view.py
"""Rota para visualização detalhada de pedidos"""
from fasthtml.common import *
from database.models_extended import get_pedido_by_id
from config import APP_NAME

def setup_pedido_view_route(rt):
    @rt("/pedidos/{pedido_id}")
    def get(pedido_id: int):
        dados = get_pedido_by_id(pedido_id)
        pedido = dados['pedido']
        itens = dados['itens']
        romaneio = dados['romaneio']
        
        if not pedido:
            return RedirectResponse('/pedidos', status_code=303)
        
        header = Div(
            Grid(
                H2(f"Pedido {pedido[1]}"),  # codigo
                A("← Voltar", href="/pedidos", role="button", cls="outline"),
            ),
            cls='header-custom'
        )
        
        # Dados do pedido
        info_pedido = Div(
            H3("Informações do Pedido"),
            Grid(
                Div(Strong("Código: "), pedido[1]),
                Div(Strong("Data: "), pedido[2]),
            ),
            Grid(
                Div(Strong("Representante: "), pedido[3] or '-'),
                Div(Strong("Motorista: "), pedido[5] or '-'),
            ),
            Grid(
                Div(Strong("Cliente: "), pedido[12] or '-'),  # cliente_nome
                Div(Strong("Nota Fiscal: "), pedido[6] or '-'),
            ),
            Grid(
                Div(Strong("Total m³: "), f"{pedido[8]:.2f}"),
                Div(Strong("Valor Total: "), f"R$ {pedido[9]:,.2f}"),
            ),
            cls='card-custom'
        )
        
        # Itens do pedido
        tabela_itens = Div(
            H3("Itens do Pedido"),
            Table(
                Thead(Tr(
                    Th("Descrição"), Th("Volume (m³)"), Th("Valor Unit."), Th("Valor Total")
                )),
                Tbody(
                    *[Tr(
                        Td(item[2]), 
                        Td(f"{item[3]:.4f}"), 
                        Td(f"R$ {item[4]:,.2f}"),
                        Td(f"R$ {item[5]:,.2f}")
                    ) for item in itens]
                )
            ),
            cls='card-custom'
        )
        
        # Romaneio (se existir)
        romaneio_section = Div()
        if romaneio:
            romaneio_section = Div(
                H3("Romaneio"),
                Table(
                    Thead(Tr(
                        Th("Essência"), Th("Espessura (cm)"), Th("Largura (cm)"), 
                        Th("Comprimento (m)"), Th("Qtd"), Th("m³ Total"), Th("%")
                    )),
                    Tbody(
                        *[Tr(
                            Td(r[2]), 
                            Td(f"{r[3]:.2f}"), 
                            Td(f"{r[4]:.2f}"),
                            Td(f"{r[5]:.2f}"),
                            Td(str(r[6])),
                            Td(f"{r[7]:.4f}"),
                            Td(f"{r[8]:.2f}%")
                        ) for r in romaneio]
                    )
                ),
                cls='card-custom'
            )
        
        botoes = Div(
            A("➕ Adicionar Romaneio", href=f"/pedidos/{pedido_id}/romaneio", 
              role="button", cls='btn-primary-custom'),
            A("✏️ Editar Pedido", href=f"/pedidos/editar/{pedido_id}", 
              role="button", cls="outline"),
            cls='card-custom'
        )
        
        return Title(f"Pedido {pedido[1]} - {APP_NAME}"), Container(
            header, info_pedido, tabela_itens, romaneio_section, botoes
        )
