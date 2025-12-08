import tkinter as tk

root = tk.Tk()
root.title('menu')
root.minsize(300,200)

main_menu = tk.Menu(root)

#File menu start here
file_menu = tk.Menu(main_menu,tearoff=0)

file_menu.add_command(label='new Text file')
file_menu.add_command(label='new file')
file_menu.add_command(label='new window')
file_menu.add_separator()
file_menu.add_command(label='open file')
file_menu.add_command(label='open folder')

#open recent dropdown starts here
openrecent = tk.Menu(main_menu)
openrecent.add_command(label='File 1 12/11/2023')
openrecent.add_command(label='File 2 12/11/2024')
openrecent.add_command(label='File 3 12/11/2025')
openrecent.add_command(label='File 4 12/11/2026')

file_menu.add_cascade(label='open recent',menu=openrecent)

file_menu.add_separator()

file_menu.add_command(label='Exit',command=root.quit)

main_menu.add_cascade(label='file',menu=file_menu)
#Edit menu starts here
edit_menu = tk.Menu(main_menu,tearoff=0)

edit_menu.add_command(label='Undo')
edit_menu.add_command(label='Redo')
edit_menu.add_separator()
edit_menu.add_command(label='Copy')
edit_menu.add_command(label='Cut')
edit_menu.add_command(label='Paste')
edit_menu.add_separator()
edit_menu.add_command(label='Find')
edit_menu.add_command(label='replace')

main_menu.add_cascade(label='edit',menu=edit_menu)
#view menu starts here
view_menu = tk.Menu(main_menu,tearoff=0)

view_menu.add_checkbutton(label='Terminal')
view_menu.add_checkbutton(label='Explorer')
view_menu.add_separator()
view_menu.add_radiobutton(label='Menu')
view_menu.add_radiobutton(label='Panel')
view_menu.add_radiobutton(label='Outuput')
view_menu.add_separator()
view_menu.add_command(label='problems')
view_menu.add_command(label='debug_console')

main_menu.add_cascade(label='view',menu=view_menu)
root.config(menu=main_menu)

root.mainloop()