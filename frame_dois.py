import tkinter as tk
from tkinter import ttk
import requests
from tkinter import messagebox
#{nova_url}154/modelos/
fonte = 'Arial 12'

class Button_Dois(tk.Frame):
    """
    Frame que exibe uma lista de marcas de veículos obtidas de uma API.
    Inclui uma barra de rolagem e um campo de busca para filtrar a lista.
    """
    def __init__(self, parent, url, command=None):
        """
        Construtor do Frame.

        :param parent: O widget pai (janela principal).
        :param url: A URL da API para buscar a lista de marcas.
        :param command: A função (callback) a ser chamada quando uma marca é 
        selecionada.
                        Receberá o código da marca como argumento.
        """
        super().__init__(parent)
        self.parent = parent
        self.grid(row=0, column=0, sticky='nsew') 
        self.grid_rowconfigure(1, weight=1) # Linha 1 (canvas) vai expandir
        self.grid_columnconfigure(0, weight=1)

        self.command_callback = command
        # Variável de controle para o Radiobutton selecionado.
        self.var_marca_selecionada = tk.StringVar()
        self.url = url
        # Armazena a lista completa de marcas para evitar múltiplas chamadas à API.
        self.all_marcas = [] 

        self._criar_widgets()
        self.carregar_marcas()

    def _criar_widgets(self):
        # --- Campo de Busca ---
        self.var_entry_busca = tk.StringVar()
        tk.Label(self, text="Buscar Marca:").grid(row=0, column=0, sticky='w', 
                                                padx=5)
        entry = tk.Entry(self, textvariable=self.var_entry_busca)
        entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        # O evento <KeyRelease> chama o filtro toda vez que uma tecla é solta
        entry.bind('<KeyRelease>', self.filtrar_marcas)

        # 1. Criar um Canvas e a Scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', 
                                    command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # 2. Criar um Frame DENTRO do Canvas para colocar os Radiobuttons
        self.scrollable_frame = tk.Frame(self.canvas)

        # 3. Adicionar o frame ao canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame,
                                                        anchor='nw')

        # 4. Configurar o evento para atualizar a área de rolagem
        self.scrollable_frame.bind('<Configure>', lambda e: 
            self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        # 5. Posicionar o Canvas e a Scrollbar na tela
        self.canvas.grid(row=1, column=0, columnspan=2, sticky='nsew')
        self.scrollbar.grid(row=1, column=2, sticky='ns')

    def carregar_marcas(self):
        """Busca as marcas na API e cria os Radiobuttons."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.all_marcas = response.json() # Armazena a lista completa
            self.atualizar_lista_radio(self.all_marcas) # Exibe a lista inicial
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro de Rede", 
                                f"Não foi possível buscar as marcas: {e}")

    def filtrar_marcas(self, event=None):
        """
        Filtra a lista de marcas com base no texto digitado no campo de busca.
        É chamado a cada tecla pressionada no Entry.

        :param event: O objeto de evento do Tkinter (não utilizado diretamente).
        """
        texto_busca = self.var_entry_busca.get().lower()
        if not texto_busca:
            marcas_filtradas = self.all_marcas
        else:
            marcas_filtradas = [m for m in self.all_marcas if
                                texto_busca in m['nome'].lower()]
        
        self.atualizar_lista_radio(marcas_filtradas)

    def atualizar_lista_radio(self, lista_marcas):
        """
        Limpa o frame de rolagem e recria os Radiobuttons com a lista de marcas 
        fornecida.

        :param lista_marcas: Uma lista de dicionários, onde cada dicionário
                representa uma marca e deve conter as chaves 'nome' e 'codigo'.
        """
        # Limpa os widgets antigos do frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Cria os novos Radiobuttons
        for marca in lista_marcas:
            tk.Radiobutton(self.scrollable_frame, text=marca['nome'], 
                        value=marca['codigo'],variable=self.var_marca_selecionada,
                        command=self.ao_clicar).pack(anchor='w', padx=10, pady=2)

    def ao_clicar(self):
        """
        Callback executado ao clicar em um Radiobutton.
        Chama a função de callback principal com o código da marca selecionada.
        """
        if self.command_callback:
            valor_selecionado = self.var_marca_selecionada.get()
            print(f"Código da marca clicado no frame_dois: {valor_selecionado}")
            self.command_callback(valor_selecionado)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Teste de Formulário")
    root.minsize(300,200)
    # Exemplo de URL para teste direto do arquivo
    test_url = 'https://parallelum.com.br/fipe/api/v1/carros/marcas/'
    main_button = Button_Dois(root, url=test_url)
    root.mainloop()