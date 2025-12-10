import tkinter as tk

fonte = 'Arial 12 bold'

class FrameExibicao(tk.Frame):
    """Um frame simples para exibir conteúdo de texto com um botão de voltar."""
    def __init__(self, parent, dados_veiculo, back_command=None):
        """
        Construtor do Frame.

        :param parent: O widget pai (janela principal).
        :param dados_veiculo: Um dicionário com os dados do veículo a 
        serem exibidos.
        :param back_command: A função (callback) a ser chamada quando o
        botão 'Voltar' é clicado.
        """
        super().__init__(parent)
        self.grid(row=0, column=0, sticky='nsew')
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1) 
        # Permite que a coluna de valor se expanda

        self.dados = dados_veiculo
        self.back_command = back_command

        labels_info = {
            'Valor': 'Valor FIPE:',
            'Marca': 'Marca:',
            'Modelo': 'Modelo:',
            'AnoModelo': 'Ano do Modelo:',
            'Combustivel': 'Combustível:',
            'CodigoFipe': 'Código FIPE:',
            'MesReferencia': 'Mês de Referência:'
        }
            
        i = 0 # Contador de linha para o grid
        for i, (chave, texto_label) in enumerate(labels_info.items()):
            valor = dados_veiculo.get(chave, 'N/A')
            tk.Label(self, text=f"{texto_label}", font=fonte).grid(row=i, 
                                            column=0, sticky='e', padx=5, pady=5)
            tk.Label(self, text=f"{valor}", font='Arial 12').grid(
                                    row=i, column=1, sticky='w', padx=5, pady=5)

        # Adiciona o botão de voltar
        if self.back_command:
            tk.Button(self, text='Voltar', command=self.back_command).grid(
                                    row=i + 1,column=0, columnspan=2, pady=10)
