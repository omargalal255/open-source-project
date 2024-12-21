import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from cryptography.fernet import Fernet
import base64
import hashlib
import cv2
import numpy as np
import subprocess
import win32com.client

# Key generation utility class
class SimpleEncryptorDecryptor:
    def _derive_key(self, password):
        """
        Derive a 32-byte key from the password using SHA256 and encode it for Fernet.
        """
        return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

    def encrypt(self, message, password):
        """
        Encrypt a message using the derived key and Fernet encryption.
        """
        key = self._derive_key(password)
        fernet = Fernet(key)
        return fernet.encrypt(message.encode()).decode()

    def decrypt(self, encrypted_message, password):
        """
        Decrypt a message using the derived key and Fernet decryption.
        """
        key = self._derive_key(password)
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_message.encode()).decode()


# LSB Steganography Class
class LSBSteg:
    def __init__(self, im):
        self.image = im
        self.height, self.width, self.nbchannels = im.shape
        self.size = self.width * self.height

        self.maskONEValues = [1, 2, 4, 8, 16, 32, 64, 128]
        self.maskONE = self.maskONEValues.pop(0)

        self.maskZEROValues = [254, 253, 251, 247, 239, 223, 191, 127]
        self.maskZERO = self.maskZEROValues.pop(0)

        self.curwidth = 0
        self.curheight = 0
        self.curchan = 0

    def put_binary_value(self, bits):
        for c in bits:
            val = list(self.image[self.curheight, self.curwidth])

            if int(c) == 1:
                val[self.curchan] = int(val[self.curchan]) | self.maskONE
            else:
                val[self.curchan] = int(val[self.curchan]) & self.maskZERO

            self.image[self.curheight, self.curwidth] = tuple(val)
            self.next_slot()

    def next_slot(self):
        if self.curchan == self.nbchannels - 1:
            self.curchan = 0
            if self.curwidth == self.width - 1:
                self.curwidth = 0
                if self.curheight == self.height - 1:
                    self.curheight = 0
                    if self.maskONE == 128:
                        print("No available slot remaining (image filled)")
                    else:
                        self.maskONE = self.maskONEValues.pop(0)
                        self.maskZERO = self.maskZEROValues.pop(0)
                else:
                    self.curheight += 1
            else:
                self.curwidth += 1
        else:
            self.curchan += 1

    def encode_text(self, txt, password):
        encrypted_txt = SimpleEncryptorDecryptor().encrypt(txt, password)

        l = len(encrypted_txt)
        binl = f"{l:016b}"
        self.put_binary_value(binl)

        for char in encrypted_txt:
            c = ord(char)
            self.put_binary_value(f"{c:08b}")

        return self.image

    def decode_text(self, password):
        ls = self.read_bits(16)
        l = int(ls, 2)

        unhideTxt = ""
        for i in range(l):
            tmp = self.read_byte()
            unhideTxt += chr(int(tmp, 2))

        return SimpleEncryptorDecryptor().decrypt(unhideTxt, password)

    def read_bit(self):
        val = self.image[self.curheight, self.curwidth][self.curchan]
        val = int(val) & self.maskONE
        self.next_slot()

        if val > 0:
            return "1"
        else:
            return "0"

    def read_byte(self):
        return self.read_bits(8)

    def read_bits(self, nb):
        bits = ""
        for i in range(nb):
            bits += self.read_bit()
        return bits


# Main GUI Application
class GUIApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("LSB Steganography Tool")
        self.root.resizable(False, False)

        # Get the window dimensions
        window_width = 600
        window_height = 400

        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate position for centering the window
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)

        # Set window size and position
        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.encryptor_decryptor = SimpleEncryptorDecryptor()

        self.init_gui()

    def init_gui(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(row=0, column=0)

        ttk.Label(main_frame, text="Enter Password:").grid(row=0, column=0, padx=10, pady=5)
        self.password_entry = ttk.Entry(main_frame, width=40, show="*")
        self.password_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

        ttk.Label(main_frame, text="Message to Encode:").grid(row=1, column=0, padx=10, pady=5)
        self.message_entry = ttk.Entry(main_frame, width=50)
        self.message_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

        ttk.Label(main_frame, text="Select Image:").grid(row=2, column=0, padx=10, pady=5)
        self.file_entry = ttk.Entry(main_frame, width=50)
        self.file_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

        ttk.Button(main_frame, text="Browse", command=self.select_file).grid(row=2, column=3)

        ttk.Label(main_frame, text="Save Location:").grid(row=3, column=0, padx=10, pady=5)
        self.save_entry = ttk.Entry(main_frame, width=50)
        self.save_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=5)

        ttk.Button(main_frame, text="Encrypt", command=self.encrypt_and_save).grid(row=4, column=1)
        ttk.Button(main_frame, text="Decrypt", command=self.decrypt_file).grid(row=4, column=2)

        # Back button to close current window
        def Back():
            root.destroy()
            subprocess.Popen(['python', "images.py"], cwd=os.path.dirname(os.path.abspath(__file__)))

        # Frame to center the button
        center_frame = ttk.Frame(root)
        center_frame.grid(row=9, column=0, columnspan=3, padx=10, pady=15)

        btn_back = ttk.Button(center_frame, text="Back", command=Back)
        btn_back.pack(anchor="center")  # Center the button in the frame



    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def encrypt_and_save(self):
        password = self.password_entry.get()
        message = self.message_entry.get()
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

        if not password or not message or not save_path:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            original_image = cv2.imread(self.file_entry.get())
            steg = LSBSteg(original_image)
            steg.encode_text(message, password)

            cv2.imwrite(save_path, steg.image)
            messagebox.showinfo("Success", f"Message encrypted and saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {e}")

    def decrypt_file(self):
        password = self.password_entry.get()
        file_path = self.file_entry.get()

        if not password or not file_path:
            messagebox.showerror("Error", "Both password and file path are required!")
            return

        try:
            steg_decoded = LSBSteg(cv2.imread(file_path))
            hidden_text = steg_decoded.decode_text(password)
            messagebox.showinfo("Decrypted Message", f"{hidden_text}")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {e}")


# Run the GUI Application
if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApplication(root)
    root.mainloop()
