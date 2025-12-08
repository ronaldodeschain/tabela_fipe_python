import tkinter as tk
import requests
from tkinter import messagebox
fonte = 'Arial 12 bold'

class Frame(tk.Frame):
    """
    Frame final que exibe os detalhes completos de um veículo consultado.
    Também contém botões para 'Voltar' ou 'Salvar' a pesquisa.
    """
    def __init__(self, parent, url, command=None):
        """
        Construtor do Frame.

        :param parent: O widget pai (janela principal).
        :param url: A URL final da API para buscar os detalhes do veículo.
        :param command: A função (callback) a ser chamada quando o botão 
        'Voltar' é clicado.
        """
        super().__init__(parent)
        self.parent = parent
        self.url = url
        self.command_callback = command

        self.carregar_dados_veiculo()

    def carregar_dados_veiculo(self):
        """Busca os dados finais do veículo e os exibe em labels."""
        self.grid(row=0, column=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        try:
            # Faz a requisição à API para obter os detalhes do veículo.
            response = requests.get(self.url)
            response.raise_for_status()
            dados_veiculo = response.json()

            # Dicionário para mapear chaves da API para texto de exibição
            labels_info = {
                'Valor': 'Valor FIPE:',
                'Marca': 'Marca:',
                'Modelo': 'Modelo:',
                'AnoModelo': 'Ano do Modelo:',
                'Combustivel': 'Combustível:',
                'CodigoFipe': 'Código FIPE:',
                'MesReferencia': 'Mês de Referência:'
            }

            # Itera sobre o dicionário para criar e posicionar os labels de 
            # forma dinâmica.
            for i, (chave, texto_label) in enumerate(labels_info.items()):
                valor = dados_veiculo.get(chave, 'N/A')
                tk.Label(self, text=f"{texto_label}", font=fonte).grid(row=i, 
                                            column=0, sticky='e', padx=5, pady=5)
                tk.Label(self, text=f"{valor}", font='Arial 12').grid(
                                    row=i, column=1, sticky='w', padx=5, pady=5)
            
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro de Rede", 
                                f"Não foi possível buscar os dados do veículo: {e}")
            # Se houver erro, a variável 'i' pode não ter sido definida.
            # Definimos um valor padrão para que os botões possam ser criados
            # mesmo assim.
            i = -1 

        # Adiciona os botões de ação na parte inferior da tela.
        tk.Button(self, text='Voltar', command=self.voltar_tela).grid(row=i+1, 
                                                column=0, columnspan=2, pady=10)
        tk.Button(self,text='Salvar',command=self.salvar_pesquisa).grid(row=i+1,
                                                column=1,columnspan=2,padx=10)
    def voltar_tela(self):
        """Chama a função de callback (se existir) para retornar à tela anterior."""
        if self.command_callback:
            self.command_callback()

    def salvar_pesquisa(self):
        """Função placeholder para a lógica de salvar a pesquisa."""
        #logica para salvar em json?
        pass 
    
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Teste de Formulário")
    root.minsize(300,200)
    # Exemplo de URL para teste direto do arquivo
    test_url = 'https://parallelum.com.br/fipe/api/v1/carros/marcas/59/modelos/5940/anos/2014-1'
    main_button = Frame(root, url=test_url)
    root.mainloop()