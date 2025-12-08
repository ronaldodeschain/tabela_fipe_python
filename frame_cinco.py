import tkinter as tk
import requests
from tkinter import messagebox

fonte = 'Arial 12 bold'

class Frame(tk.Frame):
    """
    Frame final que exibe os detalhes completos de um veículo consultado.
    Também contém um botão para 'Voltar'.
    """
    def __init__(self, parent, url, back_command=None, result_callback=None):
        """
        Construtor do Frame.

        :param parent: O widget pai (janela principal).
        :param url: A URL final da API para buscar os detalhes do veículo.
        :param back_command: A função (callback) a ser chamada quando o botão
        'Voltar' é clicado.
        :param result_callback: A função (callback) para passar o resultado final.
        """
        super().__init__(parent)
        self.parent = parent
        self.url = url
        self.back_command = back_command
        self.result_callback = result_callback

        self.carregar_dados_veiculo()

    def carregar_dados_veiculo(self):
        """Busca os dados finais do veículo, os exibe e os passa para o callback."""
        self.grid(row=0, column=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        dados_formatados_str = ""  # Inicializa a string de resultado
        i = -1 # Garante que 'i' exista caso a requisição falhe

        try:
            response = requests.get(self.url)
            response.raise_for_status()
            dados_veiculo = response.json()

            labels_info = {
                'Valor': 'Valor FIPE:',
                'Marca': 'Marca:',
                'Modelo': 'Modelo:',
                'AnoModelo': 'Ano do Modelo:',
                'Combustivel': 'Combustível:',
                'CodigoFipe': 'Código FIPE:',
                'MesReferencia': 'Mês de Referência:'
            }
            
            linhas_resultado = []
            for i, (chave, texto_label) in enumerate(labels_info.items()):
                valor = dados_veiculo.get(chave, 'N/A')
                tk.Label(self, text=f"{texto_label}", font=fonte).grid(row=i, 
                                            column=0, sticky='e', padx=5, pady=5)
                tk.Label(self, text=f"{valor}", font='Arial 12').grid(
                                    row=i, column=1, sticky='w', padx=5, pady=5)
                linhas_resultado.append(f"{texto_label} {valor}")
            
            dados_formatados_str = "\n".join(linhas_resultado)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro de Rede", 
                            f"Não foi possível buscar os dados do veículo: {e}")
        
        # Passa o resultado para o callback na classe App, se existir
        if self.result_callback:
            self.result_callback(dados_formatados_str)

        # Adiciona o botão de voltar, usando o back_command diretamente
        if self.back_command:
            tk.Button(self,text='Voltar',command=self.back_command).grid(row=i+1,
                                                column=0,columnspan=2, pady=10)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Teste de Formulário")
    root.minsize(300,200)
    # Exemplo de URL para teste direto do arquivo
    test_url = 'https://parallelum.com.br/fipe/api/v1/carros/marcas/59/modelos/5940/anos/2014-1'
    main_button = Frame(root, url=test_url)
    root.mainloop()