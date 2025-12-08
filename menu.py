import tkinter as tk
from tkinter import messagebox

class Menu:
    """
    Cria e gerencia a barra de menu principal (File, etc.) para a janela da aplicação.
    """
    def __init__(self, root_window, new_command=None):
        """
        Construtor da classe Menu.

        :param root_window: A janela principal (tk.Tk) onde o menu será inserido.
        :param new_command: A função (callback) a ser executada quando o item de menu 'New' é clicado.
        """
        main_menu = tk.Menu(root_window)
        root_window.config(menu=main_menu)
        self.new_command = new_command

        # --- Menu "File" ---
        file_menu = tk.Menu(main_menu, tearoff=0)
        # O comando 'New' chama o método 'iniciar_nova_consulta'.
        file_menu.add_command(label='New', command=self.iniciar_nova_consulta)
        file_menu.add_command(label='Open')
        file_menu.add_command(label='Save')
        file_menu.add_separator()
        # O comando 'Exit' fecha a aplicação.
        file_menu.add_command(label='Exit', command=root_window.destroy)
        
        # Adiciona o menu "File" à barra de menu principal.
        main_menu.add_cascade(label='File', menu=file_menu)

    def iniciar_nova_consulta(self):
        """
        Função chamada pelo item de menu 'New'.
        Executa o comando de callback fornecido no construtor para reiniciar
        o fluxo da aplicação.
        """
        if self.new_command:
            self.new_command()
            print('Aplicação reiniciada para a primeira tela')
            

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Teste de Menu")
    root.geometry("300x200")
    menu_app = Menu(root)
    root.mainloop()