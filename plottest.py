import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
"""
from matplotlib.figure import Figure
exemplo do stackover - 
https://stackoverflow.com/questions/67280510/how-to-display-matplotlib-charts-
in-tkinter
"""


df1 = pd.DataFrame({
    'year': [2001, 2002, 2003],
    'value': [1, 3, 2],
    'personal': [9, 1, 5],
})

df2 = pd.DataFrame({
    'year': [2001, 2002, 2003],
    'value': [1, 3, 2],
    'personal': [9, 1, 5],
})

# --- 

root = tk.Tk()
root.minsize(800,700)

# resize grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# --- 

figure1 = plt.Figure(figsize=(2,2), dpi=100) #type:ignore

scatter1 = FigureCanvasTkAgg(figure1, root)
scatter1.get_tk_widget().grid(row=0, column=0, sticky='news')
#scatter1.get_tk_widget().pack(fill='both', expand=True)

ax1 = figure1.add_subplot(111)
ax1.plot(df1['year'], df1['personal'], color='red')

ax1.legend([''])
ax1.set_xlabel('valeur de personals')
ax1.set_title('ev de personal ')

# --- 

figure2 = plt.Figure(figsize=(2,2), dpi=100) #type:ignore

scatter2 = FigureCanvasTkAgg(figure2, root)
scatter2.get_tk_widget().grid(row=0, column=1, sticky='news')
#scatter2.get_tk_widget().pack(side='right', fill='both', expand=True)

ax2 = figure2.add_subplot(111)
ax2.plot(df2['year'], df2['value'], color='red')

ax2.legend([''])
ax2.set_xlabel('valeur BSA')
ax2.set_title('Evolutiion des valeurs BSA depuis 1990 ')

# --- 

figure3 = plt.Figure(figsize=(2,2), dpi=100) #type:ignore

scatter3 = FigureCanvasTkAgg(figure3, root)
scatter3.get_tk_widget().grid(row=1, column=0, sticky='news')
#scatter3.get_tk_widget().pack(fill='both', expand=True)

ax3 = figure3.add_subplot(111)
ax3.plot(df1['year'], df1['personal'], color='red')

ax3.legend([''])
ax3.set_xlabel('valeur de personals')
ax3.set_title('ev de personal ')

# --- 

figure4 = plt.Figure(figsize=(2,2), dpi=100) #type:ignore

scatter4 = FigureCanvasTkAgg(figure4, root)
scatter4.get_tk_widget().grid(row=1, column=1, sticky='news')
#scatter4.get_tk_widget().pack(fill='both', expand=True)

ax4 = figure4.add_subplot(111)
ax4.plot(df2['year'], df2['value'], color='red')

ax4.legend([''])
ax4.set_xlabel('valeur BSA')
ax4.set_title('Evolutiion des valeurs BSA depuis 1990 ')

# ---

root.mainloop()