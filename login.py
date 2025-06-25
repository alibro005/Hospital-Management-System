# login.py

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Pillow library for image handling

from main_gui import HospitalGUI

# Dummy credentials

VALID_USERNAME = "admin@hms.com"
VALID_PASSWORD = "1234"


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Login")
        self.root.geometry("800x400")
        self.root.resizable(False, False)

        # Main Frame
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        # ===== Left Image Panel =====

        left_image = Image.open("images/login.png")  
        left_image = left_image.resize(
            (350, 400), Image.Resampling.LANCZOS
        )  
        # Resize to fit the panel
        left_photo = ImageTk.PhotoImage(left_image)

        left_panel = tk.Label(main_frame, image=left_photo, width=300)
        left_panel.image = left_photo  
        left_panel.pack(side="left", fill="y")

        # ===== Right Login Panel =====
        
        login_frame = tk.Frame(main_frame, padx=40, pady=20)
        login_frame.pack(side="right", fill="both", expand=True)

        tk.Label(login_frame, text="Login to  HMS", font=("Poppins", 16, "bold")).pack(
            pady=15
        )

        tk.Label(login_frame, text="Username:", font=("Poppins", 11)).pack(anchor="w")
        self.username_entry = tk.Entry(login_frame, font=("Poppins", 11))
        self.username_entry.pack(fill="x", pady=8)

        tk.Label(login_frame, text="Password:", font=("Poppins", 11)).pack(anchor="w")
        self.password_entry = tk.Entry(login_frame, show="*", font=("Poppins", 11))
        self.password_entry.pack(fill="x", pady=8)

        tk.Button(
            login_frame,
            text="Login",
            command=self.authenticate,
            font=("Poppins", 9, "bold"),
            bg="#4CAF50",
            fg="white",
            width=18,
            height=2,
        ).pack(pady=20)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            messagebox.showinfo("Login Success", "Welcome!")
            self.root.destroy()

            # Launch the main GUI
           
            root = tk.Tk()
            app = HospitalGUI(root)
            root.mainloop()

        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


# Run login window

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

    