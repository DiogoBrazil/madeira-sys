# routes/auth_routes.py
"""Rotas de autenticação"""
from fasthtml.common import *
from dataclasses import dataclass
from database.models import get_user_by_credentials
from config import APP_NAME, APP_VERSION, APP_TAGLINE

def setup_auth_routes(rt):
    @rt("/login")
    def get():
        frm = Form(
            Div(
                Div(
                    Span("🌲 ", cls="logo"),
                    Span(APP_NAME, cls="logo"),
                    style="text-align: center; color: var(--primary-color); margin-bottom: 0.5rem;"
                ),
                P(APP_TAGLINE, style="text-align: center; color: #666; margin-top: 0;"),
                P(f"v{APP_VERSION}", cls="version", style="text-align: center; color: #999;"),
                Hr(),
                Input(id='email', name='email', type='email', placeholder='Email', required=True),
                Input(id='pwd', name='pwd', type='password', placeholder='Senha', required=True),
                Button('Entrar', cls='btn-primary-custom', style='width: 100%;'),
                P("Usuário padrão: admin@madeirasys.com / admin123", 
                  style="text-align: center; font-size: 0.8rem; color: #999; margin-top: 1rem;")
            ),
            action='/login', 
            method='post',
            cls='card-custom',
            style='max-width: 400px; margin: 5rem auto;'
        )
        return Title(f"{APP_NAME} - Login"), Main(frm, cls='container')

    @dataclass
    class Login:
        email: str
        pwd: str

    @rt("/login")
    def post(login: Login, sess):
        print(f"DEBUG: Login attempt - Email: {login.email}, Password: {login.pwd}")
        user = get_user_by_credentials(login.email, login.pwd)
        print(f"DEBUG: User found: {user}")
        
        if user:
            sess['auth'] = {
                'id': user[0],
                'nome': user[1],
                'is_admin': user[2]
            }
            print(f"DEBUG: Session set: {sess['auth']}")
            return RedirectResponse('/', status_code=303)
        
        print("DEBUG: Login failed, redirecting to /login")
        return RedirectResponse('/login', status_code=303)

    @rt("/logout")
    def get(sess):
        sess.clear()
        return RedirectResponse('/login', status_code=303)