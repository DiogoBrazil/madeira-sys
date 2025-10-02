# auth/middleware.py
"""Middleware de autenticação"""
from fasthtml.common import RedirectResponse, Beforeware

def auth_before(req, sess):
    """Verifica autenticação antes de processar rotas"""
    auth = req.scope['auth'] = sess.get('auth', None)
    if not auth and req.url.path not in ['/login', '/favicon.ico']:
        return RedirectResponse('/login', status_code=303)

# Criar middleware
bware = Beforeware(auth_before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', '/login'])