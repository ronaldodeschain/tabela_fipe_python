import tkinter as tk
from tkinter import messagebox
from menu import Menu
from frame_um import Button
from frame_dois import Button_Dois
from frame_tres import Button_Tres
from frame_quatro import Button_Quatro
from frame_cinco import Frame as Frame_Cinco

class App:
    """
    Classe principal da aplicação que gerencia a navegação entre as telas (frames)
    e mantém o estado da consulta do usuário (tipo de veículo, marca, modelo, etc.).
    """
    def __init__(self, root):
        self.root = root
        self.fonte = 'Arial 12'
        self.root.title('Consulta Tabela FIPE')
        self.root.minsize(400, 300)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.menu = Menu(root, new_command=self.mostrar_frame_um)

        self.base_url = 'https://parallelum.com.br/fipe/api/v1/'
        self.current_frame = None

        # Variáveis para armazenar o estado da seleção do usuário ao longo do fluxo
        self.tipo_veiculo = None
        self.codigo_marca = None
        self.modelo_marca = None
        self.ano_modelo = None
        
        # Inicia a aplicação exibindo a primeira tela de seleção
        self.mostrar_frame_um()

    def limpar_frame_atual(self):
        """Destrói o frame (tela) atualmente visível para dar lugar ao próximo."""
        if self.current_frame:
            self.current_frame.destroy()

    def mostrar_frame_um(self):
        """Exibe a tela inicial para seleção do tipo de veículo (carro, moto, 
                                                                    caminhão).
        Esta função também reseta o estado de qualquer consulta anterior.
        """
        self.limpar_frame_atual()
        # Reseta o estado para uma nova consulta
        self.tipo_veiculo = None
        self.codigo_marca = None
        self.modelo_marca = None
        self.ano_modelo = None
        self.current_frame = Button(self.root, command=self.on_veiculo_selecionado)

    def on_veiculo_selecionado(self, tipo_veiculo):
        """
        Callback executado quando um tipo de veículo é selecionado no frame_um.
        Armazena o tipo de veículo e avança para a tela de seleção de marca.

        :param tipo_veiculo: A string que representa o tipo de veículo (ex: 'carros').
        """
        self.tipo_veiculo = tipo_veiculo
        print(f"Tipo de veículo selecionado: {self.tipo_veiculo}")

        self.limpar_frame_atual()
        url_marcas = f'{self.base_url}{self.tipo_veiculo}/marcas/'
        self.current_frame = Button_Dois(self.root, url=url_marcas, 
                                        command=self.on_marca_selecionada)

    def on_marca_selecionada(self, codigo_marca):
        """
        Callback executado quando uma marca é selecionada no frame_dois.
        Armazena o código da marca e avança para a tela de seleção de modelo.

        :param codigo_marca: O código numérico da marca selecionada (ex: '59').
        """
        self.codigo_marca = codigo_marca
        print(f"Código da marca selecionada: {self.codigo_marca}")
        
        self.limpar_frame_atual()
        # Aqui você pode adicionar a lógica para o frame_tres
        url_modelos = f'{self.base_url}{self.tipo_veiculo}/marcas/{
            codigo_marca}/modelos/'
        print(f"URL para modelos: {url_modelos}")
        self.current_frame = Button_Tres(self.root,url_modelos,
                                        command=self.on_modelo_selecionado)
        
    def on_modelo_selecionado(self,modelo):
        """
        Callback executado quando um modelo é selecionado no frame_tres.
        Armazena o código do modelo e avança para a tela de seleção de ano.

        :param modelo: O código numérico do modelo selecionado (ex: '5940').
        """
        
        self.modelo_marca = modelo
        print(f"Modelo da marca selecionado: {self.modelo_marca}")
        
        self.limpar_frame_atual()
        url_marca = f'{self.base_url}{self.tipo_veiculo}/marcas/{
            self.codigo_marca}/modelos/{self.modelo_marca}/anos/'
        self.current_frame = Button_Quatro(self.root,url_marca,
                                        command=self.on_ano_selecionado)
        
    def on_ano_selecionado(self,ano):
        """
        Callback executado quando um ano é selecionado no frame_quatro.
        Armazena o ano/combustível e avança para a tela final de detalhes do veículo.

        :param ano: A string que representa o ano e o tipo de combustível (ex: '2014-1').
        """
        self.ano_modelo = ano
        print(f"Ano selecionado do modelo: {self.ano_modelo}")
        
        self.limpar_frame_atual()
        url_final = f'{self.base_url}{self.tipo_veiculo}/marcas/{
            self.codigo_marca}/modelos/{self.modelo_marca}/anos/{self.ano_modelo}/'
        # Passamos o método que volta para a tela 4 como comando
        self.current_frame = Frame_Cinco(self.root, url=url_final,
                                        command=self.mostrar_frame_quatro)
    
    def mostrar_frame_quatro(self):
        """
        Função para retornar à tela de seleção de ano (frame_quatro).
        É usada como callback para o botão 'Voltar' na tela final.
        """
        self.limpar_frame_atual()
        # Limpa a seleção de ano para permitir uma nova escolha
        self.ano_modelo = None
        url_anos = f'{self.base_url}{self.tipo_veiculo}/marcas/{
            self.codigo_marca}/modelos/{self.modelo_marca}/anos/'
        self.current_frame = Button_Quatro(self.root, url=url_anos, 
                                        command=self.on_ano_selecionado)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()