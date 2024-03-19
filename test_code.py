import tkinter as tk
from tkinter import ttk

def on_select(event):
    selected_value = combo_box.get()
    label.config(text="Selected: " + selected_value)

# Create the main application window
root = tk.Tk()
root.title("ComboBox Example")

# Create a label for the command
command_label = tk.Label(root, text="Command:")
command_label.pack()

# Create a StringVar to store the selected value
command_var = tk.StringVar()
command_var.set("0000")

# Create a label
label = tk.Label(root, text="Selected: ")
label.pack()

# Create a Combobox
combo_box = ttk.Combobox(root, textvariable=command_var)
combo_box['values'] = ('Option 1', 'Option 2', 'Option 3', 'Option 4')
combo_box.pack()

# Bind the event handler to the ComboBox
combo_box.bind('<<ComboboxSelected>>', on_select)

root.mainloop()
