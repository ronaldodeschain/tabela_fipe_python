import tkinter as tk
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Garante que o backend do Matplotlib seja compatível com o Tkinter
matplotlib.use("TkAgg")


class FrameGrafico(tk.Frame):
    """
    Um Frame que exibe um gráfico de barras comparando os valores de veículos
    e permite adicionar mais veículos ao gráfico a partir de arquivos.
    """
    def __init__(self, parent, dados, add_command=None, back_command=None,
                 save_graphic=None):
        """
        Construtor do FrameGrafico.

        :param parent: O widget pai.
        :param dados: (list) Uma lista de dicionários, onde cada dicionário
                    representa um veículo com suas informações.
        :param add_command: (function, opcional) Callback para o botão
                            'Adicionar Veículo'.
        :param back_command: (function, opcional) Callback para o botão
                            'Voltar'.
        :para save_command: (function, opcional) Callback para o botão
                            'Salvar Gráfico'.
        """
        super().__init__(parent)
        self.grid(row=0, column=0, sticky='nsew')
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.dados = dados
        self.add_command = add_command
        self.back_command = back_command
        self.save_graphic= save_graphic

        # Configura o grid do frame para o gráfico e os botões
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # --- Criação do Gráfico Matplotlib ---
        self.figura = Figure(figsize=(10, 5), dpi=100)
        self.ax = self.figura.add_subplot(111)

        # --- Integração do Gráfico com Tkinter ---
        self.canvas = FigureCanvasTkAgg(self.figura, self)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, 
                                        sticky='nsew', padx=10, pady=10)

        # --- Botões de Ação ---
        botoes_frame = tk.Frame(self)
        botoes_frame.grid(row=1, column=0, columnspan=2, pady=10)

        if self.add_command:
            tk.Button(botoes_frame, text="Adicionar Veículo ao Gráfico", 
                    command=self.add_command).pack(side=tk.LEFT, padx=5)
        
        if self.back_command:
            tk.Button(botoes_frame, text="Voltar", 
                    command=self.back_command).pack(side=tk.LEFT, padx=5)

        if self.save_graphic:
            tk.Button(botoes_frame, text="Salvar Gráfico", 
                    command=self.save_graphic).pack(side=tk.LEFT, padx=5)

        # Atualiza o gráfico com os dados atuais
        self.atualizar_grafico()

    def atualizar_grafico(self):
        """Limpa e redesenha o gráfico de barras com os dados atuais."""
        # Limpa o eixo para o redesenho, evitando sobreposição de gráficos.
        self.ax.clear()

        # Se não houver dados, exibe uma mensagem e interrompe.
        if not self.dados:
            self.ax.set_title("Nenhum dado para exibir")
            self.canvas.draw()
            return

        # --- Preparação dos Dados para o Gráfico ---
        # Cria os rótulos para o eixo X, combinando Marca, Modelo e Ano.
        modelos = [f"{d.get('Marca', 'N/A')} - {d.get('Modelo', 'N/A'
                )}\n({d.get('AnoModelo', 'N/A')})" for d in self.dados]
        # Extrai os valores como strings formatadas (ex: "R$ 15.342,00").
        valores_str = [d.get('Valor', 'R$ 0') for d in self.dados]
        
        # Converte os valores de string para float para que possam ser plotados.
        valores_float = []
        for v_str in valores_str:
            # Limpa a string, removendo 'R$ ', '.' (milhar) e 
            # trocando ',' por '.' (decimal).
            valor_limpo = v_str.replace('R$ ', '').replace('.', ''
                                                        ).replace(',', '.')
            valores_float.append(float(valor_limpo))

        # --- Desenho do Gráfico ---
        # Cria as barras do gráfico.
        self.ax.bar(modelos, valores_float)
        self.ax.set_ylabel('Valor (R$)')
        self.ax.set_title('Comparação de Preços de Veículos (Tabela FIPE)')

        # Adiciona rótulos de valor no topo das barras
        for i, v_float in enumerate(valores_float):
            self.ax.text(i, v_float, valores_str[i], ha='center', va='bottom')

        # Ajusta a rotação dos rótulos do eixo X para evitar sobreposição.
        self.figura.autofmt_xdate(rotation=15, ha='right')
        # Garante que todos os elementos do gráfico (títulos, rótulos) caibam 
        # na figura.
        self.figura.tight_layout()
        # Redesenha o canvas do Tkinter com o gráfico atualizado.
        self.canvas.draw()