from tkinter import *
from tkinter import ttk
import subprocess
import os
import win32com.client

def center_window(root, width, height):
    """Centers the window on the screen."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

def open_tool(script_name):
    """Opens the specified script, executable, or shortcut file."""
    try:
        if script_name.endswith('.exe'):
            subprocess.Popen([script_name], cwd=os.path.dirname(os.path.abspath(__file__)), shell=True)
        elif script_name.endswith('.lnk'):
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(script_name)
            target_path = shortcut.TargetPath
            os.startfile(target_path)
        else:
            root.destroy()
            subprocess.Popen(['python', script_name], cwd=os.path.dirname(os.path.abspath(__file__)))
    except Exception as e:
        print(f"Failed to open {script_name}. Error: {str(e)}")

# Main window setup
root = Tk()
root.title("Steganography App")

# Set window properties (width: 800, height: 500)
window_width = 800
window_height = 600
center_window(root, window_width, window_height)
root.configure(bg="#EAF7FA")  # Light cyan background

# Title Label
title = ttk.Label(
    root,
    text="Steganography App",
    font=("Ubuntu", 24, "bold"),
    background="#EAF7FA",
    foreground="#007BB5"
)
title.grid(row=0, column=0, columnspan=3, pady=(20, 10), sticky="n")

# Subheading
subheading = ttk.Label(
    root,
    text="Choose a category to hide data:",
    font=("Ubuntu", 14),
    background="#EAF7FA",
    foreground="#555"
)
subheading.grid(row=1, column=0, columnspan=3, pady=(0, 20), sticky="n")

# Button styles
style = ttk.Style()
style.configure(
    "RoundedButton.TButton",
    font=("Ubuntu", 12),
    padding=15,
    foreground="black",
    background="#00BCD4",
    relief="flat"
)

style.map(
    "RoundedButton.TButton",
    background=[("active", "#00ACC1")],
    foreground=[("active", "black")]
)

# Categories with their scripts
categories = [
    ("Hide in Audio", "Audio.py"),
    ("Hide in Text", "Text.py"),
    ("Hide in Images", "images.py"),
    ("Hide in Video", "video.py")
]

# Create buttons for each category
for i, (label, script) in enumerate(categories):
    button = ttk.Button(
        root,
        text=label,
        command=lambda script=script: open_tool(script),
        style="RoundedButton.TButton"
    )
    button.grid(row=i + 2, column=1, pady=10, padx=20, sticky="ew")

# Back Button to return to main GUI
back_button = ttk.Button(
    root,
    text="Exit",
    command=lambda: open_tool("Main_GUI.py"),
    style="RoundedButton.TButton"
)
back_button.grid(row=len(categories) + 3, column=1, pady=20)

# Adjust row and column to maintain layout responsiveness
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Run main window loop
root.mainloop()
