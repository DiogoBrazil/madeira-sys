# routes/usuarios.py
"""Rotas de gestão de usuários"""
from fasthtml.common import *
from database.models import get_all_users, create_user
from config import APP_NAME

def setup_usuarios_routes(rt):
    @rt("/usuarios")
    def get(sess):
        auth = sess.get('auth')
        if not auth.get('is_admin'):
            return RedirectResponse('/', status_code=303)
        
        usuarios = get_all_users()
        
        header = Div(
            Grid(
                H2("Usuários do Sistema"),
                A("← Voltar", href="/", role="button", cls="outline"),
            ),
            cls='header-custom'
        )
        
        tabela = Table(
            Thead(Tr(Th("Nome"), Th("Email"), Th("CPF"), Th("Telefone"), Th("Admin"), Th("Ações"))),
            Tbody(
                *[Tr(
                    Td(u[1]), Td(u[2]), Td(u[3]), Td(u[4] or '-'),
                    Td("Sim" if u[5] else "Não"),
                    Td(
                        A("Editar", href=f"/usuarios/editar/{u[0]}", cls="outline") if u[0] != 1 else "-"
                    )
                ) for u in usuarios]
            )
        )
        
        btn_novo = A("➕ Novo Usuário", href="/usuarios/novo", role="button", cls='btn-primary-custom')
        
        return Title(f"Usuários - {APP_NAME}"), Container(header, Div(btn_novo, tabela, cls='card-custom'))

    @rt("/usuarios/novo")
    def get(sess):
        auth = sess.get('auth')
        if not auth.get('is_admin'):
            return RedirectResponse('/', status_code=303)
        
        frm = Form(
            Fieldset(
                Label("Nome Completo", Input(name="nome_completo", required=True)),
                Grid(
                    Label("Email", Input(name="email", type="email", required=True)),
                    Label("CPF", Input(name="cpf", required=True, placeholder="000.000.000-00")),
                ),
                Grid(
                    Label("Telefone", Input(name="telefone", type="tel", placeholder="(00) 00000-0000")),
                    Label("Senha", Input(name="senha", type="password", required=True)),
                ),
                Label(
                    Input(type="checkbox", name="is_admin", value="1"),
                    "Usuário Administrador"
                ),
            ),
            Button("Salvar", type="submit", cls='btn-primary-custom'),
            A("Cancelar", href="/usuarios", role="button", cls="outline secondary"),
            method="post", action="/usuarios/novo"
        )
        
        return Title(f"Novo Usuário - {APP_NAME}"), Container(
            Div(H2("Cadastrar Usuário"), cls='header-custom'),
            Div(frm, cls='card-custom')
        )

    @rt("/usuarios/novo")
    def post(nome_completo: str, email: str, cpf: str, telefone: str = None, 
             senha: str = "123456", is_admin: int = 0):
        create_user(nome_completo, email, cpf, telefone, senha, is_admin)
        return RedirectResponse('/usuarios', status_code=303)
