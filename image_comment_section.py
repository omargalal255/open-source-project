import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import piexif
import base64
import hashlib
from cryptography.fernet import Fernet
import subprocess
import os

# SimpleEncryptorDecryptor class to encrypt and decrypt messages
class SimpleEncryptorDecryptor:
    def _derive_key(self, password):
        return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

    def encrypt(self, message, password):
        key = self._derive_key(password)
        fernet = Fernet(key)
        return fernet.encrypt(message.encode()).decode()

    def decrypt(self, encrypted_message, password):
        key = self._derive_key(password)
        fernet = Fernet(key)
        try:
            return fernet.decrypt(encrypted_message.encode()).decode()
        except Exception as e:
            print(f"Decryption error: {e}")
            return None

# CommentSteganography class to hide and retrieve data in images
class CommentSteganography:
    def __init__(self, image_path):
        self.image_path = image_path
        self.crypto = SimpleEncryptorDecryptor()

    def hide_data(self, data_to_hide, output_path, password):
        try:
            img = Image.open(self.image_path)
            encrypted = self.crypto.encrypt(data_to_hide, password)

            img = img.convert('RGB')
            exif_dict = piexif.load(img.info['exif']) if 'exif' in img.info else {'0th': {}, 'Exif': {}, '1st': {}, 'thumbnail': None}
            exif_dict['0th'][piexif.ImageIFD.ImageDescription] = encrypted

            exif_bytes = piexif.dump(exif_dict)
            img.save(output_path, "jpeg", exif=exif_bytes)

            messagebox.showinfo("Success", f"Data hidden and saved to {output_path}")
        except Exception as e:
            print(f"Failed to hide data: {e}")
            messagebox.showerror("Error", f"Failed to hide data: {e}")

    def retrieve_data(self, stego_image_path, password):
        try:
            img = Image.open(stego_image_path)
            exif_dict = piexif.load(img.info['exif']) if 'exif' in img.info else {}
            comment_section = exif_dict.get('0th', {}).get(piexif.ImageIFD.ImageDescription, b'')
            encrypted_data = comment_section.decode('utf-8') if comment_section else ''

            if encrypted_data:
                data = self.crypto.decrypt(encrypted_data, password)
                return data
            return None
        except Exception as e:
            print(f"Failed to retrieve hidden data: {e}")
            return None

# GUI application class
class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography GUI")
        self.root.configure(bg="#EAF7FA")
        self.root.resizable(False, False)

        self.crypto = SimpleEncryptorDecryptor()

        self.init_gui()

    def init_gui(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(row=0, column=0)

        # Title Label
        title_label = ttk.Label(
            main_frame, text="Steganography Tools", font=("Helvetica", 26, "bold"),
            background="#EAF7FA", foreground="#007BB5"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        ttk.Label(main_frame, text="Enter Password:").grid(row=1, column=0, sticky=tk.E, padx=10)
        self.password_entry = ttk.Entry(main_frame, width=40, show="*")
        self.password_entry.grid(row=1, column=1, columnspan=2, padx=10)

        ttk.Label(main_frame, text="Enter Hidden Message:").grid(row=2, column=0, sticky=tk.E, padx=10)
        self.message_entry = ttk.Entry(main_frame, width=50)
        self.message_entry.grid(row=2, column=1, columnspan=2, padx=10)

        ttk.Label(main_frame, text="Selected Image Path:").grid(row=3, column=0, sticky=tk.E, padx=10)
        self.file_path_entry = ttk.Entry(main_frame, width=50)
        self.file_path_entry.grid(row=3, column=1, columnspan=2, padx=10)

        ttk.Button(main_frame, text="Select Image", command=self.select_image).grid(row=3, column=3, padx=10)
        ttk.Button(main_frame, text="Hide Data", command=self.hide_data, style="RoundedButton.TButton").grid(row=4, column=1, pady=10)
        ttk.Button(main_frame, text="Retrieve Data", command=self.retrieve_data, style="RoundedButton.TButton").grid(row=4, column=2, pady=10)

        # Back Button (for returning to main GUI or exiting the application)
        def Back():
            root.destroy()
            subprocess.Popen(['python', "images.py"], cwd=os.path.dirname(os.path.abspath(__file__)))

        center_frame = ttk.Frame(root)
        center_frame.grid(row=9, column=0, columnspan=3, padx=10, pady=15)

        btn_back = ttk.Button(center_frame, text="Back", command=Back)
        btn_back.pack(anchor="center")  # Center the button in the frame

        # Button Styles
        style = ttk.Style()
        style.configure(
            "RoundedButton.TButton",
            font=("Helvetica", 14),
            padding=15,
            background="#00BCD4",
            foreground="black",
            relief="flat"
        )
        style.map(
            "RoundedButton.TButton",
            background=[("active", "#00ACC1")],
            foreground=[("active", "black")]
        )

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)

    def hide_data(self):
        password = self.password_entry.get()
        message = self.message_entry.get()
        file_path = self.file_path_entry.get()

        if not password or not message or not file_path:
            messagebox.showerror("Error", "All fields are required!")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if save_path:
            stego = CommentSteganography(file_path)
            stego.hide_data(message, save_path, password)

    def retrieve_data(self):
        password = self.password_entry.get()
        file_path = self.file_path_entry.get()

        if not password or not file_path:
            messagebox.showerror("Error", "Password and Image Path are required!")
            return

        stego = CommentSteganography(file_path)
        hidden_message = stego.retrieve_data(file_path, password)

        if hidden_message:
            messagebox.showinfo("Hidden Data", f"Retrieved Message: {hidden_message}")
        else:
            messagebox.showerror("Error", "Failed to retrieve hidden data.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
