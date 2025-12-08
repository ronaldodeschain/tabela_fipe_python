import tkinter as tk
from tkinter import ttk
import requests
from tkinter import messagebox
fonte = 'Arial 12'

class Button_Tres(tk.Frame):
    """
    Frame que exibe uma lista de modelos de veículos obtidos de uma API.
    Inclui uma barra de rolagem e um campo de busca para filtrar a lista.
    """
    def __init__(self, parent, url, command=None):
        """
        Construtor do Frame.

        :param parent: O widget pai (janela principal).
        :param url: A URL da API para buscar a lista de modelos.
        :param command: A função (callback) a ser chamada quando um modelo é 
        selecionado.
                        Receberá o código do modelo como argumento.
        """
        super().__init__(parent)
        self.parent = parent
        self.grid(row=0, column=0, sticky='nsew')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.command_callback = command
        # Variável de controle para o Radiobutton selecionado.
        self.var_modelo_selecionado = tk.StringVar()
        self.url = url
        # Armazena a lista completa de modelos para o filtro.
        self.all_modelos = []

        self._criar_widgets()
        self.carregar_modelos()

    def _criar_widgets(self):
        """Cria e posiciona os widgets na tela."""
        self.var_entry_busca = tk.StringVar()
        tk.Label(self,text="Buscar Modelo:").grid(row=0,column=0,sticky='w',
                                        padx=5)
        entry = tk.Entry(self,textvariable=self.var_entry_busca)
        entry.grid(row=0,column=1,sticky='ew',padx=5,pady=5)
        # <keyrelease> cuida do filtro
        entry.bind('<KeyRelease>',self.filtrar_modelos)
        
        # --- Canvas e Scrollbar para a lista de modelos ---
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self,orient='vertical',
                                    command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)    
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0,0),window=self.scrollable_frame,anchor='nw')
        self.scrollable_frame.bind('<Configure>',lambda e:self.canvas.configure
                        (scrollregion=self.canvas.bbox('all')))
        
        self.canvas.grid(row=1,column=0,columnspan=2,sticky='nsew')
        self.scrollbar.grid(row=1,column=2,sticky='ns')

    def carregar_modelos(self):
        """Busca os modelos na API e cria os Radiobuttons."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            # A API retorna um dicionário com uma chave "modelos" que contém a lista
            dados = response.json()
            self.all_modelos = dados.get('modelos', []) # Pega a lista do JSON
            self.atualizar_lista_radio(self.all_modelos) # Exibe a lista inicial
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro de Rede", f"Não foi possível buscar os modelos: {e}")

    def filtrar_modelos(self,event=None):
        """
        Filtra a lista de modelos com base no texto digitado no campo de busca.
        É chamado a cada tecla pressionada no Entry.

        :param event: O objeto de evento do Tkinter (não utilizado diretamente).
        """
        texto_busca = self.var_entry_busca.get().lower()
        if not texto_busca:
            modelos_filtrados = self.all_modelos
        else:
            modelos_filtrados = [m for m in self.all_modelos if texto_busca
                                in m['nome'].lower()]
            
        self.atualizar_lista_radio(modelos_filtrados)
    
    def atualizar_lista_radio(self,lista_modelos):
        """
        Limpa o frame de rolagem e recria os Radiobuttons com a lista de
        modelos fornecida.

        :param lista_modelos: Uma lista de dicionários, onde cada dicionário
                representa um modelo e deve conter as chaves 'nome' e 'codigo'.
        """
        #limpa os widgets antigos
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        #cria os novos radios
        for modelo in lista_modelos:
            tk.Radiobutton(self.scrollable_frame, text=modelo['nome'], 
                        value=modelo['codigo'],
                        variable=self.var_modelo_selecionado,
                        command=self.ao_clicar).pack(anchor='w', padx=10, pady=2)
    def ao_clicar(self):
        """
        Callback executado ao clicar em um Radiobutton.
        Chama a função de callback principal com o código do modelo selecionado.
        """
        if self.command_callback:
            modelo_selecionado = self.var_modelo_selecionado.get()
            print(f"Código do modelo clicado no frame_tres: {modelo_selecionado}")
            self.command_callback(modelo_selecionado)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Teste de Formulário")
    root.minsize(300,200)
    # Exemplo de URL para teste direto do arquivo
    test_url = 'https://parallelum.com.br/fipe/api/v1/carros/marcas/59/modelos/'
    main_button = Button_Tres(root, url=test_url)
    root.mainloop()