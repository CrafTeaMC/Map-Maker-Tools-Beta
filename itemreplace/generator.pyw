import tkinter as tk
from tkinter import filedialog, messagebox
import os
import winsound

def generate_mcfunction():
    window = tk.Tk()
    window.title("Item Replace")  # Set the title of the window

    # Set window size and position
    window_width = 300  # Change this to your desired width
    window_height = 400  # Change this to your desired height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    frame = tk.Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    def add_separator(row):
        separator_height = 2  # Change this to your desired separator height
        separator = tk.Frame(frame, height=separator_height, bd=1, relief=tk.SUNKEN, bg='blue')
        separator.grid(row=row, column=0, columnspan=2, sticky='we', pady=5, padx=5)

    tk.Label(frame, text="Player Tag (Optional):").grid(row=0, column=0, sticky='w')
    player_tag_entry = tk.Entry(frame)
    player_tag_entry.grid(row=1, column=0, sticky='ew')

    add_separator(2)

    tk.Label(frame, text="Test Item ID:").grid(row=3, column=0, sticky='w')
    test_item_id_entry = tk.Entry(frame)
    test_item_id_entry.grid(row=4, column=0, sticky='ew')

    tk.Label(frame, text="Test Item Count (Optional):").grid(row=5, column=0, sticky='w')
    test_item_count_entry = tk.Entry(frame)
    test_item_count_entry.grid(row=6, column=0, sticky='ew')

    tk.Label(frame, text="Test Item NBT (Optional):").grid(row=7, column=0, sticky='w')
    test_item_nbt_entry = tk.Entry(frame)
    test_item_nbt_entry.grid(row=8, column=0, sticky='ew')

    add_separator(9)

    tk.Label(frame, text="Replace Item ID:").grid(row=10, column=0, sticky='w')
    replace_item_id_entry = tk.Entry(frame)
    replace_item_id_entry.grid(row=11, column=0, sticky='ew')

    tk.Label(frame, text="Replace Item Count (Optional):").grid(row=12, column=0, sticky='w')
    replace_item_count_entry = tk.Entry(frame)
    replace_item_count_entry.grid(row=13, column=0, sticky='ew')

    tk.Label(frame, text="Replace Item NBT (Optional):").grid(row=14, column=0, sticky='w')
    replace_item_nbt_entry = tk.Entry(frame)
    replace_item_nbt_entry.grid(row=15, column=0, sticky='ew')

    add_separator(16)

    tk.Label(frame, text="File Name:").grid(row=17, column=0, sticky='w')
    file_name_entry = tk.Entry(frame)
    file_name_entry.grid(row=18, column=0, sticky='ew')

    add_separator(19)

    def on_generate():
        player_tag = player_tag_entry.get()
        test_item_id = test_item_id_entry.get()
        test_item_count = f'Count:{test_item_count_entry.get()}b,' if test_item_count_entry.get() else ""
        test_item_nbt = test_item_nbt_entry.get()
        replace_item_id = replace_item_id_entry.get()
        replace_item_count = replace_item_count_entry.get() if replace_item_count_entry.get() else "1"
        replace_item_nbt = replace_item_nbt_entry.get()
        file_name = file_name_entry.get()

        if not test_item_id or not replace_item_id or not file_name:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        slots = [f'container.{i}' for i in range(0, 36)] + ['armor.chest:102', 'armor.feet:100', 'armor.head:103', 'armor.legs:101', 'weapon.offhand:-106']
        commands = []

        for slot in slots:
            if 'container' in slot:
                slot_number = slot.split('.')[1]
                command = f'execute as @a[tag={player_tag},nbt={{Inventory:[{{id:"minecraft:{test_item_id}",{test_item_count}Slot:{slot_number}b,tag:{{{test_item_nbt}}}}}]}}] at @s run item replace entity @s {slot.split(":")[0]} with minecraft:{replace_item_id}{{{replace_item_nbt}}} {replace_item_count}'
            else:
                slot_number = slot.split(':')[1]
                command = f'execute as @a[tag={player_tag},nbt={{Inventory:[{{id:"minecraft:{test_item_id}",{test_item_count}Slot:{slot_number}b,tag:{{{test_item_nbt}}}}}]}}] at @s run item replace entity @s {slot.split(":")[0]} with minecraft:{replace_item_id}{{{replace_item_nbt}}} {replace_item_count}'
            commands.append(command)

        mcfunction_content = '\n'.join(commands)

        file_path = filedialog.asksaveasfilename(defaultextension=".mcfunction", initialfile=file_name)
        with open(file_path, 'w') as f:
            f.write(mcfunction_content)

        print(f"mcfunction file saved at {file_path}.")
        winsound.PlaySound('sounds/generate_sound.wav', winsound.SND_FILENAME)

    tk.Button(frame, text="Generate", command=on_generate).grid(row=20, column=0, columnspan=2)

    window.mainloop()

generate_mcfunction()
