"""
Ponto de entrada principal da aplicação GastoJa.
Gerencia a janela principal, navegação temporal e inicialização de dependências.
"""

import customtkinter as ctk
from datetime import datetime
from dateutil.relativedelta import relativedelta

from core.database import DatabaseManager
from views.dashboard import ViewDashboard

# Constantes de paleta de cores globais
BG_COLOR = "#120d0a"
FRAME_COLOR = "#211712"
TEXT_COLOR = "#e6d5c3"
ACCENT_COLOR = "#c2753e"


class GastoJaMain:
    """
    Classe raiz da aplicação.
    Responsável por instanciar a interface, gerenciar a conexão com o banco de dados
    e controlar o estado global de visualização por data.
    """

    def __init__(self, root):
        """Inicializa os componentes core e as configurações da janela principal."""
        self.root = root
        self.root.title("GastoJa - v2.0 (Hub Edition)")
        self.root.geometry("1100x700")
        self.root.configure(fg_color=BG_COLOR)
        
        self.db = DatabaseManager()
        self.data_visualizacao = datetime.now()
        
        self.construir_header_tempo()
        self.construir_hub_central()
        
        self.atualizar_hub()

    def construir_header_tempo(self):
        """Constrói o header de navegação para seleção de mês e ano."""
        self.frame_tempo = ctk.CTkFrame(self.root, fg_color=FRAME_COLOR, corner_radius=10)
        self.frame_tempo.pack(fill="x", padx=20, pady=15)
        
        btn_voltar = ctk.CTkButton(self.frame_tempo, text="<", width=40, fg_color=BG_COLOR, hover_color=ACCENT_COLOR, command=self.mes_anterior)
        btn_voltar.pack(side="left", padx=15, pady=10)
        
        self.lbl_mes_ano = ctk.CTkLabel(self.frame_tempo, text="Mês Ano", font=("Consolas", 18, "bold"), text_color=ACCENT_COLOR)
        self.lbl_mes_ano.pack(side="left", expand=True)
        
        btn_avancar = ctk.CTkButton(self.frame_tempo, text=">", width=40, fg_color=BG_COLOR, hover_color=ACCENT_COLOR, command=self.mes_proximo)
        btn_avancar.pack(side="right", padx=15, pady=10)

    def construir_hub_central(self):
        """Inicializa o container principal e monta a view do Dashboard."""
        self.container_hub = ctk.CTkFrame(self.root, fg_color="transparent")
        self.container_hub.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.view_dashboard = ViewDashboard(self.container_hub, self)

    def mes_anterior(self):
        """Decrementa a data de visualização atual em um mês e atualiza a interface."""
        self.data_visualizacao -= relativedelta(months=1)
        self.atualizar_hub()

    def mes_proximo(self):
        """Incrementa a data de visualização atual em um mês e atualiza a interface."""
        self.data_visualizacao += relativedelta(months=1)
        self.atualizar_hub()

    def atualizar_hub(self):
        """Atualiza o label do header e dispara o refresh de dados na view ativa."""
        meses = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        
        texto = f"{meses[self.data_visualizacao.month - 1]}  {self.data_visualizacao.year}"
        self.lbl_mes_ano.configure(text=texto)
        
        if hasattr(self, 'view_dashboard'):
            self.view_dashboard.atualizar_dados()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    app = GastoJaMain(root)
    root.mainloop()