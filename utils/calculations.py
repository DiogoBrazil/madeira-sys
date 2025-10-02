# utils/calculations.py
"""Funções de cálculo para madeira"""

def calcular_m3(espessura_cm, largura_cm, comprimento_m, quantidade):
    """
    Calcula o volume em m³ de madeira
    Fórmula: (Espessura em cm × Largura em cm × Comprimento em m × Quantidade) / 10000
    """
    try:
        espessura = float(espessura_cm) if espessura_cm else 0
        largura = float(largura_cm) if largura_cm else 0
        comprimento = float(comprimento_m) if comprimento_m else 0
        qtd = int(quantidade) if quantidade else 0
        
        m3 = (espessura * largura * comprimento * qtd) / 10000
        return round(m3, 4)
    except:
        return 0