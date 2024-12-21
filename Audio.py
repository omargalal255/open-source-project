from tkinter import *
from tkinter import ttk, messagebox
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
    """Open the specified script, executable, or shortcut file."""
    try:
        if script_name.endswith('.exe'):
            subprocess.Popen([script_name], cwd=os.path.dirname(os.path.abspath(__file__)), shell=True)
        elif script_name.endswith('.lnk'):
            shortcut_path = os.path.abspath(script_name)
            if not os.path.exists(shortcut_path):
                raise FileNotFoundError(f"The shortcut '{shortcut_path}' does not exist.")

            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(shortcut_path)
            target_path = shortcut.TargetPath

            if os.path.exists(target_path):
                os.startfile(target_path)
            else:
                raise FileNotFoundError(f"The target '{target_path}' of the shortcut does not exist.")

        else:
            script_path = os.path.abspath(script_name)
            if not os.path.exists(script_path):
                raise FileNotFoundError(f"The script '{script_path}' does not exist.")

            root.destroy()
            subprocess.Popen(['python', script_path], cwd=os.path.dirname(os.path.abspath(__file__)))

    except FileNotFoundError as fnf_error:
        messagebox.showerror("File Not Found", str(fnf_error))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Main window setup
root = Tk()
root.title("Hide in Audio Tools")

# Set window properties
window_width = 900
window_height = 600
center_window(root, window_width, window_height)
root.configure(bg="#EAF7FA")

# Title Label
title_frame = Frame(root, bg="#EAF7FA")
title_frame.grid(row=0, column=0, columnspan=3, pady=20)

title = ttk.Label(
    title_frame,
    text="Hide in Audio Tools",
    font=("Ubuntu", 24, "bold"),
    background="#EAF7FA",
    foreground="#007BB5"
)
title.grid(row=0, column=0)

# Subheading
subheading_frame = Frame(root, bg="#EAF7FA")
subheading_frame.grid(row=1, column=0, columnspan=3, pady=(0, 40))

subheading = ttk.Label(
    subheading_frame,
    text="Choose a tool to hide data:",
    font=("Ubuntu", 14),
    background="#EAF7FA",
    foreground="#555"
)
subheading.grid(row=0, column=0)

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
    foreground=[("active", "white")]
)

# Frame for buttons
button_frame = Frame(root, bg="#EAF7FA")
button_frame.grid(row=2, column=0, columnspan=3, pady=20)

# Categories with their scripts
categories = [
    ("Mp3Stego Tool", "mp3stegano.py"),
    ("Steghide Tool", "steghide.py"),
]

# Create buttons for each tool, stacked vertically in the center
for i, (label, script) in enumerate(categories):
    button = ttk.Button(
        button_frame,
        text=label,
        command=lambda script=script: open_tool(script),
        style="RoundedButton.TButton"
    )
    button.grid(row=i, column=0, pady=10, padx=20, sticky="ew")

# Back Button
back_button_frame = Frame(root, bg="#EAF7FA")
back_button_frame.grid(row=3, column=0, columnspan=3, pady=20)

back_button = ttk.Button(
    back_button_frame,
    text="Back",
    command=lambda: open_tool("GUI.py"),
    style="RoundedButton.TButton"
)
back_button.grid(row=0, column=0, pady=10, padx=20, sticky="ew")

# Make the layout centered and expandable
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()

