import tkinter as tk
from tkinter import ttk, messagebox
import requests

class FrameSelecao(tk.Frame):
    """
    Um frame genérico para exibir uma lista de opções selecionáveis (Radiobuttons)
    com funcionalidade de busca e carregamento de dados via API ou lista estática.
    """
    def __init__(self, parent, command=None, url=None, dados_estaticos=None, 
                label_busca="Buscar:", chave_json=None):
        """
        Construtor do Frame de Seleção.

        :param parent: O widget pai.
        :param command: (function) Callback a ser chamado quando uma opção é 
        selecionada.
                        Recebe o 'código' da opção como argumento.
        :param url: (str, opcional) URL da API para buscar os dados.
        :param dados_estaticos: (list, opcional) Uma lista de strings para 
        opções fixas.
        :param label_busca: (str) O texto a ser exibido no label do campo 
        de busca.
        :param chave_json: (str, opcional) A chave a ser acessada no JSON 
        de resposta da API se a lista de itens estiver aninhada (ex: 'modelos').
        """
        super().__init__(parent)
        self.grid(row=0, column=0, sticky='nsew')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.command_callback = command
        self.url = url
        self.chave_json = chave_json
        self.all_items = []

        # `var_selecao` é a variável de controle do Tkinter para os Radiobuttons.
        self.var_selecao = tk.StringVar()
        self.var_selecao.set("")

        self._criar_widgets(label_busca)

        # Decide a fonte dos dados: API ou uma lista estática.
        if self.url:
            self._carregar_dados_api()
        elif dados_estaticos:
            # Converte a lista estática para o formato esperado 
            # {'nome': ..., 'codigo': ...}
            self.all_items = [{'nome': item.capitalize(), 'codigo': item} 
                            for item in dados_estaticos]
            self.atualizar_lista_radio(self.all_items)

    def _criar_widgets(self, label_busca):
        """Cria os widgets base do frame (busca, canvas, scrollbar)."""
        self.var_entry_busca = tk.StringVar()
        tk.Label(self, text=label_busca).grid(row=0, column=0, sticky='w', padx=5)
        entry = tk.Entry(self, textvariable=self.var_entry_busca)
        entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        # O evento <KeyRelease> chama o filtro toda vez que uma tecla é solta.
        entry.bind('<KeyRelease>', self.filtrar_lista)

        # --- Canvas e Scrollbar ---
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', 
                                    command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas)
        # Adiciona o frame rolável dentro do canvas.
        self.canvas.create_window((0, 0), window=self.scrollable_frame,
                                anchor='nw')
        # Configura o canvas para atualizar a região de rolagem quando o 
        # tamanho do frame interno mudar.
        self.scrollable_frame.bind('<Configure>', lambda e: 
            self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.canvas.grid(row=1, column=0, columnspan=2, sticky='nsew')
        self.scrollbar.grid(row=1, column=2, sticky='ns')

    def _carregar_dados_api(self):
        """Busca os dados da API e popula a lista de itens."""
        try:
            response = requests.get(self.url) #type:ignore
            response.raise_for_status()
            dados = response.json()

            # Se `chave_json` for fornecida (ex: 'modelos'), busca a lista
            # dentro do JSON.
            if self.chave_json:
                self.all_items = dados.get(self.chave_json, [])
            # Caso contrário, a resposta da API já é a lista.
            else:
                self.all_items = dados
            
            self.atualizar_lista_radio(self.all_items)
        except requests.exceptions.RequestException as e:
            messagebox.showerror(
                "Erro de Rede", f"Não foi possível buscar os dados: {e}")

    def filtrar_lista(self, event=None):
        """Filtra a lista de itens com base no texto da busca."""
        texto_busca = self.var_entry_busca.get().lower()
        # Se a busca estiver vazia, mostra todos os itens.
        if not texto_busca:
            items_filtrados = self.all_items
        else:
            # Filtra a lista `all_items` mantendo apenas os que contêm o texto 
            # da busca.
            items_filtrados = [item for item in self.all_items if 
                            texto_busca in item['nome'].lower()]
        
        self.atualizar_lista_radio(items_filtrados)

    def atualizar_lista_radio(self, lista_items):
        """Limpa e recria os Radiobuttons na tela."""
        # Destrói todos os widgets antigos para evitar sobreposição.
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        for item in lista_items:
            # Cria um Radiobutton para cada item na lista fornecida.
            tk.Radiobutton(
                self.scrollable_frame, 
                text=item['nome'], 
                value=item['codigo'],
                variable=self.var_selecao,
                command=self.ao_clicar
            ).pack(anchor='w', padx=10, pady=2)

    def ao_clicar(self):
        """Callback executado ao clicar em um Radiobutton."""
        if self.command_callback:
            valor_selecionado = self.var_selecao.get()
            self.command_callback(valor_selecionado)

if __name__ == '__main__':
    # Bloco para teste visual do componente
    def on_selection_test(value):
        print(f"Opção selecionada: {value}")

    root = tk.Tk()
    root.title("Teste do Frame de Seleção Genérico")
    root.geometry("400x500")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # --- Exemplo 1: Dados Estáticos (como o frame_um) ---
    # frame_estatico = FrameSelecao(
    #     root, 
    #     command=on_selection_test,
    #     dados_estaticos=['carros', 'motos', 'caminhoes'],
    #     label_busca="Selecione o tipo:"
    # )
    # frame_estatico.grid(sticky='nsew')

    # --- Exemplo 2: Dados da API (como o frame_dois) ---
    test_url_marcas = 'https://parallelum.com.br/fipe/api/v1/carros/marcas/'
    frame_api = FrameSelecao(
        root,
        command=on_selection_test,
        url=test_url_marcas,
        label_busca="Buscar Marca:"
    )
    frame_api.grid(sticky='nsew')

# test_url_modelos = 
# 'https://parallelum.com.br/fipe/api/v1/carros/marcas/59/modelos/'

    root.mainloop()