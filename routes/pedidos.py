# routes/pedidos.py
"""Rotas de gestão de pedidos"""
from fasthtml.common import *
from datetime import datetime
from database.models import get_all_pedidos, get_all_clientes, create_pedido, create_item_pedido
from database.models_extended import get_pedido_by_id
from config import APP_NAME

def setup_pedidos_routes(rt):
    @rt("/pedidos")
    def get(sess):
        pedidos = get_all_pedidos()
        flash = sess.get('flash')
        
        header = Div(
            Grid(
                H2("Pedidos / Informes de Carga"),
                A("← Voltar", href="/", role="button", cls="outline"),
            ),
            cls='header-custom'
        )
        
        tabela = Table(
            Thead(Tr(
                Th("Código"), Th("Data"), Th("Cliente"), Th("Motorista"), 
                Th("Total m³"), Th("Valor Total"), Th("Ações")
            )),
            Tbody(
                *[Tr(
                    Td(p[1]), Td(p[2]), Td(p[3] or '-'), Td(p[4] or '-'),
                    Td(f"{p[5]:.2f}"), Td(f"R$ {p[6]:,.2f}"),
                    Td(
                        A("Ver", href=f"/pedidos/{p[0]}", cls="outline"),
                        " ",
                        A("Editar", href=f"/pedidos/editar/{p[0]}", cls="outline"),
                    )
                ) for p in pedidos]
            )
        )
        
        btn_novo = A("➕ Novo Pedido", href="/pedidos/novo", role="button", cls='btn-primary-custom')
        
        flash_div = Div(
            P(flash, style="margin:0; padding:0.5rem 1rem; background:#d4edda; color:#155724; border:1px solid #c3e6cb; border-radius:4px;")
            if flash else ''
        )
        page = Container(
            header,
            Div(flash_div, btn_novo, Div(tabela, cls='table-responsive'), cls='card-custom')
        )
        if flash and 'flash' in sess:
            try:
                del sess['flash']
            except KeyError:
                pass
        return Title(f"Pedidos - {APP_NAME}"), page

    @rt("/pedidos/novo", methods=["GET"])
    def get():
        print("DEBUG: GET /pedidos/novo handler")
        clientes = get_all_clientes()
        codigo_auto = f"PED{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        frm = Form(
            Fieldset(
                Grid(
                    Label("Código", Input(name="codigo", value=codigo_auto, required=True)),
                    Label("Data", Input(name="data", type="date", value=datetime.now().strftime('%Y-%m-%d'), required=True)),
                ),
                Grid(
                    Label("Representante", Input(name="representante", placeholder="Nome do representante")),
                    Label("Motorista", Input(name="motorista", placeholder="Nome do motorista")),
                ),
                Label("Cliente", 
                    Select(
                        Option("Selecione...", value=""),
                        *[Option(c[1], value=str(c[0])) for c in clientes],
                        name="cliente_id"
                    )
                ),
                Grid(
                    Label("Nota Fiscal", Input(name="nota_fiscal", placeholder="Número da NF")),
                    Label("Data da Nota", Input(name="data_nota", type="date")),
                ),
            ),
            H3("Itens do Pedido", style="margin-top: 2rem;"),
            Div(id="itens-container"),
            Button("➕ Adicionar Item", type="button", onclick="adicionarItem()", cls="outline"),
            Hr(),
            Button("Salvar Pedido", type="submit", cls='btn-primary-custom'),
            A("Cancelar", href="/pedidos", role="button", cls="outline secondary"),
            Script("""
                let itemCount = 0;
                function adicionarItem() {
                    itemCount++;
                    const container = document.getElementById('itens-container');
                    const itemHtml = `
                        <fieldset style=\"border: 1px solid #ddd; padding: 1rem; margin: 1rem 0; border-radius: 0.5rem;\">
                            <legend>Item ${itemCount}</legend>
                            <div class=\"grid\">
                                <label>Descrição
                                    <input name=\"item_descricao_${itemCount}\" required>
                                </label>
                                <label>Espessura (cm)
                                    <input name=\"item_espessura_${itemCount}\" type=\"number\" step=\"0.01\" value=\"0\" required>
                                </label>
                                <label>Largura (cm)
                                    <input name=\"item_largura_${itemCount}\" type=\"number\" step=\"0.01\" value=\"0\" required>
                                </label>
                            </div>
                            <div class=\"grid\">
                                <label>Comprimento (m)
                                    <input name=\"item_comprimento_${itemCount}\" type=\"number\" step=\"0.01\" value=\"0\" required>
                                </label>
                                <label>Quantidade (peças)
                                    <input name=\"item_qtdpecas_${itemCount}\" type=\"number\" step=\"1\" value=\"0\" required>
                                </label>
                                <label>Volume (m³)
                                    <input name=\"item_m3_${itemCount}\" type=\"number\" step=\"0.0001\" value=\"0.0000\" readonly>
                                </label>
                            </div>
                            <div class=\"grid\">
                                <label>Valor Unitário (R$)
                                    <input name=\"item_valor_unit_${itemCount}\" type=\"number\" step=\"0.01\" value=\"0\" required>
                                </label>
                                <label>Valor Total (R$)
                                    <input name=\"item_valor_total_${itemCount}\" type=\"number\" step=\"0.01\" value=\"0\" readonly>
                                </label>
                            </div>
                        </fieldset>
                    `;
                    container.insertAdjacentHTML('beforeend', itemHtml);
                    const esp = document.querySelector(`input[name=\"item_espessura_${itemCount}\"]`);
                    const larg = document.querySelector(`input[name=\"item_largura_${itemCount}\"]`);
                    const comp = document.querySelector(`input[name=\"item_comprimento_${itemCount}\"]`);
                    const qtdp = document.querySelector(`input[name=\"item_qtdpecas_${itemCount}\"]`);
                    const vol = document.querySelector(`input[name=\"item_m3_${itemCount}\"]`);
                    const vunit = document.querySelector(`input[name=\"item_valor_unit_${itemCount}\"]`);
                    const vtotal = document.querySelector(`input[name=\"item_valor_total_${itemCount}\"]`);
                    function recalc() {
                        const e = parseFloat(esp.value) || 0;
                        const l = parseFloat(larg.value) || 0;
                        const c = parseFloat(comp.value) || 0;
                        const q = parseInt(qtdp.value) || 0;
                        const volume = (e * l * c * q) / 10000;
                        vol.value = volume.toFixed(4);
                        const vu = parseFloat(vunit.value) || 0;
                        vtotal.value = (volume * vu).toFixed(2);
                    }
                    [esp, larg, comp, qtdp, vunit].forEach(inp => inp.addEventListener('input', recalc));
                    recalc();
                }
                adicionarItem();
            """),
            method="post", 
            action="/pedidos/novo"
        )
        
        return Title(f"Novo Pedido - {APP_NAME}"), Container(
            Div(H2("Novo Pedido / Informe de Carga"), cls='header-custom'),
            Div(frm, cls='card-custom')
        )

    @rt("/pedidos/novo", methods=["POST"])
    async def post(req, sess):
        print("DEBUG: POST /pedidos/novo handler")
        form_data = await req.form()
        
        codigo = form_data.get('codigo')
        data = form_data.get('data')
        representante = form_data.get('representante')
        cliente_id = form_data.get('cliente_id') or None
        motorista = form_data.get('motorista')
        nota_fiscal = form_data.get('nota_fiscal')
        data_nota = form_data.get('data_nota')
        
        total_m3 = 0.0
        valor_total = 0.0
        itens = []  # (descricao, volume_m3, valor_unitario, valor_total)

        i = 1
        while f'item_descricao_{i}' in form_data:
            descricao = form_data.get(f'item_descricao_{i}') or ''
            try:
                esp = float(form_data.get(f'item_espessura_{i}', 0) or 0)
                larg = float(form_data.get(f'item_largura_{i}', 0) or 0)
                comp = float(form_data.get(f'item_comprimento_{i}', 0) or 0)
                qtdp = int(form_data.get(f'item_qtdpecas_{i}', 0) or 0)
            except ValueError:
                esp = larg = comp = 0.0
                qtdp = 0
            volume_item = (esp * larg * comp * qtdp) / 10000 if (esp and larg and comp and qtdp) else 0.0
            valor_unit = float(form_data.get(f'item_valor_unit_{i}', 0) or 0)
            valor_item = round(volume_item * valor_unit, 2)

            total_m3 += volume_item
            valor_total += valor_item

            itens.append((descricao, round(volume_item, 4), valor_unit, valor_item))
            i += 1
        
        auth = sess.get('auth')
        usuario_id = auth['id'] if auth else None

        pedido_id = create_pedido(codigo, data, representante, cliente_id, motorista,
                                   nota_fiscal, data_nota, total_m3, valor_total, usuario_id)
        sess['flash'] = f'Pedido {codigo} criado com sucesso.'

        for item in itens:
            create_item_pedido(pedido_id, *item)

        return RedirectResponse('/pedidos', status_code=303)