import tkinter as tk

class Button(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.grid(row=0,column=0,sticky='nsew')
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)

        """ Grid, método para inserir objeto por coluna e linha na aplicação"""
        for r in range(4):
            tk.Button(self,text="R%s"%(r),bg='yellow',command=self.ao_clicar).grid(row=r,
                                                            padx=3,pady=2)
            
    def ao_clicar(self):
        pass
        

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Teste de Formulário")
    root.minsize(300,200)
    main_button = Button(root)
    root.mainloop()    



