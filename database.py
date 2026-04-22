import json
import os
from security import CyberVault

class WalletDAO:
    def __init__(self, arquivo="wallet.bw", senha="admin"):
        self.arquivo = arquivo
        self.senha = senha

    def salvar(self, dados):
        """Criptografa e salva os dados no disco."""
        dados_json = json.dumps(dados)
        encrypted = CyberVault.criptografar(dados_json, self.senha)
        with open(self.arquivo, "wb") as f:
            f.write(encrypted)

    def carregar(self):
        """Carrega e descriptografa o histórico completo."""
        if not os.path.exists(self.arquivo):
            return {"historico": [], "orcamento_mensal": 2000.0}
        with open(self.arquivo, "rb") as f:
            encrypted = f.read()
        try:
            decrypted = CyberVault.descriptografar(encrypted, self.senha)
            return json.loads(decrypted)
        except:
            return {"historico": [], "orcamento_mensal": 2000.0}

    def get_saldo_rapido(self):
        """Calcula o saldo somando as transações sem carregar a interface."""
        dados = self.carregar()
        return sum(t['valor'] for t in dados['historico'])

    def atualizar_transacao(self, transacao_id, novo_valor, nova_cat):
        """Edita um gasto existente pelo ID."""
        dados = self.carregar()
        for t in dados['historico']:
            if t['id'] == transacao_id:
                t['valor'] = -abs(float(novo_valor))
                t['categoria'] = nova_cat.upper()
                break
        self.salvar(dados)

    def excluir_transacao(self, transacao_id):
        """Remove um gasto do histórico."""
        dados = self.carregar()
        dados['historico'] = [t for t in dados['historico'] if t['id'] != transacao_id]
        self.salvar(dados)