import unittest
from analytics import CyberAnalytics
from datetime import datetime

class TestBlackWalletAnalytics(unittest.TestCase):

    def test_previsao_gastos_com_dados_reais(self):
        # Pegamos o mês e ano atual para o teste não quebrar nunca
        mes_atual = datetime.now().strftime("%m/%Y")
        
        # Cenário: Gastamos 100 reais no total em 2 dias.
        # Se forçarmos o 'dia_estudo' para 2, a média será 50/dia.
        # Em um mês de 30 dias (como Abril), 50 * 30 = 1500.
        historico_fake = [
            {"valor": -50.0, "data": f"01/{mes_atual}", "categoria": "TESTE"},
            {"valor": -50.0, "data": f"02/{mes_atual}", "categoria": "TESTE"}
        ]
        orcamento = 1000.0
        
        # AQUI ESTÁ O SEGREDO: Passamos o dia_estudo=2
        resultado = CyberAnalytics.prever_gastos(historico_fake, orcamento, dia_estudo=2)
        
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['projecao'], 1500.0)
        self.assertEqual(resultado['estouro'], 500.0)

    def test_previsao_sem_dados(self):
        resultado = CyberAnalytics.prever_gastos([], 1000.0)
        self.assertIsNone(resultado)

if __name__ == '__main__':
    unittest.main()