import tkinter as tk
from tkinter import filedialog, messagebox
from playsound import playsound

def generate():
    try:
        x1, y1, z1 = map(int, coord1_entry.get().split())
        x2, y2, z2 = map(int, coord2_entry.get().split())
        block_id = block_id_entry.get()
        command = command_entry.get()
        filename = filename_entry.get()

        if not (block_id and command and filename):
            raise ValueError("All fields must be filled out.")

        with filedialog.asksaveasfile(defaultextension=".mcfunction", initialfile=filename, filetypes=[("Minecraft Function Files", "*.mcfunction")]) as f:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    for z in range(min(z1, z2), max(z1, z2) + 1):
                        f.write(f"execute if block {x} {y} {z} {block_id} run {command}\n")
        playsound('sounds/generate_sound.wav')
    except ValueError as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.geometry("300x300+300+300")  
root.title("Minecraft İf Block Generator")  

tk.Label(root, text="First Coordinate").pack()
coord1_entry = tk.Entry(root)
coord1_entry.pack()

tk.Label(root, text="Second Coordinate").pack()
coord2_entry = tk.Entry(root)
coord2_entry.pack()

tk.Label(root, text="Block ID").pack()
block_id_entry = tk.Entry(root)
block_id_entry.pack()

tk.Label(root, text="Command").pack()
command_entry = tk.Entry(root)
command_entry.pack()

tk.Label(root, text="Filename").pack()
filename_entry = tk.Entry(root)
filename_entry.pack()

generate_button = tk.Button(root, text="Generate", command=generate)
generate_button.pack()

root.mainloop()
