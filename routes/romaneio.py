# routes/romaneio.py
"""Rotas para gestão de romaneio (detalhamento de peças)"""
from fasthtml.common import *
from database.models_extended import get_pedido_by_id, create_romaneio_item
from utils.calculations import calcular_m3
from config import APP_NAME

def setup_romaneio_routes(rt):
    @rt("/pedidos/{pedido_id}/romaneio")
    def get(pedido_id: int):
        dados = get_pedido_by_id(pedido_id)
        pedido = dados['pedido']
        
        if not pedido:
            return RedirectResponse('/pedidos', status_code=303)
        
        header = Div(
            Grid(
                H2(f"Adicionar Romaneio - Pedido {pedido[1]}"),
                A("← Voltar", href=f"/pedidos/{pedido_id}", role="button", cls="outline"),
            ),
            cls='header-custom'
        )
        
        # Opções de essências comuns
        essencias = [
            "Pinus", "Eucalipto", "Cedro", "Ipê", "Jatobá", 
            "Peroba", "Mogno", "Cumaru", "Teca", "Outra"
        ]
        
        frm = Form(
            Fieldset(
                Label("Essência", 
                    Select(
                        *[Option(e, value=e) for e in essencias],
                        name="essencia",
                        required=True
                    )
                ),
                Grid(
                    Label("Espessura (cm)", 
                        Input(name="espessura", type="number", step="0.01", 
                              required=True, id="espessura")
                    ),
                    Label("Largura (cm)", 
                        Input(name="largura", type="number", step="0.01", 
                              required=True, id="largura")
                    ),
                ),
                Grid(
                    Label("Comprimento (m)", 
                        Input(name="comprimento", type="number", step="0.01", 
                              required=True, id="comprimento")
                    ),
                    Label("Quantidade (peças)", 
                        Input(name="quantidade", type="number", 
                              required=True, id="quantidade")
                    ),
                ),
                Div(
                    Label("Volume Total (m³)", 
                        Input(name="m3_total", type="number", step="0.0001", 
                              readonly=True, id="m3_total", value="0.0000")
                    ),
                    Label("Percentual do Pedido (%)", 
                        Input(name="percentual", type="number", step="0.01", 
                              readonly=True, id="percentual", value="0.00")
                    ),
                    cls="grid"
                ),
            ),
            Button("Adicionar ao Romaneio", type="submit", cls='btn-primary-custom'),
            A("Cancelar", href=f"/pedidos/{pedido_id}", role="button", cls="outline secondary"),
            Script(f"""
                const totalPedido = {pedido[8]};  // total_m3 do pedido
                
                function calcularM3() {{
                    const espessura = parseFloat(document.getElementById('espessura').value) || 0;
                    const largura = parseFloat(document.getElementById('largura').value) || 0;
                    const comprimento = parseFloat(document.getElementById('comprimento').value) || 0;
                    const quantidade = parseInt(document.getElementById('quantidade').value) || 0;
                    
                    // Fórmula: (Espessura × Largura × Comprimento × Quantidade) / 10000
                    const m3 = (espessura * largura * comprimento * quantidade) / 10000;
                    document.getElementById('m3_total').value = m3.toFixed(4);
                    
                    // Calcular percentual
                    if (totalPedido > 0) {{
                        const percentual = (m3 / totalPedido) * 100;
                        document.getElementById('percentual').value = percentual.toFixed(2);
                    }}
                }}
                
                // Adicionar event listeners
                ['espessura', 'largura', 'comprimento', 'quantidade'].forEach(id => {{
                    document.getElementById(id).addEventListener('input', calcularM3);
                }});
            """),
            method="post", 
            action=f"/pedidos/{pedido_id}/romaneio"
        )
        
        return Title(f"Romaneio - Pedido {pedido[1]} - {APP_NAME}"), Container(
            header,
            Div(frm, cls='card-custom')
        )
    
    @rt("/pedidos/{pedido_id}/romaneio")
    def post(pedido_id: int, essencia: str, espessura: float, largura: float, 
             comprimento: float, quantidade: int, m3_total: float, percentual: float):
        
        # Salvar item do romaneio
        create_romaneio_item(pedido_id, essencia, espessura, largura, 
                           comprimento, quantidade, m3_total, percentual)
        
        # Redirecionar para a visualização do pedido
        return RedirectResponse(f'/pedidos/{pedido_id}', status_code=303)
