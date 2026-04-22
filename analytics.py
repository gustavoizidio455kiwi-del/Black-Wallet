import calendar
from datetime import datetime

class CyberAnalytics:
    """
    Motor Analítico: Responsável por processar dados brutos 
    e gerar insights, previsões e representações visuais.
    """

    @staticmethod
    def prever_gastos(historico: list, orcamento: float, dia_estudo=None) -> dict:
        """
        Calcula a tendência de gastos usando média móvel diária.
        """
        hoje = datetime.now()
        
        # Define o dia base: usa dia_estudo (testes) ou o dia real (uso diário)
        dia_atual = dia_estudo if dia_estudo else hoje.day
        ultimo_dia = calendar.monthrange(hoje.year, hoje.month)[1]
        
        # Filtra apenas gastos do mês atual (MM/AAAA)
        mes_atual_str = hoje.strftime("%m/%Y")
        gastos_mes = [abs(t['valor']) for t in historico 
                      if t['valor'] < 0 and t['data'][3:10] == mes_atual_str]
        
        # Proteção contra divisão por zero (dia 1º às 00:00) ou falta de dados
        if not gastos_mes or dia_atual <= 0:
            return None
        
        total_acumulado = sum(gastos_mes)
        media_diaria = total_acumulado / dia_atual
        projecao_final = media_diaria * ultimo_dia
        
        return {
            "media": media_diaria,
            "projecao": projecao_final,
            "estouro": projecao_final - orcamento if (orcamento > 0 and projecao_final > orcamento) else 0,
            "dias_restantes": ultimo_dia - dia_atual
        }

    @staticmethod
    def processar_distribuicao(historico: list) -> dict:
        """Agrupa gastos por categoria para o dashboard."""
        dist = {}
        for t in historico:
            if t['valor'] < 0:
                cat = t['categoria']
                dist[cat] = dist.get(cat, 0) + abs(t['valor'])
        return dist

    @staticmethod
    def processar_evolucao(historico: list) -> dict:
        """Agrupa gastos por mês/ano para análise de histórico."""
        evol = {}
        for t in historico:
            if t['valor'] < 0:
                mes_ano = t['data'][3:10]
                evol[mes_ano] = evol.get(mes_ano, 0) + abs(t['valor'])
        return dict(sorted(evol.items()))