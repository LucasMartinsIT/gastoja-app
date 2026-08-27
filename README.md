# 📊 GastoJá Desktop - v2.0 (Hub Edition)

![Badge Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Badge SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Badge Status](https://img.shields.io/badge/Status-Conclu%C3%ADdo-success?style=for-the-badge)

O **GastoJá** é uma aplicação desktop desenvolvida para facilitar o controle financeiro pessoal, oferecendo uma interface intuitiva para o registro e acompanhamento de receitas e despesas[cite: 1]. A versão 2.0 foi totalmente reescrita com foco em arquitetura modular (MVC) e inteligência de dados.

## 🚀 Funcionalidades

- **Dashboard Analítico (Hub):** Visão centralizada de saúde financeira com indicadores de progresso (HP e Escudo).
- **Motor de Previsão de Caixa:** Algoritmo de "viagem no tempo" que calcula o saldo exato em dias específicos do mês, permitindo ligar/desligar o peso de faturas, assinaturas e gastos fixos na projeção.
- **Sistema de Escudo (Cheque Especial):** Mecânica visual que protege o saldo principal e sinaliza danos críticos quando o limite bancário é atingido.
- **Abatimento Inteligente de Faturas:** O sistema reconcilia automaticamente compras parceladas e assinaturas com a fatura principal do cartão, evitando duplicação de despesas.
- **Armazenamento Local Segregado:** Seus dados financeiros ficam salvos de forma segura na sua própria máquina, sem dependência de nuvem[cite: 1].

## 🛠️ Tecnologias e Arquitetura

O ecossistema foi construído utilizando escolhas intencionais de arquitetura e separação de responsabilidades (MVC):

- **Python:** Linguagem principal pela versatilidade, facilidade de manipulação de dados e ecossistema robusto para scripts utilitários[cite: 1].
- **CustomTkinter & Tkinter (Treeview):** Framework de interface gráfica moderno para Python. Foi escolhido por permitir a criação de componentes nativos estilizados com alta performance e suporte a temas customizados, dando vida ao visual _Dark Mocha_[cite: 1].
- **SQLite (`gastos.db`):** Banco de dados relacional embarcado de zero configuração. Garante persistência local segura e permite o uso de tabelas estruturadas (como o gerenciamento dinâmico de tags e regras de parcelas)[cite: 1]. Conta com sistema de _migrations_ automáticas para manter a retrocompatibilidade.
- **PyInstaller:** Ferramenta de empacotamento utilizada para compilar todo o interpretador, dependências e código em um executável (`.exe`) nativo e autossuficiente para desktop[cite: 1].

## 📦 Como baixar e testar

Você pode testar a aplicação diretamente no seu computador sem precisar instalar o Python ou mexer com código[cite: 1].

1. Navegue até a aba **[Releases](../../releases)** aqui mesmo neste repositório (no canto direito da tela)[cite: 1].
2. Baixe o arquivo executável (`GastoJa.exe`) da versão v2.0.0.
3. Dê um duplo clique no programa para começar a usar![cite: 1] O banco de dados será gerado automaticamente na mesma pasta.

## 🔒 Sobre o Código Fonte

O código fonte do **GastoJá** agora é **público** para fins de portfólio. A arquitetura foi refatorada para demonstrar boas práticas de engenharia de software, incluindo:

- Padronização PEP 8 e uso extensivo de _Docstrings_.
- Separação estrita entre Regras de Negócio (`DatabaseManager`) e Renderização (`ViewDashboard` / Modais).
- Tratamento de exceções e prevenção contra falhas de injeção de dados.

> 💡 **Para Recrutadores e Desenvolvedores:** Fiquem à vontade para explorar a estrutura de diretórios (`core/` e `views/`). Estou à total disposição para discutir as decisões de arquitetura e manipulação de dados durante entrevistas técnicas.

## 👨‍💻 Autor

**Lucas Martins**
Desenvolvedor Backend[cite: 1]

- [LinkedIn](https://www.linkedin.com/in/lucas-martins0)[cite: 1]
