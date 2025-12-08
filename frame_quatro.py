import tkinter as tk
import requests
from tkinter import ttk
from tkinter import messagebox
fonte = 'Arial 12'

class Button_Quatro(tk.Frame):
    """
    Frame que exibe uma lista de anos-modelo de um veículo específico.
    Inclui uma barra de rolagem e um campo de busca para filtrar a lista.
    """
    def __init__(self, parent, url, command=None):
        """
        Construtor do Frame.

        :param parent: O widget pai (janela principal).
        :param url: A URL da API para buscar a lista de anos.
        :param command: A função (callback) a ser chamada quando um ano é 
        selecionado.
                        Receberá o código do ano-modelo como argumento 
                        (ex: '2014-1').
        """
        super().__init__(parent)
        self.parent = parent
        self.grid(row=0, column=0, sticky='nsew')
        self.grid_rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.command_callback = command
        # Variável de controle para o Radiobutton selecionado.
        self.var_ano_selecionado = tk.StringVar()
        self.url = url
        # Armazena a lista completa de anos para o filtro.
        self.all_anos = []

        self._criar_widgets()
        self.carregar_ano()

    def _criar_widgets(self):
        self.var_entry_busca = tk.StringVar()
        tk.Label(self, text="Buscar Ano-Modelo:").grid(row=0, column=0, 
                                                    sticky='w', padx=5)
        entry = tk.Entry(self, textvariable=self.var_entry_busca)
        entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        entry.bind('<KeyRelease>', self.filtrar_anos)

        # --- Canvas e Scrollbar ---
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', 
                                    command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, 
                                anchor='nw')
        self.scrollable_frame.bind('<Configure>', lambda e: self.canvas.
                                configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.grid(row=1, column=0, columnspan=2, sticky='nsew')
        self.scrollbar.grid(row=1, column=2, sticky='ns')

    def carregar_ano(self):
        """Busca os anos na API e cria os Radiobuttons."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.all_anos = response.json()
            self.atualizar_lista_radio(self.all_anos)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro de Rede", 
                                f"Não foi possível buscar os anos: {e}")

    def filtrar_anos(self, event=None):
        """
        Filtra a lista de anos com base no texto digitado no campo de busca.
        É chamado a cada tecla pressionada no Entry.

        :param event: O objeto de evento do Tkinter (não utilizado diretamente).
        """
        texto_busca = self.var_entry_busca.get().lower()
        if not texto_busca:
            anos_filtrados = self.all_anos
        else:
            anos_filtrados = [a for a in self.all_anos if texto_busca in 
                            a['nome'].lower()]
        self.atualizar_lista_radio(anos_filtrados)

    def atualizar_lista_radio(self, lista_anos):
        """
        Limpa o frame de rolagem e recria os Radiobuttons com a lista de anos 
        fornecida.

        :param lista_anos: Uma lista de dicionários, onde cada dicionário
                    representa um ano e deve conter as chaves 'nome' e 'codigo'.
        """
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        for ano in lista_anos:
            tk.Radiobutton(self.scrollable_frame, text=ano['nome'], 
                        value=ano['codigo'],variable=self.var_ano_selecionado,
                        command=self.ao_clicar).pack(anchor='w', padx=10, pady=2)

    def ao_clicar(self):
        """
        Callback executado ao clicar em um Radiobutton.
        Chama a função de callback principal com o código do ano selecionado.
        """
        if self.command_callback:
            ano_selecionado = self.var_ano_selecionado.get()
            print(f"Código do ano clicado no frame_quatro: {ano_selecionado}")
            self.command_callback(ano_selecionado)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Teste de Formulário")
    root.minsize(300,200)
    # Exemplo de URL para teste direto do arquivo
    test_url = 'https://parallelum.com.br/fipe/api/v1/carros/marcas/59/modelos/5940/anos/'
    main_button = Button_Quatro(root, url=test_url)
    root.mainloop()