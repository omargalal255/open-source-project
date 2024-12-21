import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import subprocess


def center_window(width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

root = Tk()
root.title("Steghide Tool")
root.config()
window_width = 850
window_height = 500
center_window(window_width, window_height)

# Function for hiding message in image using Steghide
def steghide_hide(message, password, carrier, outimg):
    subprocess.Popen([
        "steghide", "embed", "-cf", carrier, "-ef", message, "-p", password, "-out", outimg
    ])

# Function for extracting message from image using Steghide
def steghide_extract(password, stegoimg):
    message = subprocess.getoutput([
        "steghide", "extract", "-sf", stegoimg, "-p", password, "-out", "output.txt"
    ])
    with open("output.txt", "r") as file:
        extracted_message = file.read()
    extract.insert(0, extracted_message)

title = ttk.Label(root, text="Steghide Tool GUI", font="Ubuntu 20 bold")
title.grid(row=0, column=0, columnspan=6, padx=20, pady=10)

title = ttk.Label(root, text="Steghide Hide", font="Ubuntu 20 bold")
title.grid(row=1, column=0, columnspan=6, padx=10, pady=10)

# Message to hide
message_label = ttk.Label(root, text="Enter message to hide")
message_label.grid(row=2, column=1, padx=10, pady=10)

message = ttk.Entry(root, width=50)
message.grid(row=2, column=2)

# Password
pass_label = ttk.Label(root, text="Enter password")
pass_label.grid(row=2, column=3, padx=10, pady=10)

password = ttk.Entry(root, width=20)
password.grid(row=2, column=4)

# Name of output image
out_img_name_label = ttk.Label(root, text="Enter the stego image name")
out_img_name_label.grid(row=3, column=1, padx=10, pady=10)

out_img_name = ttk.Entry(root, width=50)
out_img_name.grid(row=3, column=2, padx=10, pady=10)

# Carrier image path
path_carrier_img_label = ttk.Label(root, text="Path of the carrier image")
path_carrier_img_label.grid(row=4, column=1, padx=10, pady=10)

path_carrier_img = ttk.Entry(root, width=50)
path_carrier_img.grid(row=4, column=2, padx=10, pady=10)

# Select button for carrier image
def upload_img():
    name = filedialog.askopenfilename(title="Select the carrier image")
    path_carrier_img.insert(0, name)

btn_select = ttk.Button(root, text="Upload", command=upload_img)
btn_select.grid(row=5, column=1, padx=10, pady=10)

# Clear form function
def clear_form():
    message.delete(0, "end")
    password.delete(0, "end")
    out_img_name.delete(0, "end")
    path_carrier_img.delete(0, "end")
    stego_img_path.delete(0, "end")
    extract.delete(0, "end")

btn_clear = ttk.Button(root, text="Clear", command=clear_form)
btn_clear.grid(row=5, column=2, padx=10, pady=10)

# Hide message function
def hidebutton():
    carrier_img = path_carrier_img.get()
    passw = password.get()
    hidden_message = message.get()
    name_stego_img = out_img_name.get()

    if carrier_img == "" or passw == "" or hidden_message == "" or name_stego_img == "":
        messagebox.showerror("Error", "Please fill all the fields")
    else:
        steghide_hide(hidden_message, passw, carrier_img, name_stego_img)

btn_hide = ttk.Button(root, text="Hide", command=hidebutton)
btn_hide.grid(row=5, column=3, padx=10, pady=10)

title = ttk.Label(root, text="Steghide Extract", font="Ubuntu 20 bold")
title.grid(row=6, column=0, columnspan=6, padx=10, pady=10)

# Extract button
extract_label = ttk.Label(root, text="The hidden data")
extract_label.grid(row=7, column=1, padx=10, pady=10)

extract = ttk.Entry(root, width=50)
extract.grid(row=7, column=2, padx=10, pady=10)

def extract_hidden_message():
    path = stego_img_path.get()
    passw = password.get()

    if path == "" or passw == "":
        messagebox.showerror("Error", "Enter the password and select the path of stego file")
    else:
        steghide_extract(passw, path)

btn_extract = ttk.Button(root, text="Extract", command=extract_hidden_message)
btn_extract.grid(row=7, column=3, padx=10, pady=10)

# Select button for stego image
def upload_stego_img():
    name = filedialog.askopenfilename(title="Select stego image path")
    stego_img_path.insert(0, name)

btn_upload = ttk.Button(root, text="Upload", command=upload_stego_img)
btn_upload.grid(row=8, column=3, padx=10, pady=10)

stego_img_label = ttk.Label(root, text="Stego image path")
stego_img_label.grid(row=8, column=1)

stego_img_path = ttk.Entry(root, width=50)
stego_img_path.grid(row=8, column=2)

# Back button
def Back():
    root.destroy()
    subprocess.Popen(['python', "Audio.py"], cwd=os.path.dirname(os.path.abspath(__file__)))

btn_back = ttk.Button(root, text="Back", command=Back)
btn_back.grid(row=9, column=1, padx=10, pady=15)

root.mainloop()
