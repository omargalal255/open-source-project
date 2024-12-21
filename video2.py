import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from cryptography.fernet import Fernet
import base64
import hashlib
import subprocess

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

# Main Application Class
class GUIApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("File Encryptor/Decryptor")
        self.root.resizable(False, False)

        self.encryptor_decryptor = SimpleEncryptorDecryptor()

        # Center the window
        self.init_gui()
        self.center_window()

    def init_gui(self):
        # Main container frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(row=0, column=0)

        # Title Label
        title = ttk.Label(main_frame, text="Encryptor/Decryptor Tool", font=("Helvetica", 20, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=10)

        # Password Label and Entry
        ttk.Label(main_frame, text="Enter Password:").grid(row=1, column=0, sticky=tk.E, padx=10, pady=5)
        self.password_entry = ttk.Entry(main_frame, width=40, show="*")
        self.password_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

        # Message Label and Entry
        ttk.Label(main_frame, text="Enter Message to Encrypt:").grid(row=2, column=0, sticky=tk.E, padx=10, pady=5)
        self.message_entry = ttk.Entry(main_frame, width=50)
        self.message_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

        # File Selection for Encryption
        ttk.Label(main_frame, text="Select File:").grid(row=3, column=0, sticky=tk.E, padx=10, pady=5)
        self.file_entry = ttk.Entry(main_frame, width=50)
        self.file_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=5)

        btn_select = ttk.Button(main_frame, text="Browse", command=self.select_file)
        btn_select.grid(row=3, column=3, padx=10, pady=5)

        # Save File Selection
        ttk.Label(main_frame, text="Save Location:").grid(row=4, column=0, sticky=tk.E, padx=10, pady=5)
        self.save_entry = ttk.Entry(main_frame, width=50)
        self.save_entry.grid(row=4, column=1, columnspan=2, padx=10, pady=5)

        btn_save = ttk.Button(main_frame, text="Browse", command=self.choose_save_location)
        btn_save.grid(row=4, column=3, padx=10, pady=5)

        # Buttons
        btn_encrypt = ttk.Button(main_frame, text="Encrypt and Save", command=self.encrypt_and_save)
        btn_encrypt.grid(row=5, column=1, padx=10, pady=15)

        btn_decrypt = ttk.Button(main_frame, text="Decrypt File", command=self.decrypt_file)
        btn_decrypt.grid(row=5, column=2, padx=10, pady=15)

        btn_clear = ttk.Button(main_frame, text="Clear", command=self.clear_form)
        btn_clear.grid(row=6, column=0, columnspan=3, pady=10)

        def Back():
            root.destroy()
            subprocess.Popen(['python', "Video.py"], cwd=os.path.dirname(os.path.abspath(__file__)))

        center_frame = ttk.Frame(root)
        center_frame.grid(row=9, column=0, columnspan=3, padx=10, pady=15)

        btn_back = ttk.Button(center_frame, text="Back", command=Back)
        btn_back.pack(anchor="center")  # Center the button in the frame

    # Select File for Encryption/Decryption
    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select a File")
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def choose_save_location(self):
        save_path = filedialog.asksaveasfilename(
            title="Save Encrypted File As",
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All Files", "*.*")]
        )
        if save_path:
            self.save_entry.delete(0, tk.END)
            self.save_entry.insert(0, save_path)

    def encrypt_and_save(self):
        password = self.password_entry.get()
        message = self.message_entry.get()
        save_path = self.save_entry.get()

        if not password or not message or not save_path:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            encrypted_message = self.encryptor_decryptor.encrypt(message, password)
            with open(save_path, 'w') as file:
                file.write(encrypted_message)
            messagebox.showinfo("Success", f"Message encrypted and saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {e}")

    def decrypt_file(self):
        password = self.password_entry.get()
        file_path = self.file_entry.get()

        if not password or not file_path:
            messagebox.showerror("Error", "Password and file path are required!")
            return

        try:
            with open(file_path, 'r') as file:
                encrypted_message = file.read()
                decrypted_message = self.encryptor_decryptor.decrypt(encrypted_message, password)
                messagebox.showinfo("Decrypted Message", f"Message: {decrypted_message}")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {e}")

    def clear_form(self):
        self.password_entry.delete(0, tk.END)
        self.message_entry.delete(0, tk.END)
        self.file_entry.delete(0, tk.END)
        self.save_entry.delete(0, tk.END)

    def center_window(self):
        self.root.update_idletasks()  # Ensure all widgets are loaded
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")


# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApplication(root)
    root.mainloop()
