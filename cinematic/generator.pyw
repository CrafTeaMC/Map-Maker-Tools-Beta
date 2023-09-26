import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import winsound
import json

root = tk.Tk()
root.title("Minecraft Cinematic Generator")

SOUNDS_DIR = "sounds"

position_entries = []
duration_entries = []

def lerp(a, b, t):
    return a + (b - a) * t

def generate_mcfunctions(datapack_name, folder_name, positions, durations, player_tag, game_mode, start_game_mode):
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return
    folder_path = os.path.join(folder_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    with open(os.path.join(folder_path, 'start.mcfunction'), 'w') as f:
        f.write(f'schedule function {datapack_name}:{folder_name}/tick_0 1t\n')
        f.write(f'gamemode {start_game_mode} @a[tag={player_tag}]\n')
    tick = 0
    for i in range(len(positions) - 1):
        duration = durations[i]
        for t in range(duration * 20):
            pos_t = t / (duration * 20)
            x = lerp(positions[i][0], positions[i + 1][0], pos_t)
            y = lerp(positions[i][1], positions[i + 1][1], pos_t)
            z = lerp(positions[i][2], positions[i + 1][2], pos_t)
            yaw = lerp(positions[i][3], positions[i + 1][3], pos_t)
            pitch = lerp(positions[i][4], positions[i + 1][4], pos_t)
            with open(os.path.join(folder_path, f'tick_{tick}.mcfunction'), 'w') as f:
                f.write(f'execute as @a[tag={player_tag}] at @s run tp @s {x} {y} {z} {yaw} {pitch}\n')
                if tick < sum(durations) * 20 - 1:
                    f.write(f'schedule function {datapack_name}:{folder_name}/tick_{tick+1} 1t\n')
                else:
                    f.write(f'tag @a[tag={player_tag}] remove {player_tag}\n')
                    f.write(f'gamemode {game_mode} @a[tag={player_tag}]\n')
            tick += 1
    print(f'mcfunctions generated for duration: {sum(durations)}s')
    sound_file = os.path.join(SOUNDS_DIR, "generate_sound.wav")
    if os.path.exists(sound_file):
        winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)

def on_submit():
    datapack_name = datapack_name_entry.get()
    if not datapack_name:
        messagebox.showerror("Error", "Please enter the name of your datapack")
        return
    
    folder_name = folder_name_entry.get()
    if not folder_name:
        messagebox.showerror("Error", "Please enter the name of the folder to save the mcfunctions")
        return
    
    player_tag = player_tag_entry.get()
    
    game_mode = game_mode_var.get()
    start_game_mode = start_game_mode_var.get()
    
    positions = []
    for entry in position_entries:
        position_str = entry[1].get()
        if not position_str:
            messagebox.showerror("Error", "Please enter all position and rotation values")
            return
        try:
            position = [float(x) for x in position_str.split()]
            if len(position) != 5:
                raise ValueError
            positions.append(position)
        except ValueError:
            messagebox.showerror("Error", "Invalid position or rotation value")
            return
    
    durations = []
    for entry in duration_entries:
        duration_str = entry.get()
        if not duration_str:
            messagebox.showerror("Error", "Please enter all durations")
            return
        try:
            duration = int(duration_str)
            durations.append(duration)
        except ValueError:
            messagebox.showerror("Error", "Invalid duration value")
            return
    
    generate_mcfunctions(datapack_name, folder_name, positions, durations, player_tag, game_mode, start_game_mode)

def on_add_position():
    position_frame = tk.Frame(root)
    
    position_label = tk.Label(position_frame, text=f"Enter position and rotation {len(position_entries)+1} (x y z yaw pitch):")
    position_label.pack(side="top")
    
    position_entry_frame = tk.Frame(position_frame)
    
    position_entry = tk.Entry(position_entry_frame)
    
    position_entry.pack(side="left")
    
    position_entry_frame.pack(side="top")
    
    position_entries.append((position_frame, position_entry))
    
    if len(position_entries) > 2:
        remove_position_button.config(state="normal")

    duration_frame = tk.Frame(root)
        
    duration_label = tk.Label(duration_frame, text=f"Enter duration from position {len(duration_entries)+1} to position {len(duration_entries)+2}:")
    duration_label.pack(side="top")

    duration_entry = tk.Entry(duration_frame)

    def validate_duration_input(char):
        return char.isdigit()

    validate_duration_command = root.register(validate_duration_input)

    duration_entry.config(validate="key", validatecommand=(validate_duration_command, '%S'))

    duration_entry.pack(side="top")

    duration_entries.append(duration_entry)

    duration_frame.pack(before=add_position_button)

    position_frame.pack(before=add_position_button)

def on_remove_position():
    if len(position_entries) > 2:
        position_entries[-1][0].destroy()
        del position_entries[-1]
        
        duration_entries[-1].master.destroy()
        del duration_entries[-1]
        
        if len(position_entries) == 2:
            remove_position_button.config(state="disabled")

datapack_name_label = tk.Label(root, text="Enter the name of your datapack:")
datapack_name_label.pack()
datapack_name_entry = tk.Entry(root)
datapack_name_entry.pack()

separator1 = tk.Frame(root, height=2, bd=1, relief="sunken")
separator1.pack(fill="x", padx=5, pady=5)

folder_name_label = tk.Label(root, text="Enter the name of the folder to save the mcfunctions:")
folder_name_label.pack()
folder_name_entry = tk.Entry(root)
folder_name_entry.pack()

separator2 = tk.Frame(root, height=2, bd=1, relief="sunken")
separator2.pack(fill="x", padx=5, pady=5)

player_tag_label = tk.Label(root, text="Enter player tag (Optional):")
player_tag_label.pack()
player_tag_entry = tk.Entry(root)
player_tag_entry.pack()

separator3 = tk.Frame(root, height=2, bd=1, relief="sunken")
separator3.pack(fill="x", padx=5, pady=5)

game_mode_var = tk.StringVar(root)
game_mode_var.set("adventure") # default value

game_mode_label = tk.Label(root, text="Which game mode should the player be in when the cinematic ends?")
game_mode_label.pack()
game_mode_option_menu = tk.OptionMenu(root, game_mode_var, "spectator", "adventure", "creative", "survival")
game_mode_option_menu.pack()

start_game_mode_var = tk.StringVar(root)
start_game_mode_var.set("spectator") # default value

start_game_mode_label = tk.Label(root, text="Which game mode should the player be in when the cinematic starts?")
start_game_mode_label.pack()
start_game_mode_option_menu = tk.OptionMenu(root, start_game_mode_var, "spectator", "adventure", "creative", "survival")
start_game_mode_option_menu.pack()

separator4 = tk.Frame(root, height=2, bd=1, relief="sunken")
separator4.pack(fill="x", padx=5, pady=5)

for i in range(2):
    position_frame = tk.Frame(root)
    
    position_label = tk.Label(position_frame, text=f"Enter position and rotation {i+1} (x y z yaw pitch):")
    position_label.pack(side="top")
    
    position_entry_frame = tk.Frame(position_frame)
    
    position_entry = tk.Entry(position_entry_frame)
    
    position_entry.pack(side="left")
    
    position_entry_frame.pack(side="top")
    
    position_entries.append((position_frame, position_entry))
    
    if i > 0:
        duration_frame = tk.Frame(root)
        
        duration_label = tk.Label(duration_frame, text=f"Enter duration from position {i} to position {i+1}:")
        duration_label.pack(side="top")
        
        duration_entry = tk.Entry(duration_frame)

        def validate_duration_input(char):
            return char.isdigit()

        validate_duration_command = root.register(validate_duration_input)

        duration_entry.config(validate="key", validatecommand=(validate_duration_command, '%S'))

        duration_entry.pack(side="top")
        
        duration_entries.append(duration_entry)
        
        duration_frame.pack()
    
    position_frame.pack()

add_position_button = tk.Button(root, text="Add Position", command=on_add_position)
add_position_button.pack()

remove_position_button = tk.Button(root, text="Remove Position", command=on_remove_position)
remove_position_button.pack()
remove_position_button.config(state="disabled")

submit_button = tk.Button(root, text="Generate", command=on_submit)
submit_button.pack()

root.mainloop()
