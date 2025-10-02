# routes/clientes.py
"""Rotas de gestão de clientes"""
from fasthtml.common import *
from database.models import get_all_clientes, create_cliente
from database.models_extended import delete_cliente, get_cliente_by_id
from config import APP_NAME

def setup_clientes_routes(rt):
    @rt("/clientes")
    def get(sess):
        clientes = get_all_clientes()
        flash = sess.get('flash')  # não consome imediatamente para garantir exibição
        
        header = Div(
            Grid(
                H2("Clientes Cadastrados"),
                A("← Voltar", href="/", role="button", cls="outline"),
            ),
            cls='header-custom'
        )
        
        flash_div = Div(
            P(flash, style="margin:0; padding:0.5rem 1rem; background:#d4edda; color:#155724; border:1px solid #c3e6cb; border-radius:4px;")
            if flash else ''
        )

        if not clientes:
            tabela_content = P("Nenhum cliente cadastrado ainda.", style="color:#666; font-style:italic;")
        else:
            tabela_content = Table(
                Thead(Tr(Th("Nome"), Th("CPF/CNPJ"), Th("Telefone"), Th("Ações"))),
                Tbody(
                    *[Tr(
                        Td(c[1]),
                        Td(c[2] or '-'),
                        Td(c[3] or '-'),
                        Td(
                            A("Editar", href=f"/clientes/editar/{c[0]}", cls="outline"),
                            " ",
                            A("Excluir", href=f"/clientes/deletar/{c[0]}", 
                              onclick="return confirm('Tem certeza?')", cls="outline secondary")
                        )
                    ) for c in clientes]
                )
            )

        tabela = Div(
            tabela_content,
            cls='table-responsive'
        )
        
        btn_novo = A("➕ Novo Cliente", href="/clientes/novo", role="button", cls='btn-primary-custom')
        
        page = Container(
            header,
            Div(flash_div, btn_novo, tabela, cls='card-custom')
        )
        # Limpa flash após montar página
        if flash and 'flash' in sess:
            try:
                del sess['flash']
            except KeyError:
                pass
        return Title(f"Clientes - {APP_NAME}"), page

    @rt("/clientes/novo", methods=["GET"])
    def get():
        print("DEBUG: GET /clientes/novo handler")
        frm = Form(
            Fieldset(
                Label("Nome Completo", Input(name="nome", required=True)),
                Label("CPF/CNPJ", Input(name="cpf_cnpj", placeholder="000.000.000-00 ou 00.000.000/0000-00")),
                Label("Telefone", Input(name="telefone", type="tel", placeholder="(00) 00000-0000")),
                Label("Endereço", Textarea(name="endereco", rows=3)),
            ),
            Button("Salvar", type="submit", cls='btn-primary-custom'),
            A("Cancelar", href="/clientes", role="button", cls="outline secondary"),
            method="post", action="/clientes/novo"
        )
        
        return Title(f"Novo Cliente - {APP_NAME}"), Container(
            Div(H2("Cadastrar Cliente"), cls='header-custom'),
            Div(frm, cls='card-custom')
        )

    @rt("/clientes/novo", methods=["POST"])
    def post(sess, nome: str, cpf_cnpj: str = None, telefone: str = None, endereco: str = None):
        print("DEBUG: POST /clientes/novo handler - nome=", nome)
        try:
            create_cliente(nome, cpf_cnpj, telefone, endereco)
            sess['flash'] = 'Cliente cadastrado com sucesso.'
            print("DEBUG: Cliente cadastrado com sucesso")
        except Exception as e:  # pragma: no cover - raros casos de erro
            sess['flash'] = f'Erro ao cadastrar cliente: {e.__class__.__name__}'
            print("DEBUG: Erro ao cadastrar cliente:", e)
        return RedirectResponse('/clientes', status_code=303)
    
    @rt("/clientes/deletar/{cliente_id}")
    def get(cliente_id: int):
        delete_cliente(cliente_id)
        return RedirectResponse('/clientes', status_code=303)
