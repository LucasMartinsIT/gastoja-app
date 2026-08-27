"""
Módulo de persistência de dados e regras de negócio da aplicação GastoJa.
Gerencia a conexão SQLite, inicialização de schemas, migrações estruturais nativas
e o motor lógico de consultas financeiras temporais (viagem no tempo e fluxo de caixa).
"""

import sqlite3
from datetime import datetime

class DatabaseManager:
    """
    Camada de acesso a dados (DAO) e orquestração de regras financeiras.
    """

    def __init__(self, db_name="gastos.db"):
        self.db_name = db_name
        self.iniciar_banco()

    def conectar(self):
        """Estabelece e retorna uma nova conexão com o banco de dados SQLite."""
        return sqlite3.connect(self.db_name)

    def iniciar_banco(self):
        """
        Garante a integridade do schema do banco de dados na inicialização.
        Cria as tabelas caso não existam e aplica migrações estruturais dinâmicas
        para manter a compatibilidade com versões anteriores da base local.
        """
        conn = self.conectar()
        cursor = conn.cursor()
        
        # Criação de entidades estruturais
        cursor.execute('''CREATE TABLE IF NOT EXISTS config (chave TEXT PRIMARY KEY, valor REAL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT UNIQUE)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS bancos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE,
            dia_fechamento INTEGER,
            dia_vencimento INTEGER,
            cheque_especial REAL DEFAULT 0.0
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor REAL,
            tipo TEXT,
            mes_ano_registro TEXT,
            parcela_inicial INTEGER,
            total_parcelas INTEGER,
            tag TEXT DEFAULT '',
            dia_vencimento INTEGER DEFAULT 1,
            banco TEXT DEFAULT 'Carteira/Dinheiro',
            data_exata TEXT DEFAULT ''
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor REAL,
            tipo TEXT,
            dia_recebimento INTEGER,
            mes_ano_registro TEXT,
            data_exata TEXT DEFAULT ''
        )''')

        # Migrações dinâmicas (Backward Compatibility)
        colunas_gastos = [col[1] for col in cursor.execute("PRAGMA table_info(gastos)").fetchall()]
        if 'tag' not in colunas_gastos: 
            cursor.execute("ALTER TABLE gastos ADD COLUMN tag TEXT DEFAULT ''")
        if 'dia_vencimento' not in colunas_gastos: 
            cursor.execute("ALTER TABLE gastos ADD COLUMN dia_vencimento INTEGER DEFAULT 1")
        if 'banco' not in colunas_gastos: 
            cursor.execute("ALTER TABLE gastos ADD COLUMN banco TEXT DEFAULT 'Carteira/Dinheiro'")
        if 'data_exata' not in colunas_gastos: 
            cursor.execute("ALTER TABLE gastos ADD COLUMN data_exata TEXT DEFAULT ''")

        colunas_bancos = [col[1] for col in cursor.execute("PRAGMA table_info(bancos)").fetchall()]
        if 'cheque_especial' not in colunas_bancos: 
            cursor.execute("ALTER TABLE bancos ADD COLUMN cheque_especial REAL DEFAULT 0.0")

        colunas_receitas = [col[1] for col in cursor.execute("PRAGMA table_info(receitas)").fetchall()]
        if 'data_exata' not in colunas_receitas: 
            cursor.execute("ALTER TABLE receitas ADD COLUMN data_exata TEXT DEFAULT ''")

        cursor.execute(
            "INSERT OR IGNORE INTO bancos (nome, dia_fechamento, dia_vencimento, cheque_especial) "
            "VALUES ('Carteira/Dinheiro', 31, 1, 0.0)"
        )
        
        conn.commit()
        conn.close()

    def adicionar_receita(self, descricao, valor, tipo, dia, mes_ano, data_exata):
        """Persiste um novo registro de entrada financeira (Receita)."""
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO receitas (descricao, valor, tipo, dia_recebimento, mes_ano_registro, data_exata) VALUES (?, ?, ?, ?, ?, ?)",
            (descricao, valor, tipo, dia, mes_ano, data_exata)
        )
        conn.commit()
        conn.close()

    def obter_receitas_do_mes(self, mes_ano_alvo):
        """
        Recupera as receitas aplicáveis a um determinado mês.
        Aplica a lógica de recorrência para receitas do tipo 'Fixo' e 
        filtragem exata para receitas do tipo 'Avulso'.
        """
        conn = self.conectar()
        cursor = conn.cursor()
        data_alvo = datetime.strptime(mes_ano_alvo, "%Y-%m")
        cursor.execute("SELECT id, descricao, valor, tipo, dia_recebimento, mes_ano_registro, data_exata FROM receitas")
        todas_receitas = cursor.fetchall()
        conn.close()

        receitas_validas = []
        total_hp = 0.0

        for rec in todas_receitas:
            data_reg = datetime.strptime(rec[5], "%Y-%m")
            tipo = rec[3]

            if tipo == 'Fixo' and data_reg <= data_alvo:
                receitas_validas.append(rec)
                total_hp += rec[2]
            elif tipo == 'Avulso' and rec[5] == mes_ano_alvo:
                receitas_validas.append(rec)
                total_hp += rec[2]

        return receitas_validas, total_hp

    def atualizar_cheque_especial(self, banco_nome, valor_limite):
        """Atualiza a margem de segurança (limite) atrelada a uma instituição."""
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE bancos SET cheque_especial = ? WHERE nome = ?", (valor_limite, banco_nome))
        conn.commit()
        conn.close()

    def obter_total_cheque_especial(self):
        """Consolida o valor total de margem de crédito disponível entre todos os bancos."""
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(cheque_especial) FROM bancos")
        total = cursor.fetchone()[0]
        conn.close()
        return total if total else 0.0

    def adicionar_gasto(self, desc, valor, tipo, mes_ano_registro, parc_atual, parc_total, tag, dia_venc, banco, data_exata):
        """Persiste um novo registro de saída financeira estruturada (Gasto)."""
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO gastos (descricao, valor, tipo, mes_ano_registro, parcela_inicial, total_parcelas, tag, dia_vencimento, banco, data_exata)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            (desc, valor, tipo, mes_ano_registro, parc_atual, parc_total, tag, dia_venc, banco, data_exata)
        )
        conn.commit()
        conn.close()

    def obter_gastos_do_mes(self, mes_ano_alvo):
        """
        Motor de extração e projeção de despesas do mês.
        Processa faturas, projeta parcelamentos futuros baseados no delta de tempo
        e realiza a reconciliação automática de faturas declaradas versus gastos individuais vinculados.
        """
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, descricao, valor, tipo, mes_ano_registro, parcela_inicial, total_parcelas, tag, dia_vencimento, banco, data_exata FROM gastos")
        todos_gastos = cursor.fetchall()
        conn.close()

        gastos_normais = []
        faturas_declaradas = []
        data_alvo = datetime.strptime(mes_ano_alvo, "%Y-%m")

        # Triagem e projeção temporal das despesas
        for gasto in todos_gastos:
            tipo = gasto[3]
            data_registro = datetime.strptime(gasto[4], "%Y-%m")

            if tipo == "Fatura":
                if gasto[4] == mes_ano_alvo:
                    faturas_declaradas.append(gasto)
            
            elif tipo == "Fixo" or tipo == "Assinatura":
                if data_registro <= data_alvo:
                    gastos_normais.append(list(gasto))
            
            elif tipo == "Variável":
                if gasto[4] == mes_ano_alvo:
                    gastos_normais.append(list(gasto))
            
            elif tipo == "Parcelado":
                meses_diferenca = (data_alvo.year - data_registro.year) * 12 + (data_alvo.month - data_registro.month)
                if meses_diferenca >= 0:
                    parcela_no_mes_alvo = gasto[5] + meses_diferenca
                    if parcela_no_mes_alvo <= gasto[6]:
                        gasto_ajustado = list(gasto)
                        gasto_ajustado[5] = parcela_no_mes_alvo
                        gastos_normais.append(gasto_ajustado)

        # Reconciliação (Motor de Abatimento)
        # Isola os valores de faturas manuais deduzindo gastos explícitos do cartão.
        for fatura in faturas_declaradas:
            banco_fatura = fatura[9]
            valor_fatura = fatura[2]
            
            # Subtrai despesas atreladas ao cartão (ignorando 'Fixos' que são débitos em conta)
            total_explicado = sum(
                g[2] for g in gastos_normais 
                if g[9] == banco_fatura and g[3] in ["Assinatura", "Parcelado", "Variável"]
            )
            
            valor_restante = valor_fatura - total_explicado
            fatura_ajustada = list(fatura)
            
            if valor_restante > 0:
                fatura_ajustada[2] = valor_restante
                fatura_ajustada[1] = f"{fatura[1]} (Complemento)" 
            else:
                fatura_ajustada[2] = 0.0 
                fatura_ajustada[1] = f"{fatura[1]} (Totalmente Abatida)"
                
            gastos_normais.append(fatura_ajustada)

        return [tuple(g) for g in gastos_normais]