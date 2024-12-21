#gui image
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
            # Ensure proper path resolution
            script_path = os.path.abspath(script_name)
            if os.path.exists(script_path):
                root.destroy()  # Close current window
                subprocess.Popen(['python', script_path], cwd=os.path.dirname(script_path))
            else:
                print(f"{script_path} does not exist.")
    except Exception as e:
        print(f"Failed to open {script_name}. Error: {str(e)}")

# Main window setup
root = Tk()
root.title("Hide in Image Tools")

# Set window properties
window_width = 700
window_height = 800
center_window(root, window_width, window_height)
root.configure(bg="#EAF7FA")  # Light cyan background

# Title Label
title = ttk.Label(
    root,
    text="Hide in Image Tools",
    font=("Helvetica", 26, "bold"),
    background="#EAF7FA",
    foreground="#007BB5"
)
title.pack(pady=(20, 10))

# Subheading
subheading = ttk.Label(
    root,
    text="Choose a tool to hide data:",
    font=("Helvetica", 18),
    background="#EAF7FA",
    foreground="#555"
)
subheading.pack(pady=(0, 20))

# Frame to contain buttons
button_frame = Frame(root, bg="#EAF7FA")
button_frame.pack(pady=20)

# Button styles
style = ttk.Style()
style.configure(
    "RoundedButton.TButton",
    font=("Helvetica", 14),
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

# Categories with their tools
categories = [
    ("Image With LSB", "image_LSB.py"),
    ("Image With Comment Section", "image_comment_section.py"),
    ("SteganographyX Plus", "Tools/Images_apps/SteganographyX Plus/StgP.exe"),
    ("Xiao Stenography", "Tools/Images_apps/Xiao Stenography.lnk"),
    ("Hex Editor Neo", "Tools/Images_apps/Hex Editor Neo.lnk"),
]

# Create buttons for each tool
for i, (label, script) in enumerate(categories):
    button = ttk.Button(button_frame, text=label, command=lambda script=script: open_tool(script), style="RoundedButton.TButton")
    button.grid(row=i, column=0, pady=10, padx=20, sticky="ew")

# Corrected Back Button functionality
back_button = ttk.Button(
    root,
    text="Back",
    command=lambda: open_tool("GUI.py"),
    style="RoundedButton.TButton"
)
back_button.pack(pady=20)

# Run the main loop
root.mainloop()
