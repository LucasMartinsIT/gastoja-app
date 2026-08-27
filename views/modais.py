"""
Módulo de janelas modais da aplicação GastoJa.
Contém as interfaces de sobreposição (Toplevel) para inserção e 
gerenciamento de dados como Receitas, Gastos, Bancos, Tags e Limites.
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

# Constantes de paleta de cores e tipografia
BG_COLOR = "#120d0a"        
FRAME_COLOR = "#211712"     
TEXT_COLOR = "#e6d5c3"      
ACCENT_COLOR = "#c2753e"    
DANGER_COLOR = "#8f3333"    
SUCCESS_COLOR = "#4d734d"

FONT_MAIN = ("Consolas", 13)
FONT_BOLD = ("Consolas", 13, "bold")
FONT_TITLE = ("Consolas", 16, "bold")


class ModalGasto(ctk.CTkToplevel):
    """
    Interface para registro de novas despesas.
    Suporta lançamentos fixos, avulsos, parcelados e faturas.
    """

    def __init__(self, app_core):
        super().__init__()
        self.app = app_core
        self.title("Registrar Dano (Gasto)")
        self.geometry("600x450")
        self.configure(fg_color=BG_COLOR)
        self.attributes("-topmost", True) 

        ctk.CTkLabel(self, text="Registrar Novo Gasto", font=FONT_TITLE, text_color=DANGER_COLOR).pack(pady=15)

        frame = ctk.CTkFrame(self, fg_color=FRAME_COLOR)
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Campos base: Data, Descrição e Valor
        row1 = ctk.CTkFrame(frame, fg_color="transparent")
        row1.pack(fill="x", pady=10)
        
        ctk.CTkLabel(row1, text="Data:", font=FONT_MAIN).pack(side="left", padx=5)
        self.entry_data = ctk.CTkEntry(row1, width=100)
        self.entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_data.pack(side="left", padx=5)

        ctk.CTkLabel(row1, text="Desc:", font=FONT_MAIN).pack(side="left", padx=5)
        self.entry_desc = ctk.CTkEntry(row1, width=150)
        self.entry_desc.pack(side="left", padx=5)

        ctk.CTkLabel(row1, text="Valor:", font=FONT_MAIN).pack(side="left", padx=5)
        self.entry_valor = ctk.CTkEntry(row1, width=100)
        self.entry_valor.pack(side="left", padx=5)

        # Classificação: Tipo, Tag e Banco
        row2 = ctk.CTkFrame(frame, fg_color="transparent")
        row2.pack(fill="x", pady=10)
        
        self.combo_tipo = ctk.CTkOptionMenu(
            row2, 
            values=["Fixo", "Assinatura", "Variável", "Parcelado", "Fatura"], 
            fg_color=BG_COLOR, 
            button_color=ACCENT_COLOR, 
            command=self.toggle_parcelas
        )
        self.combo_tipo.pack(side="left", padx=5)

        # Carregamento de dependências do banco
        conn = self.app.db.conectar()
        tags = [row[0] for row in conn.execute("SELECT nome FROM tags ORDER BY nome").fetchall()]
        bancos = [row[0] for row in conn.execute("SELECT nome FROM bancos ORDER BY id").fetchall()]
        conn.close()

        self.combo_tag = ctk.CTkOptionMenu(row2, values=tags if tags else ["Sem Tag"], fg_color=BG_COLOR, button_color=ACCENT_COLOR)
        self.combo_tag.pack(side="left", padx=5)

        self.combo_banco = ctk.CTkOptionMenu(row2, values=bancos if bancos else ["Nenhum"], fg_color=BG_COLOR, button_color=ACCENT_COLOR)
        self.combo_banco.pack(side="left", padx=5)

        # Container dinâmico para controle de parcelas
        self.frame_parcelas = ctk.CTkFrame(frame, fg_color="transparent")
        
        ctk.CTkLabel(self.frame_parcelas, text="Parcela Atual:", font=FONT_MAIN).pack(side="left", padx=5)
        self.entry_parc_atual = ctk.CTkEntry(self.frame_parcelas, width=50)
        self.entry_parc_atual.insert(0, "1")
        self.entry_parc_atual.pack(side="left", padx=5)

        ctk.CTkLabel(self.frame_parcelas, text="de Total de:", font=FONT_MAIN).pack(side="left", padx=5)
        self.entry_parc_total = ctk.CTkEntry(self.frame_parcelas, width=50)
        self.entry_parc_total.pack(side="left", padx=5)

        self.btn_salvar = ctk.CTkButton(self, text="Adicionar Dano", fg_color=DANGER_COLOR, hover_color="#6b2626", font=FONT_BOLD, command=self.salvar)
        self.btn_salvar.pack(pady=15)

    def toggle_parcelas(self, escolha):
        """Controla a visibilidade dos campos de parcela baseado no tipo de gasto."""
        if escolha == "Parcelado":
            self.frame_parcelas.pack(fill="x", pady=5)
        else:
            self.frame_parcelas.pack_forget()

    def salvar(self):
        """Valida e persiste os dados do lançamento no banco de dados."""
        desc = self.entry_desc.get().strip()
        try:
            valor = float(self.entry_valor.get().replace(',', '.'))
        except ValueError:
            messagebox.showerror("Erro", "Valor numérico inválido.", parent=self)
            return

        tipo = self.combo_tipo.get()
        parc_atual = 0
        parc_total = 0

        if tipo == "Parcelado":
            try:
                parc_atual = int(self.entry_parc_atual.get())
                parc_total = int(self.entry_parc_total.get())
            except ValueError:
                messagebox.showerror("Erro", "Valores das parcelas devem ser números inteiros.", parent=self)
                return

        mes_ano_registro = self.app.data_visualizacao.strftime("%Y-%m")
        self.app.db.adicionar_gasto(
            desc, valor, tipo, mes_ano_registro, 
            parc_atual, parc_total, self.combo_tag.get(), 
            1, self.combo_banco.get(), self.entry_data.get()
        )
        
        self.app.atualizar_hub()
        self.destroy()


class ModalReceita(ctk.CTkToplevel):
    """
    Interface para registro de entradas financeiras.
    """

    def __init__(self, app_core):
        super().__init__()
        self.app = app_core
        self.title("Adicionar HP (Receita)")
        self.geometry("450x350")
        self.configure(fg_color=BG_COLOR)
        self.attributes("-topmost", True)

        ctk.CTkLabel(self, text="Registrar Novo Ganho", font=FONT_TITLE, text_color=SUCCESS_COLOR).pack(pady=15)

        frame = ctk.CTkFrame(self, fg_color=FRAME_COLOR)
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.entry_desc = ctk.CTkEntry(frame, placeholder_text="Descrição (Ex: Salário)")
        self.entry_desc.pack(fill="x", padx=10, pady=10)
        
        self.entry_valor = ctk.CTkEntry(frame, placeholder_text="Valor (R$)")
        self.entry_valor.pack(fill="x", padx=10, pady=5)

        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x", pady=10)
        
        self.combo_tipo = ctk.CTkOptionMenu(row, values=["Fixo", "Avulso"], fg_color=BG_COLOR, button_color=ACCENT_COLOR, width=120)
        self.combo_tipo.pack(side="left", padx=10)

        ctk.CTkLabel(row, text="Dia Fixo:", font=FONT_MAIN).pack(side="left", padx=5)
        self.entry_dia = ctk.CTkEntry(row, width=60)
        self.entry_dia.insert(0, "5")
        self.entry_dia.pack(side="left", padx=5)

        ctk.CTkButton(self, text="Adicionar HP", fg_color=SUCCESS_COLOR, hover_color="#3a593a", font=FONT_BOLD, command=self.salvar).pack(pady=15)

    def salvar(self):
        """Valida e persiste a nova receita."""
        desc = self.entry_desc.get().strip()
        try:
            valor = float(self.entry_valor.get().replace(',', '.'))
            dia_fixo = int(self.entry_dia.get())
        except ValueError:
            return

        mes_ano = self.app.data_visualizacao.strftime("%Y-%m")
        data_exata = datetime.now().strftime("%d/%m/%Y")
        
        self.app.db.adicionar_receita(desc, valor, self.combo_tipo.get(), dia_fixo, mes_ano, data_exata)
        self.app.atualizar_hub()
        self.destroy()


class ModalCofres(ctk.CTkToplevel):
    """
    Interface para configuração de entidades estruturais: Bancos (Cofres) e Categorias (Tags).
    """

    def __init__(self, app_core):
        super().__init__()
        self.app = app_core
        self.title("Gerenciar Cofres e Tags")
        self.geometry("450x450")
        self.configure(fg_color=BG_COLOR)
        self.attributes("-topmost", True)

        # Seção 1: Configuração de Instituições Financeiras
        frame_banco = ctk.CTkFrame(self, fg_color=FRAME_COLOR)
        frame_banco.pack(fill="x", padx=20, pady=(15, 10))

        ctk.CTkLabel(frame_banco, text="Novo Banco/Cartão", font=FONT_TITLE, text_color=ACCENT_COLOR).pack(pady=10)
        
        self.entry_nome = ctk.CTkEntry(frame_banco, placeholder_text="Nome (Ex: Nubank)")
        self.entry_nome.pack(pady=5, fill="x", padx=40)
        
        frame_dias = ctk.CTkFrame(frame_banco, fg_color="transparent")
        frame_dias.pack(pady=5)
        
        ctk.CTkLabel(frame_dias, text="Fechamento:", font=FONT_MAIN).grid(row=0, column=0, padx=5, pady=5)
        self.entry_fechamento = ctk.CTkEntry(frame_dias, width=60)
        self.entry_fechamento.insert(0, "1")
        self.entry_fechamento.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(frame_dias, text="Vencimento:", font=FONT_MAIN).grid(row=1, column=0, padx=5, pady=5)
        self.entry_vencimento = ctk.CTkEntry(frame_dias, width=60)
        self.entry_vencimento.insert(0, "10")
        self.entry_vencimento.grid(row=1, column=1, padx=5, pady=5)
        
        ctk.CTkButton(frame_banco, text="Salvar Cofre", fg_color=ACCENT_COLOR, command=self.salvar_cofre).pack(pady=15)

        # Seção 2: Configuração de Categorias
        frame_tag = ctk.CTkFrame(self, fg_color=FRAME_COLOR)
        frame_tag.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(frame_tag, text="Nova Tag (Categoria)", font=FONT_TITLE, text_color=SUCCESS_COLOR).pack(pady=10)
        
        self.entry_tag = ctk.CTkEntry(frame_tag, placeholder_text="Nome (Ex: Alimentação)")
        self.entry_tag.pack(pady=5, fill="x", padx=40)

        ctk.CTkButton(frame_tag, text="Salvar Tag", fg_color=SUCCESS_COLOR, hover_color="#3a593a", command=self.salvar_tag).pack(pady=15)

    def salvar_cofre(self):
        """Insere um novo banco/cartão com regras de fechamento/vencimento."""
        nome = self.entry_nome.get().strip()
        if not nome:
            return
            
        try:
            fechamento = int(self.entry_fechamento.get())
            vencimento = int(self.entry_vencimento.get())
        except ValueError:
            messagebox.showerror("Erro", "Os dias devem ser representados por números inteiros.", parent=self)
            return
            
        conn = self.app.db.conectar()
        try:
            conn.execute(
                "INSERT INTO bancos (nome, dia_fechamento, dia_vencimento) VALUES (?, ?, ?)", 
                (nome, fechamento, vencimento)
            )
            conn.commit()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na persistência do cofre: {e}", parent=self)
        finally:
            conn.close()
            
        self.app.atualizar_hub()
        self.destroy()

    def salvar_tag(self):
        """Insere uma nova categoria (tag) no sistema."""
        nome_tag = self.entry_tag.get().strip()
        if not nome_tag:
            return

        conn = self.app.db.conectar()
        try:
            conn.execute("INSERT INTO tags (nome) VALUES (?)", (nome_tag,))
            conn.commit()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na persistência da tag: {e}", parent=self)
        finally:
            conn.close()
            
        self.app.atualizar_hub()
        self.destroy()


class ModalEscudo(ctk.CTkToplevel):
    """
    Interface para alocação de limite emergencial (Cheque Especial).
    Permite vincular uma margem de segurança a uma instituição financeira específica.
    """

    def __init__(self, app_core):
        super().__init__()
        self.app = app_core
        self.title("Configurar Escudo")
        self.geometry("400x250")
        self.configure(fg_color=BG_COLOR)
        self.attributes("-topmost", True)

        ctk.CTkLabel(self, text="Escudo (Cheque Especial)", font=FONT_TITLE, text_color="#d6a848").pack(pady=15)

        # Assegura a integridade do schema (backward compatibility para base legada)
        conn = self.app.db.conectar()
        try:
            conn.execute("ALTER TABLE bancos ADD COLUMN limite REAL DEFAULT 0")
            conn.commit()
        except:
            pass 
            
        bancos = [row[0] for row in conn.execute("SELECT nome FROM bancos ORDER BY id").fetchall()]
        conn.close()

        frame = ctk.CTkFrame(self, fg_color=FRAME_COLOR)
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.combo_banco = ctk.CTkOptionMenu(frame, values=bancos if bancos else ["Nenhum"], fg_color=BG_COLOR, button_color=ACCENT_COLOR)
        self.combo_banco.pack(pady=10, fill="x", padx=40)

        self.entry_limite = ctk.CTkEntry(frame, placeholder_text="Limite (R$)")
        self.entry_limite.pack(pady=5, fill="x", padx=40)

        ctk.CTkButton(frame, text="Atualizar Escudo", fg_color="#d6a848", hover_color="#b58a33", text_color=BG_COLOR, font=FONT_BOLD, command=self.salvar).pack(pady=15)

    def salvar(self):
        """Atualiza a propriedade de limite (escudo) da instituição selecionada."""
        banco = self.combo_banco.get()
        try:
            limite = float(self.entry_limite.get().replace(',', '.'))
        except ValueError:
            messagebox.showerror("Erro", "Formato de valor inválido.", parent=self)
            return

        conn = self.app.db.conectar()
        conn.execute("UPDATE bancos SET limite = ? WHERE nome = ?", (limite, banco))
        conn.commit()
        conn.close()
        
        self.app.atualizar_hub()
        self.destroy()