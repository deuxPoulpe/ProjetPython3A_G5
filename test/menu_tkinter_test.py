import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk


def update_values():
    num_var1.set(int(scale_var1.get()))
    num_var2.set(int(scale_var2.get()))
    str_var1.set(entry_var1.get())
    str_var2.set(entry_var2.get())
    print("Variables mises à jour:")
    print(f"Numérique 1: {num_var1.get()}, Numérique 2: {num_var2.get()}")
    print(f"Texte 1: {str_var1.get()}, Texte 2: {str_var2.get()}")
    print(f"Booléen 1: {bool_var1.get()}, Booléen 2: {bool_var2.get()}")

def get_current_value(scale_var):
    return '{:.0f}'.format(scale_var.get())

root = ThemedTk(theme="breeze")
root.geometry('300x700')
root.resizable(True, True)
root.title('Menu de Paramétrage')

# Modifier la couleur de fond de la fenêtre principale
# root.configure(bg='#87CEFA')

# Changer la police pour un style pixel art
font_style = ("Pixel", 12)

# Variables
num_var1 = tk.IntVar()
num_var2 = tk.IntVar()
str_var1 = tk.StringVar()
str_var2 = tk.StringVar()
bool_var1 = tk.BooleanVar()
bool_var2 = tk.BooleanVar()

label_var1 = ttk.Label(root, text="Variable Numérique 1", font=font_style)
label_var1.pack(pady=(10, 0))
scale_var1 = ttk.Scale(root, from_=0, to=100, orient="horizontal", variable=num_var1)
scale_var1.pack(pady=5)
scale_var1_label = ttk.Label(root, text="", font=font_style)
scale_var1_label.pack()

label_var2 = ttk.Label(root, text="Variable Numérique 2", font=font_style)
label_var2.pack(pady=(10, 0))
scale_var2 = ttk.Scale(root, from_=0, to=100, orient="horizontal", variable=num_var2)
scale_var2.pack(pady=5)
scale_var2_label = ttk.Label(root, text="", font=font_style)
scale_var2_label.pack()

label_str1 = ttk.Label(root, text="Texte Variable 1", font=font_style)
label_str1.pack(pady=(10, 0))
entry_var1 = ttk.Entry(root, textvariable=str_var1)
entry_var1.pack(pady=5)

label_str2 = ttk.Label(root, text="Texte Variable 2", font=font_style)
label_str2.pack(pady=(10, 0))
entry_var2 = ttk.Entry(root, textvariable=str_var2)
entry_var2.pack(pady=5)

check_label1 = ttk.Label(root, text="Booléen Variable 1", font=font_style)
check_label1.pack(pady=(10, 0))
check_var1 = ttk.Checkbutton(root, text="Activer", variable=bool_var1)
check_var1.pack(pady=5)

check_label2 = ttk.Label(root, text="Booléen Variable 2", font=font_style)
check_label2.pack(pady=(10, 0))
check_var2 = ttk.Checkbutton(root, text="Activer", variable=bool_var2)
check_var2.pack(pady=5)

def get_current_value(scale_var):
    return '{:.0f}'.format(scale_var.get())

def update_slider1_label(event):
    scale_var1_label.config(text=get_current_value(scale_var1))

def update_slider2_label(event):
    scale_var2_label.config(text=get_current_value(scale_var2))

scale_var1.bind("<Motion>", update_slider1_label)
scale_var2.bind("<Motion>", update_slider2_label)

update_slider1_label(None)
update_slider2_label(None)

update_button = ttk.Button(root, text="Mettre à jour les variables", command=update_values)
update_button.pack(pady=10)


root.mainloop()
