from tkinter import *
from tkinter import ttk
import subprocess
import os

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
        if script_name.endswith(".py"):  # Python script
            subprocess.Popen(['python', script_name], cwd=os.path.dirname(os.path.abspath(__file__)))
            root.destroy()

        elif script_name.endswith(".jar"):  # Java JAR file
            subprocess.Popen(['java', '-jar', script_name], cwd=os.path.dirname(os.path.abspath(__file__)))

        else:
            print(f"Unsupported file type for {script_name}")

    except FileNotFoundError:
        print(f"{script_name} not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Main window setup
root = Tk()
root.title("Hide in txt tools")

# Set window properties
window_width = 900
window_height = 600
center_window(root, window_width, window_height)

root.configure(bg="#EAF7FA")

# Title label with the first button style color
title = ttk.Label(
    root,
    text="Hide in TXT Tools",
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

# Frame to center the buttons
button_frame = Frame(root, bg="#EAF7FA")
button_frame.grid(row=2, column=0, columnspan=3, pady=20)

# Categories with their scripts
categories = [
    ("Snow", "snow.py"),
    ("Open Stego Tool", "Tools/hide in files/openstego-0.8.6/lib/openstego.jar"),
    ("Back", "GUI.py"),
]

# Create buttons for each category stacked vertically
for i, (label, script) in enumerate(categories):
    button = ttk.Button(
        button_frame,
        text=label,
        command=lambda script=script: open_tool(script),
        style="RoundedButton.TButton"
    )
    button.grid(row=i, column=0, pady=10, padx=20, sticky="ew")

# Make the layout expandable and consistent
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()
