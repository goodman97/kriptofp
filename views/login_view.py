import tkinter as tk
from controllers.auth_controller import AuthController
from views.chat_view import ChatWindow

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Secure Chat Login")
        self.root.geometry("300x200")
        self.auth = AuthController()

        self.username = tk.Entry(self.root)
        self.username.pack(pady=5)
        self.password = tk.Entry(self.root, show="*")
        self.password.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.register).pack()

        self.label = tk.Label(self.root, text="")
        self.label.pack()

    def login(self):
        user = self.username.get()
        pwd = self.password.get()
        if self.auth.login_user(user, pwd):
            self.root.destroy()
            ChatWindow(user).run()
        else:
            self.label.config(text="Login gagal!")

    def register(self):
        user = self.username.get()
        pwd = self.password.get()
        self.auth.register_user(user, pwd)
        self.label.config(text="Akun berhasil dibuat!")

    def run(self):
        self.root.mainloop()
