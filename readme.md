# Tabela FIPE - Consulta de Preços de Veículos

## Descrição

Este é um projeto de portfólio que consiste em uma aplicação de desktop desenvolvida em Python com a biblioteca `tkinter`. A aplicação permite ao usuário consultar o preço de mercado de veículos (carros, motos e caminhões) de acordo com a tabela FIPE, utilizando a API pública do [Parallelum](https://deividfortuna.github.io/fipe/).

O sistema guia o usuário através de um assistente passo a passo para selecionar o tipo de veículo, a marca, o modelo e o ano, exibindo ao final o valor atualizado do veículo.

## Funcionalidades

-   Consulta de preços para Carros, Motos e Caminhões.
-   Interface gráfica intuitiva e fácil de usar.
-   Busca dinâmica de marcas, modelos e anos através da API FIPE.
-   Exibição detalhada das informações do veículo ao final da consulta.
-   Opção de iniciar uma nova consulta ou sair da aplicação através do menu.

## Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    ```
2.  **Navegue até o diretório do projeto:**
    ```bash
    cd tabela_fipe_python
    ```
3.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Execute a aplicação:**
    ```bash
    python main.py
    ```

## Tecnologias Utilizadas

-   **Python**: Linguagem principal do projeto.
-   **Tkinter**: Biblioteca padrão do Python para a criação de interfaces gráficas.
-   **Requests**: Biblioteca para realizar as requisições HTTP à API da Tabela FIPE.
