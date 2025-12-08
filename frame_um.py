import tkinter as tk
from tkinter import messagebox

class Button(tk.Frame):
    """
    Frame inicial da aplicação que exibe as opções de tipo de veículo
    (carros, motos, caminhoes) para o usuário selecionar.
    """
    def __init__(self, parent, command=None):
        """
        Construtor do Frame.

        :param parent: O widget pai (geralmente a janela principal 'root').
        :param command: A função (callback) a ser chamada quando uma opção é 
        selecionada.
                        Esta função receberá o tipo de veículo como argumento 
                        (ex: 'carros').
        """
        super().__init__(parent)
        self.parent = parent
        self.grid(row=0, column=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.command_callback = command
        self.dados_validos = ['carros', 'motos', 'caminhoes']

        # Variável de controle do Tkinter para armazenar a seleção do Radiobutton.
        self.var_tipo_veiculo = tk.StringVar()

        self._criar_widgets()

    def _criar_widgets(self):
        """Cria e posiciona os widgets na tela."""
        tk.Label(self, text='Selecione uma opção:').grid(
                                                row=2, column=0, columnspan=2,
                                                sticky='w', padx=5, pady=(10,0))
        
        # Cria um Radiobutton para cada tipo de veículo disponível.
        for i, dado in enumerate(self.dados_validos):
            tk.Radiobutton(self, text=f'{dado.capitalize()}', value=dado, 
                    variable=self.var_tipo_veiculo, 
                    command=self.ao_clicar_radio).grid(
                        row=i+3, column=0, sticky='w', padx=150, pady=2)
            
    def ao_clicar_radio(self):
        """
        Função chamada sempre que um Radiobutton é clicado.
        Obtém o valor selecionado e o passa para a função de callback principal.
        """
        if self.command_callback:
            valor_selecionado = self.var_tipo_veiculo.get()
            self.command_callback(valor_selecionado)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Teste de Formulário")
    root.minsize(300, 200)
    main_button = Button(root)
    root.mainloop()    
