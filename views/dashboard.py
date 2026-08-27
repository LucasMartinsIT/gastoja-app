"""
Módulo principal de visualização da aplicação GastoJa.
Contém a classe ViewDashboard, responsável por renderizar a interface central (Hub),
painéis de resumo financeiro, projeções de caixa e tabelas de log.
"""

import customtkinter as ctk
from tkinter import ttk
from views.modais import ModalGasto, ModalReceita, ModalCofres, ModalEscudo

# Constantes de paleta de cores globais
BG_COLOR = "#120d0a"        
FRAME_COLOR = "#211712"     
TEXT_COLOR = "#e6d5c3"      
ACCENT_COLOR = "#c2753e"    
SUCCESS_COLOR = "#4d734d"
DANGER_COLOR = "#8f3333"
INFO_COLOR = "#2d5a88"

# Constantes tipográficas
FONT_MAIN = ("Consolas", 12)
FONT_TITLE = ("Consolas", 18, "bold")
FONT_GIANT = ("Consolas", 28, "bold")
FONT_TABLE = ("Consolas", 14) 
FONT_TABLE_HEAD = ("Consolas", 14, "bold") 


class ViewDashboard:
    """
    Controlador da interface principal (Dashboard).
    Gerencia a exibição dos componentes visuais, integra-se com o banco de dados
    para atualização em tempo real e processa cálculos de fluxo de caixa e projeções.
    """

    def __init__(self, parent, app_core):
        self.parent = parent
        self.app = app_core
        self.construir_painel()

    def construir_painel(self):
        """Constrói e posiciona todos os widgets que compõem o Dashboard."""
        
        # Barra superior de ações e atalhos
        self.frame_acoes = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.frame_acoes.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkButton(self.frame_acoes, text="➕ Lançar Dano", font=FONT_TITLE, fg_color=DANGER_COLOR, hover_color="#6b2626", height=40, command=self.abrir_modal_gasto).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(self.frame_acoes, text="➕ Adicionar HP", font=FONT_TITLE, fg_color=SUCCESS_COLOR, hover_color="#3a593a", height=40, command=self.abrir_modal_receita).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(self.frame_acoes, text="⚙️ Cofres & Tags", font=FONT_TITLE, fg_color=FRAME_COLOR, hover_color=ACCENT_COLOR, text_color=TEXT_COLOR, height=40, border_width=1, border_color=ACCENT_COLOR, command=self.abrir_modal_cofres).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(self.frame_acoes, text="🛡️ Escudo", font=FONT_TITLE, fg_color="#d6a848", hover_color="#b58a33", text_color=BG_COLOR, height=40, command=self.abrir_modal_escudo).pack(side="left", expand=True, padx=5)

        # Container rolável central
        self.scroll_hub = ctk.CTkScrollableFrame(self.parent, fg_color="transparent")
        self.scroll_hub.pack(fill="both", expand=True, padx=10, pady=5)

        # Painel primário: Saldo Livre (HP) e Cheque Especial (Escudo)
        self.frame_resumo = ctk.CTkFrame(self.scroll_hub, fg_color=FRAME_COLOR, corner_radius=15)
        self.frame_resumo.pack(fill="x", pady=10, padx=10)
        
        self.label_titulo_saldo = ctk.CTkLabel(self.frame_resumo, text="HP Restante (Saldo Livre)", font=FONT_MAIN, text_color=TEXT_COLOR)
        self.label_titulo_saldo.pack(pady=(15, 0))
        
        self.lbl_saldo_valor = ctk.CTkLabel(self.frame_resumo, text="R$ 0.00", font=FONT_GIANT, text_color=INFO_COLOR)
        self.lbl_saldo_valor.pack(pady=(5, 10))

        self.barra_vida = ctk.CTkProgressBar(self.frame_resumo, height=20, corner_radius=10, fg_color=BG_COLOR, progress_color=INFO_COLOR)
        self.barra_vida.set(1.0)
        self.barra_vida.pack(fill="x", padx=40, pady=(0, 10))

        self.label_titulo_escudo = ctk.CTkLabel(self.frame_resumo, text="Escudo (Cheque Especial): R$ 0.00", font=FONT_MAIN, text_color="#d6a848")
        self.label_titulo_escudo.pack(pady=(5, 0))
        
        self.barra_escudo = ctk.CTkProgressBar(self.frame_resumo, height=12, corner_radius=10, fg_color=BG_COLOR, progress_color="#d6a848")
        self.barra_escudo.set(1.0)
        self.barra_escudo.pack(fill="x", padx=60, pady=(5, 15))

        # Grid de cards analíticos secundários
        self.frame_cards = ctk.CTkFrame(self.scroll_hub, fg_color="transparent")
        self.frame_cards.pack(fill="x", pady=5, padx=5)

        self.card_hp = self.criar_card_simples(self.frame_cards, "Receitas do Mês", "R$ 0.00", SUCCESS_COLOR)
        
        # Card analítico: Projeção de Custo Fixo
        frame_fixo = ctk.CTkFrame(self.frame_cards, fg_color=FRAME_COLOR, corner_radius=10)
        frame_fixo.pack(side="left", expand=True, fill="both", padx=5)
        
        ctk.CTkLabel(frame_fixo, text="Gasto Fixo Mensal", font=FONT_MAIN, text_color=TEXT_COLOR).pack(pady=(10, 0))
        self.lbl_custo_fixo = ctk.CTkLabel(frame_fixo, text="R$ 0.00", font=("Consolas", 18, "bold"), text_color="#d6a848")
        self.lbl_custo_fixo.pack(pady=(0, 2))
        
        self.lbl_sobra_fixo = ctk.CTkLabel(frame_fixo, text="Sobra: R$ 0.00", font=("Consolas", 11), text_color=SUCCESS_COLOR)
        self.lbl_sobra_fixo.pack(pady=(0, 5))

        frame_switches = ctk.CTkFrame(frame_fixo, fg_color="transparent")
        frame_switches.pack(pady=(0, 10))

        self.var_fixos = ctk.BooleanVar(value=True)
        self.var_assinaturas = ctk.BooleanVar(value=True)
        self.var_parcelas = ctk.BooleanVar(value=True)

        ctk.CTkSwitch(frame_switches, text="Fixos", variable=self.var_fixos, font=("Consolas", 10), command=self.atualizar_dados, progress_color=ACCENT_COLOR).pack(anchor="w", pady=1)
        ctk.CTkSwitch(frame_switches, text="Assinaturas", variable=self.var_assinaturas, font=("Consolas", 10), command=self.atualizar_dados, progress_color=ACCENT_COLOR).pack(anchor="w", pady=1)
        ctk.CTkSwitch(frame_switches, text="Parcelas", variable=self.var_parcelas, font=("Consolas", 10), command=self.atualizar_dados, progress_color=ACCENT_COLOR).pack(anchor="w", pady=1)

        # Card analítico: Projeção de Caixa por Data
        frame_prev = ctk.CTkFrame(self.frame_cards, fg_color=FRAME_COLOR, corner_radius=10)
        frame_prev.pack(side="left", expand=True, fill="both", padx=5)

        ctk.CTkLabel(frame_prev, text="Saldo até o Dia:", font=FONT_MAIN, text_color=TEXT_COLOR).pack(pady=(10, 0))

        row_prev = ctk.CTkFrame(frame_prev, fg_color="transparent")
        row_prev.pack(pady=2)

        self.entry_dia_prev = ctk.CTkEntry(row_prev, width=35, height=25)
        self.entry_dia_prev.insert(0, "22")
        self.entry_dia_prev.pack(side="left", padx=5)
        
        ctk.CTkButton(row_prev, text="Ver", width=35, height=25, fg_color=INFO_COLOR, command=self.calcular_previsao).pack(side="left")

        self.lbl_valor_prev = ctk.CTkLabel(frame_prev, text="R$ 0.00", font=("Consolas", 18, "bold"), text_color=INFO_COLOR)
        self.lbl_valor_prev.pack(pady=(0, 5))

        frame_switches_prev = ctk.CTkFrame(frame_prev, fg_color="transparent")
        frame_switches_prev.pack(pady=(0, 10))

        self.prev_var_fixos = ctk.BooleanVar(value=True)
        self.prev_var_assinaturas = ctk.BooleanVar(value=True)
        self.prev_var_parcelas = ctk.BooleanVar(value=True)

        ctk.CTkSwitch(frame_switches_prev, text="Abater Fixos", variable=self.prev_var_fixos, font=("Consolas", 10), command=self.calcular_previsao, progress_color=INFO_COLOR).pack(anchor="w", pady=1)
        ctk.CTkSwitch(frame_switches_prev, text="Abater Assin.", variable=self.prev_var_assinaturas, font=("Consolas", 10), command=self.calcular_previsao, progress_color=INFO_COLOR).pack(anchor="w", pady=1)
        ctk.CTkSwitch(frame_switches_prev, text="Abater Parc.", variable=self.prev_var_parcelas, font=("Consolas", 10), command=self.calcular_previsao, progress_color=INFO_COLOR).pack(anchor="w", pady=1)

        self.card_dano = self.criar_card_simples(self.frame_cards, "Dano Total", "R$ 0.00", DANGER_COLOR)

        # Estilização do Treeview (Tabelas)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=FRAME_COLOR, foreground=TEXT_COLOR, rowheight=35, fieldbackground=FRAME_COLOR, font=FONT_TABLE)
        style.map('Treeview', background=[('selected', ACCENT_COLOR)])
        style.configure("Treeview.Heading", background=BG_COLOR, foreground=ACCENT_COLOR, font=FONT_TABLE_HEAD)

        # Tabela: Histórico de Receitas
        frame_tab_rec = ctk.CTkFrame(self.scroll_hub, fg_color="transparent")
        frame_tab_rec.pack(fill="x", pady=(20, 5), padx=10)
        ctk.CTkLabel(frame_tab_rec, text="Histórico de Receitas (HP)", font=FONT_TITLE, text_color=SUCCESS_COLOR).pack(anchor="w")
        
        colunas_rec = ("ID", "Data", "Descrição", "Valor", "Tipo", "Dia Fixo")
        self.tree_receitas = ttk.Treeview(frame_tab_rec, columns=colunas_rec, show="headings", height=4)
        for col in colunas_rec: self.tree_receitas.heading(col, text=col)
        self.tree_receitas.column("ID", width=0, stretch=False)
        self.tree_receitas.column("Data", width=110, anchor="center")
        self.tree_receitas.column("Descrição", width=250)
        self.tree_receitas.column("Valor", width=120, anchor="center")
        self.tree_receitas.column("Tipo", width=120, anchor="center")
        self.tree_receitas.column("Dia Fixo", width=100, anchor="center")
        self.tree_receitas.pack(fill="x", pady=5)
        
        ctk.CTkButton(frame_tab_rec, text="🗑️ Excluir Receita", fg_color="transparent", border_width=1, border_color=DANGER_COLOR, text_color=DANGER_COLOR, hover_color="#3d1818", command=self.excluir_receita).pack(anchor="e")

        # Tabela: Histórico de Gastos
        frame_tab_gas = ctk.CTkFrame(self.scroll_hub, fg_color="transparent")
        frame_tab_gas.pack(fill="x", pady=(20, 20), padx=10)
        ctk.CTkLabel(frame_tab_gas, text="Histórico de Danos (Gastos)", font=FONT_TITLE, text_color=DANGER_COLOR).pack(anchor="w")
        
        colunas_gas = ("ID", "Data", "Descrição", "Valor", "Tipo", "Tag", "Banco", "Detalhes")
        self.tree_gastos = ttk.Treeview(frame_tab_gas, columns=colunas_gas, show="headings", height=8)
        for col in colunas_gas: self.tree_gastos.heading(col, text=col)
        self.tree_gastos.column("ID", width=0, stretch=False)
        self.tree_gastos.column("Data", width=110, anchor="center")
        self.tree_gastos.column("Descrição", width=250)
        self.tree_gastos.column("Valor", width=120, anchor="center")
        self.tree_gastos.column("Tipo", width=120, anchor="center")
        self.tree_gastos.column("Tag", width=120, anchor="center")
        self.tree_gastos.column("Banco", width=120, anchor="center")
        self.tree_gastos.column("Detalhes", width=100, anchor="center")
        self.tree_gastos.pack(fill="x", pady=5)
        
        ctk.CTkButton(frame_tab_gas, text="🗑️ Excluir Gasto", fg_color="transparent", border_width=1, border_color=DANGER_COLOR, text_color=DANGER_COLOR, hover_color="#3d1818", command=self.excluir_gasto).pack(anchor="e")

    def criar_card_simples(self, master, titulo, valor, cor):
        """Método auxiliar para instanciar cards de resumo padronizados."""
        frame = ctk.CTkFrame(master, fg_color=FRAME_COLOR, corner_radius=10)
        frame.pack(side="left", expand=True, fill="both", padx=5)
        ctk.CTkLabel(frame, text=titulo, font=FONT_MAIN, text_color=TEXT_COLOR).pack(pady=(15, 5))
        lbl_valor = ctk.CTkLabel(frame, text=valor, font=("Consolas", 20, "bold"), text_color=cor)
        lbl_valor.pack(pady=(0, 15))
        return lbl_valor

    def atualizar_dados(self):
        """
        Recupera as informações do banco de dados relativas ao mês em visualização,
        processa as regras de negócio de custo fixo e escudo, e atualiza a interface.
        """
        mes_alvo = self.app.data_visualizacao.strftime("%Y-%m")

        # Limpeza de views antigas
        for item in self.tree_receitas.get_children(): self.tree_receitas.delete(item)
        for item in self.tree_gastos.get_children(): self.tree_gastos.delete(item)

        receitas, total_hp = self.app.db.obter_receitas_do_mes(mes_alvo)
        gastos = self.app.db.obter_gastos_do_mes(mes_alvo)
        total_dano = sum(g[2] for g in gastos)
        saldo = total_hp - total_dano

        # Processamento do agrupamento de custo fixo com base no estado dos switches
        incluir_fixos = self.var_fixos.get()
        incluir_assinaturas = self.var_assinaturas.get()
        incluir_parcelas = self.var_parcelas.get()
        
        custo_fixo = 0.0
        for g in gastos:
            tipo = g[3]
            valor = g[2]
            if tipo == "Fixo" and incluir_fixos: custo_fixo += valor
            elif tipo == "Assinatura" and incluir_assinaturas: custo_fixo += valor
            elif tipo == "Parcelado" and incluir_parcelas: custo_fixo += valor
                
        sobra_fixa = total_hp - custo_fixo

        # Atualização dos labels numéricos
        self.card_hp.configure(text=f"R$ {total_hp:.2f}")
        self.card_dano.configure(text=f"R$ {total_dano:.2f}")
        self.lbl_custo_fixo.configure(text=f"R$ {custo_fixo:.2f}")
        
        cor_sobra = SUCCESS_COLOR if sobra_fixa >= 0 else DANGER_COLOR
        self.lbl_sobra_fixo.configure(text=f"Sobra: R$ {sobra_fixa:.2f}", text_color=cor_sobra)

        # Recuperação do limite consolidado (Cheque Especial)
        conn = self.app.db.conectar()
        try:
            cursor = conn.execute("SELECT SUM(limite) FROM bancos")
            total_escudo = cursor.fetchone()[0] or 0.0
        except:
            total_escudo = 0.0
        finally:
            conn.close()

        # Renderização visual das barras de HP e Escudo
        if saldo >= 0:
            self.lbl_saldo_valor.configure(text=f"R$ {saldo:.2f}", text_color=INFO_COLOR)
            self.barra_vida.configure(progress_color=INFO_COLOR)
            percentual = saldo / total_hp if total_hp > 0 else 1.0
            self.barra_vida.set(percentual)
            self.label_titulo_escudo.configure(text=f"Escudo (Cheque Especial): R$ {total_escudo:.2f}", text_color="#d6a848")
            self.barra_escudo.set(1.0)
        else:
            self.lbl_saldo_valor.configure(text=f"- R$ {abs(saldo):.2f}", text_color=DANGER_COLOR)
            self.barra_vida.configure(progress_color=DANGER_COLOR)
            self.barra_vida.set(0.0) 
            
            if total_escudo > 0:
                escudo_restante = total_escudo + saldo 
                if escudo_restante >= 0:
                    self.label_titulo_escudo.configure(text=f"Escudo Ativo! Resta: R$ {escudo_restante:.2f}", text_color="#d6a848")
                    self.barra_escudo.set(escudo_restante / total_escudo)
                else:
                    self.label_titulo_escudo.configure(text=f"ESCUDO ROMPIDO! Dano Crítico: R$ {abs(escudo_restante):.2f}", text_color=DANGER_COLOR)
                    self.barra_escudo.set(0.0)
            else:
                self.label_titulo_escudo.configure(text="Sem Escudo!", text_color=DANGER_COLOR)
                self.barra_escudo.set(0.0)

        # População dos datagrids
        for r in receitas:
            self.tree_receitas.insert("", "end", values=(r[0], r[6], r[1], f"R$ {r[2]:.2f}", r[3], r[4]))
        for g in gastos:
            detalhes = f"{g[5]}/{g[6]}" if g[3] == "Parcelado" else "-"
            self.tree_gastos.insert("", "end", values=(g[0], g[10], g[1], f"R$ {g[2]:.2f}", g[3], g[7], g[9], detalhes))

        self.calcular_previsao() 

    def calcular_previsao(self):
        """
        Calcula o fluxo de caixa projetado até uma data específica no mês corrente,
        considerando parâmetros customizáveis (ex: ignorar fixos, assinaturas, etc).
        """
        try:
            dia_alvo = int(self.entry_dia_prev.get())
        except ValueError:
            self.lbl_valor_prev.configure(text="Dia Inválido", text_color=DANGER_COLOR)
            return

        mes_alvo = self.app.data_visualizacao.strftime("%Y-%m")
        receitas, _ = self.app.db.obter_receitas_do_mes(mes_alvo)
        gastos = self.app.db.obter_gastos_do_mes(mes_alvo)

        hp_ate_dia = 0.0
        dano_ate_dia = 0.0

        # Filtro temporal para receitas
        for r in receitas:
            if r[3] == "Fixo":
                if r[4] <= dia_alvo: 
                    hp_ate_dia += r[2]
            else:
                try:
                    dia_rec = int(r[6].split('/')[0])
                    if dia_rec <= dia_alvo:
                        hp_ate_dia += r[2]
                except:
                    pass

        # Captura do estado de configurações temporais
        abater_fixos = self.prev_var_fixos.get()
        abater_assinaturas = self.prev_var_assinaturas.get()
        abater_parcelas = self.prev_var_parcelas.get()

        # Filtro misto (temporal e lógico) para despesas
        for g in gastos:
            tipo = g[3]
            valor = g[2]
            
            if tipo == "Fixo":
                if abater_fixos: dano_ate_dia += valor
            elif tipo == "Assinatura":
                if abater_assinaturas: dano_ate_dia += valor
            elif tipo == "Parcelado":
                if abater_parcelas: dano_ate_dia += valor
            else:
                try:
                    dia_gasto = int(g[10].split('/')[0])
                    if dia_gasto <= dia_alvo:
                        dano_ate_dia += valor
                except:
                    pass

        saldo_prev = hp_ate_dia - dano_ate_dia
        cor = INFO_COLOR if saldo_prev >= 0 else DANGER_COLOR
        prefixo = "" if saldo_prev >= 0 else "- "
        self.lbl_valor_prev.configure(text=f"{prefixo}R$ {abs(saldo_prev):.2f}", text_color=cor)

    def excluir_receita(self):
        """Remove o registro de receita selecionado na Treeview correspondente."""
        selecionado = self.tree_receitas.selection()
        if selecionado:
            item_id = self.tree_receitas.item(selecionado[0], "values")[0]
            conn = self.app.db.conectar()
            conn.execute("DELETE FROM receitas WHERE id = ?", (item_id,))
            conn.commit()
            conn.close()
            self.atualizar_dados()

    def excluir_gasto(self):
        """Remove o registro de gasto selecionado na Treeview correspondente."""
        selecionado = self.tree_gastos.selection()
        if selecionado:
            item_id = self.tree_gastos.item(selecionado[0], "values")[0]
            conn = self.app.db.conectar()
            conn.execute("DELETE FROM gastos WHERE id = ?", (item_id,))
            conn.commit()
            conn.close()
            self.atualizar_dados()

    # Handlers para invocação de modais
    def abrir_modal_gasto(self):
        ModalGasto(self.app)
        
    def abrir_modal_receita(self):
        ModalReceita(self.app)
        
    def abrir_modal_cofres(self):
        ModalCofres(self.app)
        
    def abrir_modal_escudo(self):
        ModalEscudo(self.app)