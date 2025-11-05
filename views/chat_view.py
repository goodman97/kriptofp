import tkinter as tk
from tkinter import messagebox, filedialog
from controllers.chat_controller import ChatController
from controllers.file_controller import FileController
from controllers.stegano_controller import SteganoController
import datetime

class ChatWindow:
    def __init__(self, username):
        self.root = tk.Tk()
        self.root.title(f"Secure Chat - {username}")
        self.username = username
        self.chat = ChatController()
        self.file_ctrl = FileController()
        self.stegano = SteganoController()

        # Frame utama (sidebar kiri + area kanan)
        self.main_frame = tk.Frame(self.root, bg="#111")
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar kiri (daftar user)
        self.sidebar = tk.Frame(self.main_frame, width=180, bg="#222")
        self.sidebar.pack(side="left", fill="y")
        tk.Label(self.sidebar, text="User Online", fg="white", bg="#222", font=("Arial", 11, "bold")).pack(pady=5)

        self.user_listbox = tk.Listbox(self.sidebar, bg="#333", fg="white", selectbackground="#555")
        self.user_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.user_listbox.bind("<<ListboxSelect>>", self.select_user)

        # Area kanan (chat)
        self.chat_frame = tk.Frame(self.main_frame, bg="#111")
        self.chat_frame.pack(side="right", fill="both", expand=True)

        self.chat_display = tk.Text(self.chat_frame, state='disabled', width=60, height=20, bg="#111", fg="white")
        self.chat_display.pack(padx=10, pady=10)

        # Input + tombol
        input_frame = tk.Frame(self.chat_frame, bg="#111")
        input_frame.pack(pady=5)
        self.entry = tk.Entry(input_frame, width=45)
        self.entry.grid(row=0, column=0, padx=5)
        tk.Button(input_frame, text="Send", command=self.send_message, bg="#2a9d8f", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(input_frame, text="File", command=self.send_file, bg="#264653", fg="white").grid(row=1, column=0, pady=5)
        tk.Button(input_frame, text="Image", command=self.send_image, bg="#e9c46a", fg="black").grid(row=1, column=1, pady=5)

        # Variabel
        self.current_receiver = None

        # Load user list otomatis
        self.load_user_list()

    def load_user_list(self):
        users = self.chat.get_all_users(self.username)
        self.user_listbox.delete(0, tk.END)
        now = datetime.datetime.now()

        for uname, last in users:
            delta = (now - last).total_seconds()
            status = "🟢" if delta < 15 else "⚪"
            self.user_listbox.insert(tk.END, f"{status} {uname}")

        self.root.after(5000, self.load_user_list)

    def select_user(self, event):
        selection = self.user_listbox.curselection()
        if not selection:
            return
        user_display = self.user_listbox.get(selection[0])
        self.current_receiver = user_display[2:]  # skip simbol status
        self.show_messages()

    def show_messages(self):
        if not self.current_receiver:
            return
        self.chat_display.config(state='normal')
        self.chat_display.delete("1.0", tk.END)
        messages = self.chat.get_messages(self.username, self.current_receiver)
        for s, r, c in messages:
            if s == self.username:
                self.chat_display.insert(tk.END, f"Me: {c}\n", "send")
            else:
                self.chat_display.insert(tk.END, f"{s}: {c}\n", "recv")
        self.chat_display.config(state='disabled')

    def send_message(self):
        msg = self.entry.get()
        if not msg or not self.current_receiver:
            messagebox.showwarning("Error", "Pilih penerima dulu dan tulis pesan.")
            return
        self.chat.send_message(self.username, self.current_receiver, msg)
        self.entry.delete(0, tk.END)
        self.show_messages()

    def send_file(self):
        if not self.current_receiver:
            messagebox.showwarning("Error", "Pilih penerima dulu!")
            return
        path = filedialog.askopenfilename(title="Pilih file")
        if not path:
            return
        filename = path.split("/")[-1]
        save_path = f"samba_share/files/{filename}.enc"
        self.file_ctrl.encrypt_file(path, save_path)
        messagebox.showinfo("File terenkripsi", f"File disimpan di {save_path}")

    def send_image(self):
        if not self.current_receiver:
            messagebox.showwarning("Error", "Pilih penerima dulu!")
            return
        img_path = filedialog.askopenfilename(title="Pilih gambar PNG", filetypes=[("PNG Images", "*.png")])
        if not img_path:
            return
        msg = self.entry.get()
        if not msg:
            messagebox.showwarning("Kosong", "Masukkan pesan dulu sebelum sisipkan.")
            return
        save_path = f"samba_share/images/stego_{self.username}_{self.current_receiver}.png"
        self.stegano.embed_message(img_path, msg, save_path)
        messagebox.showinfo("Sukses", f"Pesan disisipkan di {save_path}")

    def run(self):
        self.root.mainloop()
