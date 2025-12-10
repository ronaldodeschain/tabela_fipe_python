import tkinter as tk
import requests
from tkinter import messagebox

fonte = 'Arial 12 bold'

class Frame(tk.Frame):
    """
    Frame que exibe os detalhes completos de um veículo, seja a partir de uma
    consulta via API (URL) ou de dados já carregados (dicionário).
    """
    def __init__(self, parent, url=None, dados_veiculo=None, back_command=None, 
                result_callback=None):
        """
        Construtor do Frame.

        :param parent: O widget pai (janela principal).
        :param url: (Opcional) A URL da API para buscar os detalhes do veículo.
        :param dados_veiculo: (Opcional) Um dicionário com os dados do veículo.
        :param back_command: A função (callback) a ser chamada quando o botão
        'Voltar' é clicado.
        :param result_callback: A função (callback) para passar o dicionário de
        dados do resultado.
        """
        super().__init__(parent)
        self.grid(row=0, column=0, sticky='nsew')
        self.columnconfigure(1, weight=1) # Coluna de valor se expande

        self.back_command = back_command
        self.result_callback = result_callback

        if url:
            self._carregar_dados_da_url(url)
        elif dados_veiculo:
            self._exibir_dados(dados_veiculo)
        else:
            tk.Label(self, text="Nenhuma informação para exibir.").pack()

    def _carregar_dados_da_url(self, url):
        """Busca os dados da API e chama a função de exibição."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            dados_veiculo = response.json()
            self._exibir_dados(dados_veiculo)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro de Rede", 
                            f"Não foi possível buscar os dados do veículo: {e}")
            # Mesmo com erro, mostra o botão de voltar
            if self.back_command:
                tk.Button(self, text='Voltar', command=self.back_command).grid(
                    row=0, column=0, columnspan=2, pady=10)

    def _exibir_dados(self, dados_veiculo):
        """Cria os labels na tela para exibir os dados do veículo."""
        labels_info = {
            'Valor': 'Valor FIPE:',
            'Marca': 'Marca:',
            'Modelo': 'Modelo:',
            'AnoModelo': 'Ano do Modelo:',
            'Combustivel': 'Combustível:',
            'CodigoFipe': 'Código FIPE:',
            'MesReferencia': 'Mês de Referência:'
        }
        
        i = 0
        for i, (chave, texto_label) in enumerate(labels_info.items()):
            valor = dados_veiculo.get(chave, 'N/A')
            tk.Label(self, text=f"{texto_label}", font=fonte).grid(row=i, 
                                        column=0, sticky='e', padx=5, pady=5)
            tk.Label(self, text=f"{valor}", font='Arial 12').grid(
                                row=i, column=1, sticky='w', padx=5, pady=5)
        
        # Passa o dicionário de dados para o callback na classe App
        if self.result_callback:
            self.result_callback(dados_veiculo)

        # Adiciona o botão de voltar
        if self.back_command:
            tk.Button(self, text='Voltar', command=self.back_command).grid(
                row=i + 1, column=0, columnspan=2, pady=10)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Teste de Formulário")
    root.minsize(300,200)
    # Exemplo de teste com URL
    test_url = 'https://parallelum.com.br/fipe/api/v1/carros/marcas/59/modelos/5940/anos/2022-3'
    main_button = Frame(root, url=test_url)
    root.mainloop()