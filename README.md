# 📊 GastoJa Desktop  - Controle Financeiro Simplificado

![Badge Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Badge Status](https://img.shields.io/badge/Status-Conclu%C3%ADdo-success?style=for-the-badge)

O **GastoJa** é uma aplicação desktop desenvolvida para facilitar o controle financeiro pessoal, oferecendo uma interface intuitiva para o registro e acompanhamento de receitas e despesas.

https://github.com/user-attachments/assets/b77f2a53-d2a7-40ac-be7d-f5512dead237

## 🚀 Funcionalidades

* **Interface Amigável:** Design limpo focado na experiência do usuário.
* **Gestão de Finanças:** Cadastro rápido de entradas e saídas.
* **Armazenamento Local:** Seus dados financeiros ficam salvos de forma segura na sua própria máquina, sem dependência de nuvem.
* **Execução Direta:** Não requer instalação de dependências complexas (Standalone).

## 🛠️ Tecnologias e Arquitetura

O ecossistema foi construído utilizando escolhas intencionais de arquitetura:

* **Python:** Linguagem principal pela versatilidade, facilidade de manipulação de dados e ecossistema robusto para scripts utilitários.
* **CustomTkinter:** Framework de interface gráfica moderno para Python. Foi escolhido por permitir a criação de componentes nativos estilizados com alta performance e suporte a temas customizados, dando vida ao visual _Dark Mocha_.
* **SQLite (`gastos.db`):** Banco de dados relacional embarcado de zero configuração. Garante persistência local segura, substituindo arquivos JSON estáticos e permitindo o uso de tabelas estruturadas (como o gerenciamento dinâmico de tags e regras de 
parcelas).
* **Matplotlib:** Biblioteca de visualização de dados integrada para renderizar o gráfico analítico de distribuição de recursos diretamente na interface gráfica.
* **PyInstaller:** Ferramenta de empacotamento utilizada para compilar todo o interpretador, dependências e código em um executável (`.exe`) nativo e autossuficiente para desktop.

## 📦 Como baixar e testar

Você pode testar a aplicação diretamente no seu computador sem precisar instalar o Python ou mexer com código.

1. Navegue até a aba **[Releases](../../releases)** aqui mesmo neste repositório (no canto direito da tela).
2. Baixe o arquivo executável (`.exe` ou `.zip`) da versão mais recente.
3. Extraia (se necessário) e dê um duplo clique no programa para começar a usar!

## 🔒 Sobre o Código Fonte

O código fonte do **GastoJá** é mantido em um repositório **privado**, pois trata-se de um projeto de autoria própria. 

> 💡 **Para Recrutadores:** Caso você tenha interesse em avaliar a arquitetura do projeto, a estruturação em Python, manipulação de dados ou meus padrões de código, estou à total disposição para demonstrar a base de código durante uma entrevista técnica.

## 👨‍💻 Autor

**Lucas Martins**
Desenvolvedor Backend

- [LinkedIn](https://www.linkedin.com/in/lucas-martins0)
