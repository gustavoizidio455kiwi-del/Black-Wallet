import os
from datetime import datetime
from database import WalletDAO
from analytics import CyberAnalytics
from logger_config import setup_logger # Nossa auditoria de segurança

# Inicializa o logger para este módulo
log = setup_logger("Interface")

class BlackWalletUI:
    def __init__(self):
        try:
            self.db = WalletDAO()
            self.dados = self.db.carregar()
            log.info("Sessão iniciada com sucesso.")
        except Exception as e:
            log.critical(f"Falha ao iniciar banco de dados: {e}")
            print("\033[0;31m✘ ERRO CRÍTICO: Não foi possível carregar os dados.\033[0m")
            exit()
        
        self.cores = {
            'reset': '\033[0m', 
            'cyber': '\033[1;36m', 
            'red': '\033[0;31m',
            'green': '\033[0;32m'
        }

    # --- MELHORIA 1: VALIDAÇÃO DE ENTRADA ---
    def ler_float(self, msg):
        """Impede que o programa feche se o usuário digitar letras no valor."""
        while True:
            try:
                entrada = input(msg).replace(',', '.')
                return float(entrada)
            except ValueError:
                log.warning(f"Tentativa de input inválido: '{entrada}'")
                print(f"{self.cores['red']}✘ Erro: Digite um valor numérico (Ex: 50.00){self.cores['reset']}")

    def logo(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        saldo = sum(t['valor'] for t in self.dados['historico'])
        print(f"{self.cores['cyber']}=== BLACK WALLET CYBER-SEC EDITION ==={self.cores['reset']}")
        print(f"Status: {self.cores['green']}Cofre Criptografado{self.cores['reset']} | Log: {self.cores['green']}Ativo{self.cores['reset']}")
        print(f"Saldo Total: R$ {saldo:.2f}")
        print("-" * 55)

    def menu(self):
        while True:
            self.logo()
            print("1. [+/-] Novo Lançamento")
            print("2. [DSH] Dashboard Visual")
            print("3. [IA ] Previsão de Gastos")
            print("4. [SET] Configurar Orçamento")
            print("0. [OFF] Sair")
            
            op = input(f"\n{self.cores['cyber']}Seleção > {self.cores['reset']}")
            
            if op == '1':
                v = self.ler_float("Valor: R$ ")
                cat = input("Categoria: ").upper() or "GERAL"
                desc = input("Descrição: ") or "Lançamento"
                
                nova_transacao = {
                    "id": len(self.dados["historico"]) + 1,
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "valor": -abs(v), # Tratamos como gasto por padrão
                    "categoria": cat,
                    "descricao": desc
                }
                
                self.dados["historico"].append(nova_transacao)
                self.db.salvar(self.dados)
                log.info(f"Transação registrada: ID {nova_transacao['id']} - R$ {v}")
                
            elif op == '2':
                log.info("Acessou Dashboard.")
                gastos = CyberAnalytics.processar_distribuicao(self.dados['historico'])
                if not gastos:
                    print("Nenhum dado para exibir.")
                else:
                    total = sum(gastos.values())
                    for c, v in sorted(gastos.items(), key=lambda x: x[1], reverse=True):
                        perc = (v/total)*100
                        print(f"{c:12} | R$ {v:>8.2f} ({perc:>5.1f}%)")
                input("\nEnter para voltar...")

            elif op == '3':
                log.info("Acessou IA Preditiva.")
                res = CyberAnalytics.prever_gastos(self.dados['historico'], self.dados['orcamento_mensal'])
                if res:
                    print(f"\nMédia Diária: R$ {res['media']:.2f}")
                    print(f"Projeção Final: R$ {res['projecao']:.2f}")
                    if res['estouro'] > 0:
                        print(f"{self.cores['red']}⚠ ALERTA: Projeção excede orçamento em R$ {res['estouro']:.2f}{self.cores['reset']}")
                else:
                    print("Dados insuficientes para calcular previsão.")
                input("\nEnter para voltar...")

            elif op == '4':
                limite = self.ler_float("Novo limite mensal: R$ ")
                self.dados['orcamento_mensal'] = limite
                self.db.salvar(self.dados)
                log.info(f"Orçamento mensal alterado para: R$ {limite}")

            elif op == '0':
                log.info("Sistema encerrado.")
                break

if __name__ == "__main__":
    BlackWalletUI().menu()