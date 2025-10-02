# utils/validators.py
"""Funções de validação"""
import re

def validar_cpf(cpf):
    """Validação básica de CPF"""
    cpf = re.sub(r'\D', '', cpf)
    return len(cpf) == 11

def validar_cnpj(cnpj):
    """Validação básica de CNPJ"""
    cnpj = re.sub(r'\D', '', cnpj)
    return len(cnpj) == 14