"""
Modulo principal da aplicação. Implementa as lógicas de consulta e redireciona
para os módulos responsáveis por exibir e manipular os dados.
"""
from tkinter import messagebox, filedialog
import json
from menu import Menu
from frame_cinco import Frame as Frame_Cinco
from frame_selecao import FrameSelecao
from frame_grafico import FrameGrafico
# pylint: disable=too-many-instance-attributes
# 11 is reasonable in this case
class App:
    """
    Classe principal da aplicação que gerencia a navegação entre as telas (frames)
    e mantém o estado da consulta do usuário (tipo de veículo, marca, modelo, etc.).
    """
    def __init__(self, root):
        # --- Configuração da Janela Principal ---
        self.root = root
        self.fonte = 'Arial 12'
        self.root.title('Consulta Tabela FIPE')
        self.root.minsize(400, 300)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.menu = Menu(
            # A classe Menu é instanciada com referências aos métodos da App
            # que devem ser executados quando um item de menu é clicado.
            self.root,
            #mapeia para o menu os comandos a passar
            restart_command=self.mostrar_frame_um,
            open_command=self.abrir_arquivo,
            save_as_command=self.salvar_como,
            load_graphic=self.gerar_grafico,
            about_us=self.sobre_nos
        )

        # --- Estado da Aplicação ---
        self.base_url = 'https://parallelum.com.br/fipe/api/v1/'
        self.current_frame = None

        # `resultado_final` armazena o dicionário do último veículo consultado via API.
        self.resultado_final = None
        # `dados` é uma lista que acumula os dicionários de todos os veículos
        # carregados (via API ou arquivo), usada para popular o gráfico.
        self.dados = []
        # Variáveis de estado que armazenam as seleções do usuário passo a passo.
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
        # Reseta todas as variáveis de estado para iniciar uma nova consulta do zero.
        self.tipo_veiculo = None
        self.codigo_marca = None
        self.modelo_marca = None
        self.ano_modelo = None
        self.resultado_final = None # Limpa o resultado da consulta FIPE
        self.current_frame = FrameSelecao(
            self.root,
            # `command` especifica qual método chamar quando uma opção for selecionada.
            command=self.on_veiculo_selecionado,
            dados_estaticos=['carros', 'motos', 'caminhoes'],
            label_busca="Selecione o Tipo:"
        )

    def on_veiculo_selecionado(self, tipo_veiculo):
        """
        Callback executado quando um tipo de veículo é selecionado no frame_um.
        Armazena o tipo de veículo e avança para a tela de seleção de marca.

        :param tipo_veiculo: (str) O tipo de veículo selecionado.
                            Ex: 'carros'
        """
        self.tipo_veiculo = tipo_veiculo
        print(f"Tipo de veículo selecionado: {self.tipo_veiculo}")

        self.limpar_frame_atual()
        url_marcas = f'{self.base_url}{self.tipo_veiculo}/marcas/'
        self.current_frame = FrameSelecao(
            self.root,
            url=url_marcas,
            command=self.on_marca_selecionada,
            label_busca="Buscar Marca:")

    def on_marca_selecionada(self, codigo_marca):
        """
        Callback executado quando uma marca é selecionada no frame_dois.
        Armazena o código da marca e avança para a tela de seleção de modelo.

        :param codigo_marca: (str) O código da marca selecionada. Ex: '59'
        """
        self.codigo_marca = codigo_marca
        print(f"Código da marca selecionada: {self.codigo_marca}")

        self.limpar_frame_atual()
        # Aqui você pode adicionar a lógica para o frame_tres
        url_modelos = f'{self.base_url}{self.tipo_veiculo}/marcas/{
            codigo_marca}/modelos/'
        print(f"URL para modelos: {url_modelos}")
        self.current_frame = FrameSelecao(
            self.root,
            url=url_modelos,
            command=self.on_modelo_selecionado,
            label_busca="Buscar Modelo:",
            chave_json='modelos')

    def on_modelo_selecionado(self,modelo):
        """
        Callback executado quando um modelo é selecionado no frame_tres.
        Armazena o código do modelo e avança para a tela de seleção de ano.

        :param modelo: (str) O código do modelo selecionado. Ex: '5940'
        """

        self.modelo_marca = modelo
        print(f"Modelo da marca selecionado: {self.modelo_marca}")

        self.limpar_frame_atual()
        url_marca = f'{self.base_url}{self.tipo_veiculo}/marcas/{
            self.codigo_marca}/modelos/{self.modelo_marca}/anos/'
        self.current_frame = FrameSelecao(
            self.root,
            url=url_marca,
            command=self.on_ano_selecionado,
            label_busca="Buscar Ano-Modelo:")

    def on_ano_selecionado(self,ano):
        """
        Callback executado quando um ano é selecionado no frame_quatro.
        Armazena o ano/combustível e avança para a tela final de detalhes do 
        veículo.

        :param ano: (str) O código do ano-modelo selecionado.
                    Ex: '2014-1'
        """
        self.ano_modelo = ano
        print(f"Ano selecionado do modelo: {self.ano_modelo}")

        self.limpar_frame_atual()
        url_final = f'{self.base_url}{self.tipo_veiculo}/marcas/{
            self.codigo_marca}/modelos/{self.modelo_marca}/anos/{self.ano_modelo}/'
        # Passamos o método que volta para a tela 4 como comando
        self.current_frame = Frame_Cinco(
            self.root,
            url=url_final,
            # O botão 'Voltar' na tela final reinicia o fluxo.
            back_command=self.mostrar_frame_um,
            # Passa o método que vai receber o dicionário com os dados do veículo.
            result_callback=self.on_resultado_obtido
        )

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
        self.current_frame = FrameSelecao(
            self.root,
            url=url_anos,
            command=self.on_ano_selecionado,
            label_busca="Buscar Ano-Modelo:")

    def on_resultado_obtido(self,resultado):
        """
        Callback que recebe os dados do veículo da tela final (Frame_Cinco).
        Armazena o dicionário para a função 'Salvar' e o adiciona à lista
        de dados para o gráfico.

        :param resultado: (dict) Dicionário com os dados completos do veículo.
        """
        self.resultado_final = resultado
        self.dados.append(resultado)

    def abrir_arquivo(self, recarregar_frame_grafico=False):
        """
        Abre um seletor de arquivos para carregar um veículo de um arquivo JSON.
        """
        filepath = filedialog.askopenfilename(
            filetypes=[('Arquivos JSON', '*.json'), ("Todos os arquivos", "*.*")]
        )
        if not filepath:
            return

        try:
            # Lê o arquivo JSON e o converte de volta para um dicionário Python.
            with open(filepath, 'r', encoding='utf-8') as f:
                dados_veiculo = json.load(f)

            self.dados.append(dados_veiculo) # Adiciona o dicionário à lista

            # Se a função foi chamada a partir do gráfico, recarrega o gráfico.
            if recarregar_frame_grafico:
                self.gerar_grafico() # Recarrega o gráfico com os novos dados
            # Caso contrário, exibe os dados do arquivo na tela de exibição.
            else:
                self.limpar_frame_atual()
                # Reutiliza o Frame_Cinco para exibir dados do arquivo
                self.current_frame = Frame_Cinco(self.root,
                dados_veiculo=dados_veiculo,back_command=self.mostrar_frame_um)
        except FileNotFoundError as e:
            messagebox.showerror("Erro ao Abrir",
                                f"Não foi possível ler o arquivo: {e}")
    def salvar_como(self):
        """Abre o diálogo para salvar o arquivo."""
        self.salvar_arquivo()

    def salvar_arquivo(self):
        """Abre a janela de diálogo para salvar o arquivo com o resultado."""
        if not self.resultado_final:
            messagebox.showwarning("Aviso",
                "Nenhum resultado para salvar. Realize uma consulta primeiro.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[('Arquivos JSON', '*.json'), ("Todos os arquivos", "*.*")]
        )

        if not filepath:
            return  # Usuário cancelou a janela de salvar
        try:
            # Usa json.dump para escrever o dicionário no arquivo de forma
            # formatada.
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.resultado_final, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Sucesso", f"Consulta salva em:\n{filepath}")
        except IOError as e:
            messagebox.showerror("Erro ao Salvar",
                            f"Ocorreu um erro ao tentar salvar o arquivo: {e}")

    def adicionar_veiculo_ao_grafico(self):
        """
        Abre um arquivo e adiciona seus dados à lista, depois recarrega o gráfico.
        """
        self.abrir_arquivo(recarregar_frame_grafico=True)

    def gerar_grafico(self):
        """
        Limpa a tela atual e exibe o FrameGrafico, passando a lista de dados
        acumulados (`self.dados`) para serem plotados.
        """
        self.limpar_frame_atual()
        self.current_frame = FrameGrafico(
            self.root,
            self.dados,
            add_command=self.adicionar_veiculo_ao_grafico,
            back_command=self.mostrar_frame_um,
            save_graphic=self.salvar_grafico
        )

    def salvar_grafico(self):
        """
        Salva o grafico gerado pelo usuário para ser acessado externamente.
        
        :param return grafico.jpg
        """

    #https://voiston.com/
    texto = "Scooby Doo!"

    def sobre_nos(self):
        """
        Messagebox que exibe um resumo da aplicação e seu desenvolvedor.
        Exibe os canais de contato e link para o site.
        
        :param self: Message
        """
        messagebox.showinfo("Exibindo o sobre",f'{self.texto}')
