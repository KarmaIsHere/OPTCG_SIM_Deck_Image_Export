import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import threading

from deck_tools import run_deck_builder

deck_var = None
folder_var = None
output_var = None
generate_button = None
progress_bar = None

def handle_run_deck_builder_result(success, result_message=None):
    progress_bar.stop()
    progress_bar.grid_forget()

    generate_button.config(state=tk.NORMAL)

    if success:
        messagebox.showinfo("Done", f"Deck image saved to:\n{result_message}")
    else:
        messagebox.showerror("Error", f"An error occurred:\n{result_message}")

def browse_folder():
    folder = filedialog.askdirectory(title="Select Output Folder")
    if folder:
        output_var.set(folder)

def browse_deck_file():
    deck_file_path = filedialog.askopenfilename(
        title="Select Deck File",
        filetypes=(("Sim deck files", "*.deck"), ("Text files", "*.txt"), ("All files", "*.*"))
    )
    if deck_file_path:
        deck_directory = os.path.dirname(deck_file_path)
        sim_folder_path = os.path.dirname(deck_directory)
        folder_var.set(sim_folder_path)
        deck_var.set(deck_file_path)
    else:
        folder_var.set("")
        deck_var.set("")

def start_generate_thread():
    sim_path = folder_var.get()
    deck_full_path = deck_var.get()
    output_path = output_var.get()

    if not deck_full_path:
        messagebox.showwarning("Missing Info", "Please select a deck file.")
        return
    if not output_path:
        messagebox.showwarning("Missing Info", "Please select an output folder.")
        return

    progress_bar.grid(row=4, column=0, columnspan=3, pady=10, padx=5, sticky="ew")
    progress_bar.start()

    generate_button.config(state=tk.DISABLED)

    thread = threading.Thread(
        target=run_deck_builder_threaded,
        args=(sim_path, deck_full_path, output_path)
    )
    thread.daemon = True
    thread.start()

def run_deck_builder_threaded(sim_path, deck_name, output_path):
    try:
        output = run_deck_builder(sim_path, deck_name, output_path)
        root.after(0, handle_run_deck_builder_result, True, output)
    except Exception as e:
        root.after(0, handle_run_deck_builder_result, False, str(e))

root = tk.Tk()
root.title("OPTCG Deck Collage Generator")

deck_var = tk.StringVar(root)
folder_var = tk.StringVar(root)
output_var = tk.StringVar(root)

tk.Label(root, text="Inferred Sim Folder:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
tk.Label(root, textvariable=folder_var, wraplength=400, justify='left').grid(row=0, column=1, columnspan=2, sticky='w', padx=5, pady=5)

tk.Label(root, text="Deck File:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
tk.Entry(root, textvariable=deck_var, width=50, state='readonly').grid(row=1, column=1, padx=5)
tk.Button(root, text="Browse", command=browse_deck_file).grid(row=1, column=2, padx=5)

tk.Label(root, text="Output Folder:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
tk.Entry(root, textvariable=output_var, width=50, state='readonly').grid(row=2, column=1, padx=5)
tk.Button(root, text="Browse", command=browse_folder).grid(row=2, column=2, padx=5)

generate_button = tk.Button(root, text="Generate Deck Image", command=start_generate_thread, bg="green", fg="white")
generate_button.grid(row=3, column=1, pady=15)

progress_bar = ttk.Progressbar(root, mode='indeterminate', length=300)

root.mainloop()