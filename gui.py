import customtkinter as ctk
from PIL import Image
import os
import json
from datetime import datetime
from tkinter import messagebox

class CyberDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações de Janela
        self.title("BLACK WALLET v9.1 - TERMINAL OPERACIONAL")
        self.geometry("1100x700")
        self.configure(fg_color="#000000")
        
        self.path = os.path.dirname(__file__)
        self.data_file = os.path.join(self.path, "dados.json")
        
        # Inicialização de Variáveis
        self.user_name = "USUARIO_DESCONHECIDO"
        self.balance = 0.0
        self.transactions = []
        
        # Carrega dados ou inicia Configuração Inicial
        self.load_data_or_setup()

        # Layout Principal (Grid)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_sidebar()
        
        # Área de Conteúdo Principal
        self.main_view = ctk.CTkFrame(self, fg_color="transparent")
        self.main_view.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)
        
        self.setup_header()
        self.setup_balance_card()
        
        # Container de Logs (Histórico de Fluxo de Caixa)
        self.log_container = ctk.CTkScrollableFrame(self.main_view, fg_color="#050505", border_width=1, border_color="#111", height=350)
        self.log_container.pack(fill="both", expand=True, pady=20)
        
        self.update_log_display()

    def load_icon(self, name):
        try:
            img_path = os.path.join(self.path, "assets", name)
            img = Image.open(img_path).convert("RGBA")
            return ctk.CTkImage(light_image=img, dark_image=img, size=(22, 22))
        except:
            return None

    # --- PERSISTÊNCIA E CONFIGURAÇÃO ---
    def load_data_or_setup(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)
                self.user_name = data.get("user_name", "CONVIDADO")
                self.balance = data.get("balance", 0.0)
                self.transactions = data.get("transactions", [])
        else:
            self.first_setup()

    def first_setup(self):
        name = ctk.CTkInputDialog(text="Identifique o Operador do Sistema (Seu Nome):", title="INICIALIZAÇÃO").get_input()
        self.user_name = name.upper() if name else "CONVIDADO"
        
        saldo = ctk.CTkInputDialog(text="Insira o Saldo Atual ou Salário Base:", title="CAPITAL_INICIAL").get_input()
        try: self.balance = float(saldo) if saldo else 0.0
        except: self.balance = 0.0
        self.save_data()

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump({
                "user_name": self.user_name,
                "balance": self.balance,
                "transactions": self.transactions
            }, f)

    # --- MÓDULO DE IA (ANÁLISE) ---
    def run_ai_analysis(self):
        total_ganho = sum(t['valor'] for t in self.transactions if t['tipo'] == 'GANHO')
        total_gasto = sum(t['valor'] for t in self.transactions if t['tipo'] == 'GASTO')
        lucro_liquido = total_ganho - total_gasto
        
        status = "FLUXO_POSITIVO" if lucro_liquido >= 0 else "FLUXO_NEGATIVO"
        
        report = (
            f"--- [ RELATÓRIO DE ANÁLISE IA ] ---\n\n"
            f"OPERADOR: {self.user_name}\n"
            f"SALDO EM CONTA: R$ {self.balance:.2f}\n"
            f"LUCRO LÍQUIDO NO PERÍODO: R$ {lucro_liquido:.2f}\n"
            f"STATUS DO SISTEMA: {status}\n\n"
            f"PARECER: {'Integridade financeira mantida. Bom controle.' if lucro_liquido >= 0 else 'Alerta! Suas saídas estão superando as entradas extras.'}\n"
            f"------------------------------------"
        )
        messagebox.showinfo("NÚCLEO DE IA", report)

    # --- INTERFACE - SIDEBAR ---
    def setup_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=70, corner_radius=0, fg_color="#000000", border_width=1, border_color="#111")
        sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(sidebar, text="", image=self.load_icon("user.png")).pack(pady=30)
        
        # Botão IA
        ctk.CTkButton(sidebar, text="", image=self.load_icon("analysis.png"), width=40, 
                      fg_color="transparent", hover_color="#111", command=self.run_ai_analysis).pack(pady=15)
        
        # Botão Configurações
        ctk.CTkButton(sidebar, text="", image=self.load_icon("config.png"), width=40, 
                      fg_color="transparent", hover_color="#111", command=self.edit_settings).pack(side="bottom", pady=30)

    # --- INTERFACE - HEADER & CARDS ---
    def setup_header(self):
        header = ctk.CTkFrame(self.main_view, fg_color="transparent")
        header.pack(fill="x", pady=(0, 30))
        
        self.lbl_name = ctk.CTkLabel(header, text=f"OPERADOR // {self.user_name}", font=("Orbitron", 22, "bold"), text_color="#00FFFF")
        self.lbl_name.pack(side="left")
        
        # Botões de Entrada
        ctk.CTkButton(header, text="+ GANHO", font=("Orbitron", 11, "bold"), fg_color="#00FF00", text_color="#000", width=90,
                     command=lambda: self.new_entry("GANHO")).pack(side="right", padx=5)
        
        ctk.CTkButton(header, text="- GASTO", font=("Orbitron", 11, "bold"), fg_color="#FF0000", text_color="#000", width=90,
                     command=lambda: self.new_entry("GASTO")).pack(side="right", padx=5)

    def setup_balance_card(self):
        self.card = ctk.CTkFrame(self.main_view, fg_color="#050505", border_width=1, border_color="#00FFFF")
        self.card.pack(fill="x", ipady=20)
        self.lbl_balance = ctk.CTkLabel(self.card, text=f"R$ {self.balance:,.2f}", font=("Orbitron", 45, "bold"), text_color="#00FFFF")
        self.lbl_balance.pack()

    # --- LÓGICA DE TRANSAÇÕES ---
    def new_entry(self, tipo):
        desc = ctk.CTkInputDialog(text=f"Descrição do {tipo} (ex: Salário, Bico, Aluguel):", title="ENTRADA_DE_DADOS").get_input()
        if desc:
            val = ctk.CTkInputDialog(text=f"Valor do {tipo}:", title="ENTRADA_DE_DADOS").get_input()
            try:
                v = float(val)
                if tipo == "GANHO": self.balance += v
                else: self.balance -= v
                
                self.transactions.insert(0, {
                    "data": datetime.now().strftime("%d/%m"),
                    "desc": desc.upper(),
                    "valor": v,
                    "tipo": tipo
                })
                self.refresh_ui()
            except: pass

    # --- CONFIGURAÇÕES EM PORTUGUÊS ---
    def edit_settings(self):
        msg = (
            "ESCOLHA UMA OPÇÃO:\n"
            "1: MUDAR NOME DO OPERADOR\n"
            "2: REAJUSTAR SALDO TOTAL (SALÁRIO)\n"
            "3: RESET GERAL DO SISTEMA"
        )
        res = ctk.CTkInputDialog(text=msg, title="CONFIGURAÇÕES").get_input()
        
        if res == "1":
            n = ctk.CTkInputDialog(text="Digite o novo nome:", title="RENOMEAR").get_input()
            if n: self.user_name = n.upper()
        elif res == "2":
            val = ctk.CTkInputDialog(text="Digite o novo Saldo/Salário Base:", title="REAJUSTE").get_input()
            try: 
                self.balance = float(val)
                self.transactions.insert(0, {"data": datetime.now().strftime("%d/%m"), "desc": "AJUSTE_DE_SALDO", "valor": self.balance, "tipo": "SISTEMA"})
            except: pass
        elif res == "3":
            confirm = ctk.CTkInputDialog(text="Digite 'APAGAR' para zerar tudo:", title="PERIGO").get_input()
            if confirm == "APAGAR":
                self.balance = 0.0
                self.transactions = []
        
        self.lbl_name.configure(text=f"OPERADOR // {self.user_name}")
        self.refresh_ui()

    def refresh_ui(self):
        self.lbl_balance.configure(text=f"R$ {self.balance:,.2f}")
        self.save_data()
        self.update_log_display()

    def update_log_display(self):
        for w in self.log_container.winfo_children(): w.destroy()
        for t in self.transactions:
            row = ctk.CTkFrame(self.log_container, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=5)
            
            if t.get('tipo') == "GANHO": cor, simb = "#00FF00", "+"
            elif t.get('tipo') == "GASTO": cor, simb = "#FF4444", "-"
            else: cor, simb = "#00FFFF", "SET"

            ctk.CTkLabel(row, text=f"[{t['data']}]", text_color="#555", font=("Consolas", 12)).pack(side="left")
            ctk.CTkLabel(row, text=t['desc'], font=("Orbitron", 11), width=200, anchor="w").pack(side="left", padx=20)
            ctk.CTkLabel(row, text=f"{simb} R$ {t['valor']:,.2f}", font=("Orbitron", 12), text_color=cor).pack(side="left")
            
            ctk.CTkButton(row, text="", image=self.load_icon("trash.png"), width=30, fg_color="transparent", 
                          command=lambda x=t: self.delete_entry(x)).pack(side="right")

    def delete_entry(self, item):
        if item['tipo'] == "GANHO": self.balance -= item['valor']
        elif item['tipo'] == "GASTO": self.balance += item['valor']
        self.transactions.remove(item)
        self.refresh_ui()

if __name__ == "__main__":
    app = CyberDashboard()
    app.mainloop()