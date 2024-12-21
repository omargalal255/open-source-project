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
window_width = 900
window_height = 530
center_window(window_width, window_height)

def mp3stego(message,password,carrier,outfilename):
    subprocess.Popen(["Tools/hide in audio/MP3Stego_1_1_19/MP3Stego/Encode.exe"
                      ,"-E"
                      ,message
                      ,"-P"
                      ,password
                      ,carrier
                      ,outfilename
                      ])
    messagebox.showinfo("Success","Message embedded successfully")
        
def mp3stego_extract(password, carrier):
    try:
        # Run the Decode.exe command in the correct working directory
        result = subprocess.run(
            [
                "Tools/hide in audio/MP3Stego_1_1_19/MP3Stego/Decode.exe",
                "-X",  # Extract flag
                "-P", password,
                carrier
            ],
            cwd="Tools/hide in audio/MP3Stego_1_1_19/MP3Stego",  # Set the working directory
            capture_output=True,  # Capture the output for debugging
            text=True  # Get output as string
        )

        # Check for errors in the process
        if result.returncode != 0:
            messagebox.showerror("Error", f"Extraction failed: {result.stderr}")
        else:
            # Confirm success
            messagebox.showinfo("Success", "Hidden message extracted successfully.")
            print(result.stdout)  # Optional: Log output for debugging

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

        
        

title= ttk.Label(root , text="MP3Stego tool hiding file inside mp3 file",font="Ubuntu 20 bold")
title.grid(row=0 ,column=0, columnspan=6 ,padx=20 ,pady=10)


title= ttk.Label(root , text="Mp3Stego hide",font="Ubuntu 20 bold")
title.grid(row=1 ,column=0, columnspan=6 ,padx=10 ,pady=10)

#password
pass_label = ttk.Label(root,text="Enter password")  
pass_label.grid(row=3 , column=3,padx=10, pady=10)

password = ttk.Entry(root,width=20)
password.grid(row=3 ,column=4) 


path_carrier_img_label= ttk.Label(root ,text = "path of the carrier file")
path_carrier_img_label.grid(row=3 , column=1 ,padx=10 ,pady=10)
    
path_carrier_img = ttk.Entry(root,width=50)
path_carrier_img.grid(row=3, column=2,padx=10,pady=10)



path_secret_message_label= ttk.Label(root ,text = "path of the secret mesaage")
path_secret_message_label.grid(row=4 , column=1 ,padx=10 ,pady=10)
    
path_secret_mesaage = ttk.Entry(root,width=50)
path_secret_mesaage.grid(row=4, column=2,padx=10,pady=10)
    
    
name_stego_file_label= ttk.Label(root ,text = "output file name")
name_stego_file_label.grid(row=6 , column=1 ,padx=10 ,pady=10)
    
name_stego_file = ttk.Entry(root,width=50)
name_stego_file.grid(row=6, column=2,padx=10,pady=10)
    
    
    
#select button carrier
def upload_carrier_file():
    name = filedialog.askopenfilename(title="select the carrie image")
    path_carrier_img.insert(0,name)

btn_select = ttk.Button(root, text="upload carrier",command = upload_carrier_file) 
btn_select.grid(row=7 , column=1 ,padx=10 ,pady=10 )


#uplaod secret message

def upload_secret_message():
    name = filedialog.askopenfilename(title="select the carrie image")
    path_secret_mesaage.insert(0,name)

btn_select = ttk.Button(root, text="upload sccret message",command = upload_secret_message) 
btn_select.grid(row=4 , column=3 ,padx=10 ,pady=10 )

#clear button

def clear_form():
    path_carrier_img.delete(0, 'end')
    password.delete(0, 'end')
    path_secret_mesaage.delete(0,'end')
    stego_file_path.delete(0,'end')
    extract.delete(0,'end')
    name_stego_file.delete(0,'end')
    
    
btn_select = ttk.Button(root, text="clear",command = clear_form) 
btn_select.grid(row=7, column=2 ,padx=10 ,pady=10 )


#hide button
def hidebutton():
    carrier_file = path_carrier_img.get()
    secret_message = path_secret_mesaage.get() 
    passw= password.get()
    output_file_name = name_stego_file.get()

    if carrier_file == '' or secret_message == '' or passw == '' or output_file_name == '' :
        messagebox.showerror("Error", "Please fill all the fields")
    else:
        mp3stego(secret_message,passw,carrier_file,output_file_name)

btn_hide = ttk.Button(root, text="hide",command = hidebutton) 
btn_hide.grid(row=7 , column=3 ,padx=10 ,pady=10 )

title= ttk.Label(root , text="mp3stego extract",font="Ubuntu 20 bold")
title.grid(row=8 ,column=0, columnspan=6 ,padx=10 ,pady=10)

#btn extract 


extract_label= ttk.Label(root, text="the hidden file name")
extract_label.grid(row=9 ,column=1 , padx=10 ,pady=10)

extract=  ttk.Entry(root, width=50)
extract.grid(row=9 ,column=2 ,padx=10,pady=10)


def extract_hidden_message():
     passw= password.get()
     path = stego_file_path.get()
     
     if path == '' or passw == '' :
        messagebox.showerror("Error", "Enter the password and select the path of stego file")
     else:
        mp3stego_extract(passw,path)


btn_extract = ttk.Button(root, text="extract", command=extract_hidden_message)
btn_extract.grid(row=9 , column=3 ,padx=10 ,pady=10)


def upload_stego_img():
    name = filedialog.askopenfilename(title="select file with secret message")
    stego_file_path.insert(0, name)
    
     
btn_upload = ttk.Button(root, text="upload",command=upload_stego_img)
btn_upload.grid(row=10 , column=3 ,padx=10 ,pady=10)

stego_img_label =  ttk.Label(root, text="select stego file")
stego_img_label.grid(row=10,column=1)

stego_file_path = ttk.Entry(root,width=50)
stego_file_path.grid(row=10 ,column=2) 


def Back():
    root.destroy()
    subprocess.Popen(['python', "Audio.py"], cwd=os.path.dirname(os.path.abspath(__file__)))

btn_back=ttk.Button(root,text="back",command=Back )
btn_back.grid(row=11,column=1,padx=10,pady=20)


root.mainloop()
