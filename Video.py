from tkinter import *
from tkinter import ttk
import subprocess
import os
import win32com.client
from tkinter import messagebox


def center_window(root, width, height):
    """Centers the window on the screen."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')


def open_tool(script_name):
    """Opens the specified tool (script, executable, or shortcut)."""
    try:
        if script_name.endswith('.exe'):
            # Open executable files
            subprocess.Popen([script_name], cwd=os.path.dirname(os.path.abspath(__file__)), shell=True)
        elif script_name.endswith('.lnk'):
            # Resolve the .lnk file's target and open it
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
            # Assume it's a Python script
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
root.title("Hide in Video Tools")

# Window properties
window_width = 900
window_height = 600
center_window(root, window_width, window_height)

root.configure(bg="#EAF7FA")  # Background color

# Title label
title = ttk.Label(
    root,
    text="Hide in Video Tools",
    font=("Ubuntu", 24, "bold"),
    foreground="black",
    background="#EAF7FA"
)
title.grid(row=0, column=0, columnspan=3, pady=(20, 10), sticky="n")

# Subheading
subheading = ttk.Label(
    root,
    text="Choose a tool to hide data:",
    font=("Ubuntu", 14),
    background="#EAF7FA"
)
subheading.grid(row=1, column=0, columnspan=3, pady=(0, 20), sticky="n")

# Button styles
style = ttk.Style()
style.configure(
    "TButton",
    font=("Ubuntu", 12),
    padding=15,
    foreground="black",
    background="#00BCD4",
    relief="flat"
)

# Button hover effect
style.map(
    "TButton",
    background=[("active", "#0056b3")],
    foreground=[("active", "white")]
)

# Categories with their corresponding scripts
categories = [
    ("Video Stego Using AES", "video2.py"),
    ("DeEgger Tool", "Tools/video_apps/DeEgger Embedder.lnk"),
    ("Back", "GUI.py"),
]

# Create buttons
for i, (label, script) in enumerate(categories):
    button = ttk.Button(
        root,
        text=label,
        command=lambda script=script: open_tool(script),
        style="TButton"
    )
    button.grid(row=i + 2, column=1, pady=10, padx=20, sticky="ew")

# Make the layout consistent
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()
>>>>>>> video
