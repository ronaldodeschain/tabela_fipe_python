import tkinter as tk

fonte = 'Arial 12'

n_window = tk.Tk()
n_window.title('logado')
n_window.minsize(300,200)
n_window.maxsize(300,200)

label = tk.Label(n_window,text='Tamo logado fi',font=fonte)
label.pack()


radio = tk.Radiobutton(n_window,text='Gerente',font=fonte)
radio.pack()
radio2 = tk.Radiobutton(n_window,text='Funcionário',font=fonte)
radio2.pack()

n_window.mainloop()

