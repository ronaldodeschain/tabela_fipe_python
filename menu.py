import tkinter as tk

class Menu:
    """
    Cria e gerencia a barra de menu principal (File, etc.) para a janela da 
    aplicação.
    Esta classe é responsável apenas pela UI do menu, delegando as ações para 
    os comandos (callbacks) fornecidos.
    """
    def __init__(self, root_window, restart_command=None, open_command=None, 
                save_as_command=None, load_graphic=None,about_us=None):
        """
        Construtor da classe Menu.

        :param root_window: A janela principal (tk.Tk) onde o menu 
        será inserido.
        :param restart_command: Callback a ser executado para o item 
        de menu 'Novo'.
        :param open_command: Callback a ser executado para o item de menu 'Abrir'.
        :param save_as_command: Callback a ser executado para o item 
        de menu 'Salvar Como...'.
        :param load_graphic: Callback a ser executado para o item de
        menu 'Carregar Gráfico'.
        """
        main_menu = tk.Menu(root_window)
        root_window.config(menu=main_menu)

        # --- Menu "Arquivo" ---
        file_menu = tk.Menu(main_menu, tearoff=0)
        
        # Conecta os itens de menu diretamente aos callbacks fornecidos
        if restart_command:
            file_menu.add_command(label='Novo', command=restart_command)
        
        if open_command:
            file_menu.add_command(label='Abrir', command=open_command)

        if save_as_command:
            file_menu.add_command(label='Salvar como...', command=save_as_command)

        
        file_menu.add_separator()
        file_menu.add_command(label='Sair', command=root_window.destroy)

        
        # -- Menu Secundário -- 
        graphic_menu = tk.Menu(main_menu, tearoff=0)
        if load_graphic:
            graphic_menu.add_command(label='Carregar Gráfico',
                                    command=load_graphic)

        # -- Menu Help -- 
        help_menu = tk.Menu(main_menu, tearoff=0)
        if about_us:
            help_menu.add_command(label='Sobre',command=about_us)
        

        # -- Constrói a estrutura do Menu -- 
        main_menu.add_cascade(label='Arquivo', menu=file_menu)
        main_menu.add_cascade(label='Gráfico', menu=graphic_menu)
        main_menu.add_cascade(label='Ajuda', menu=help_menu)

if __name__ == '__main__':
    # Bloco para teste visual do componente de menu
    def mock_action(action_name):
        print(f"Ação '{action_name}' foi chamada!")

    root = tk.Tk()
    root.title("Teste de Menu")
    root.geometry("300x200")
    
    # Instancia o menu com funções de exemplo (mocks)
    menu_app = Menu(
        root,
        restart_command=lambda: mock_action("Novo"),
        open_command=lambda: mock_action("Abrir"),
        save_as_command=lambda: mock_action("Salvar Como"),
        load_graphic=lambda:mock_action("Gerar Gráfico"),
        about_us=lambda:mock_action('Sobre')
    )
    
    tk.Label(root, text="Menu configurado no modo de teste.").pack(pady=20)
    
    root.mainloop()