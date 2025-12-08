import tkinter as tk
from tkinter import messagebox, filedialog
from menu import Menu
from frame_um import Button
from frame_dois import Button_Dois
from frame_tres import Button_Tres
from frame_quatro import Button_Quatro
from frame_cinco import Frame as Frame_Cinco

class FrameExibicao(tk.Frame):
    """Um frame simples para exibir conteúdo de texto com um botão de voltar."""
    def __init__(self, parent, content, back_command):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky='nsew')
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        label = tk.Label(self, text=content, justify=tk.LEFT, anchor="nw", 
                        wraplength=380)
        label.pack(expand=True, fill='both', padx=10, pady=10)

        back_button = tk.Button(self, text="Voltar", command=back_command)
        back_button.pack(pady=10)

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
        self.menu = Menu(
            self.root, 
            restart_command=self.mostrar_frame_um,
            open_command=self.abrir_arquivo,
            save_as_command=self.salvar_como
        )

        self.base_url = 'https://parallelum.com.br/fipe/api/v1/'
        self.current_frame = None
        self.resultado_final = None #salva o endereço final para salvar depois

        # Variáveis para armazenar o estado da seleção do usuário ao longo 
        # do fluxo
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
        self.resultado_final = None
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
        Armazena o ano/combustível e avança para a tela final de detalhes do 
        veículo.

        :param ano: A string que representa o ano e o tipo de combustível 
        (ex: '2014-1').
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
            back_command=self.mostrar_frame_um,
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
        self.current_frame = Button_Quatro(self.root, url=url_anos, 
                                        command=self.on_ano_selecionado)

    def on_resultado_obtido(self,resultado):
        """Salva os dados do resultado final no estado de aplicação."""
        self.resultado_final = resultado
    
    def abrir_arquivo(self):
        """Abre um arquivo de texto e exibe seu conteúdo em um novo frame."""
        filepath = filedialog.askopenfilename(
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if not filepath:
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                print(content) #posso adicionar aqui a logica de criar a lista?
            self.limpar_frame_atual()
            self.current_frame = FrameExibicao(self.root, content, 
                                            back_command=self.mostrar_frame_um)
        except Exception as e:
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
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt"), 
                    ('Arquivos Json','*,json'), ("Todos os arquivos", "*.*")]
        )

        if not filepath:
            return  # Usuário cancelou a janela de salvar

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.resultado_final)
            messagebox.showinfo("Sucesso", f"Consulta salva em:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Erro ao Salvar", f"Ocorreu um erro ao tentar salvar o arquivo: {e}")

        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()