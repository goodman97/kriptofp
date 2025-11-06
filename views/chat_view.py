import os
import tkinter as tk
from tkinter import messagebox, filedialog
from controllers.chat_controller import ChatController
from controllers.file_controller import FileController
from controllers.stegano_controller import SteganoController
from PIL import Image, ImageTk
import datetime
import shutil

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

        # 🔹 variabel untuk menyimpan posisi gambar steganografi agar bisa dikenali saat diklik
        self.image_positions = {}  

        # Input + tombol
        input_frame = tk.Frame(self.chat_frame, bg="#111")
        input_frame.pack(pady=5)
        self.entry = tk.Entry(input_frame, width=45)
        self.entry.grid(row=0, column=0, padx=5)
        tk.Button(input_frame, text="Send", command=self.send_message, bg="#2a9d8f", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(input_frame, text="File", command=self.send_file, bg="#264653", fg="white").grid(row=1, column=0, pady=5)
        tk.Button(input_frame, text="Stego Image", command=self.send_stegano, bg="#e9c46a", fg="black").grid(row=1, column=1, pady=5)

        # 🔹 tombol global untuk ekstraksi pesan
        tk.Button(self.chat_frame, text="Ekstrak Pesan dari Gambar",
                  command=self.extract_stego_global, bg="#f4a261", fg="black", font=("Arial", 10, "bold")).pack(pady=(10, 5))

        # Variabel
        self.current_receiver = None
        self.img_refs = []
        self.last_message_count = 0

        # Binding klik untuk deteksi klik pada gambar
        self.chat_display.bind("<Button-1>", self.on_image_click)

        # Load user list otomatis
        self.load_user_list()

        self.auto_refresh()

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
        self.current_receiver = user_display[2:]
        self.show_messages()

    def show_messages(self):
        if not self.current_receiver:
            return

        self.chat_display.config(state='normal')
        self.chat_display.delete("1.0", tk.END)
        self.image_positions.clear()
        self.img_refs.clear()

        messages = self.chat.get_messages(self.username, self.current_receiver)

        for s, r, c, msg_type, filename in messages:
            if msg_type == "text":
                text = f"Me: {c}\n" if s == self.username else f"{s}: {c}\n"
                self.chat_display.insert(tk.END, text)

            elif msg_type == "file":
                label = f"📁 Me mengirim file: {filename}\n" if s == self.username else f"📁 {s} mengirim file: {filename}\n"
                self.chat_display.insert(tk.END, label)

            elif msg_type == "stegano":
                img_path = f"samba_share/images/{filename}"
                if os.path.exists(img_path):
                    try:
                        img = Image.open(img_path)
                        img.thumbnail((200, 200))
                        img_tk = ImageTk.PhotoImage(img)
                        pos_index = self.chat_display.index(tk.END)

                        # Simpan posisi gambar agar bisa dideteksi saat diklik
                        self.image_positions[pos_index] = img_path

                        self.chat_display.image_create(tk.END, image=img_tk)
                        self.chat_display.insert(tk.END, "\n\n")
                        self.img_refs.append(img_tk)
                    except Exception as e:
                        self.chat_display.insert(tk.END, f"[Gagal menampilkan gambar: {e}]\n")
                else:
                    self.chat_display.insert(tk.END, f"[Gambar tidak ditemukan: {filename}]\n")

        self.chat_display.config(state='disabled')
        self.chat_display.yview_moveto(1.0)

    # 🔹 fungsi klik pada gambar di chat → langsung download
    def on_image_click(self, event):
        try:
            index = self.chat_display.index(f"@{event.x},{event.y}")
            nearest_pos = None
            min_diff = 999999
            for pos in self.image_positions.keys():
                diff = abs(float(self.chat_display.index(pos).split('.')[0]) - float(index.split('.')[0]))
                if diff < min_diff:
                    nearest_pos = pos
                    min_diff = diff

            if nearest_pos and min_diff < 2:  # batas toleransi klik
                img_path = self.image_positions[nearest_pos]
                if not os.path.exists(img_path):
                    messagebox.showerror("Error", "Gambar tidak ditemukan di direktori lokal.")
                    return

                save_path = filedialog.asksaveasfilename(
                    title="Simpan Gambar",
                    defaultextension=".png",
                    initialfile=os.path.basename(img_path)
                )
                if save_path:
                    shutil.copy(img_path, save_path)
                    messagebox.showinfo("Sukses", f"Gambar berhasil disimpan di:\n{save_path}")
        except Exception as e:
            print(f"[KlikGambarError] {e}")

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
        enc_data = self.file_ctrl.encrypt_file(path)
        filename = os.path.basename(path)
        save_path = f"samba_share/files/{filename}.enc"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w") as f:
            f.write(enc_data)
        self.chat.send_message(
            self.username,
            self.current_receiver,
            f"[File terenkripsi: {filename}]",
            msg_type="file",
            filename=f"{filename}.enc"
        )
        messagebox.showinfo("Sukses", f"File {filename} terenkripsi dan disimpan di {save_path}")
        self.show_messages()

    def send_stegano(self):
        if not self.current_receiver:
            messagebox.showwarning("Error", "Pilih penerima dulu!")
            return

        img_path = filedialog.askopenfilename(
            title="Pilih gambar PNG",
            filetypes=[("PNG Images", "*.png")]
        )
        if not img_path:
            return

        msg = self.entry.get()
        if not msg:
            messagebox.showwarning("Kosong", "Masukkan pesan dulu sebelum sisipkan.")
            return

        os.makedirs("samba_share/images", exist_ok=True)
        output_path = f"samba_share/images/stego_{self.username}_{self.current_receiver}.png"

        success = self.stegano.embed_message(img_path, msg, output_path)
        if not success:
            messagebox.showerror("Gagal", "Pesan terlalu panjang atau gambar tidak valid.")
            return

        self.chat.send_message(
            self.username,
            self.current_receiver,
            f"[Gambar steganografi: {os.path.basename(output_path)}]",
            msg_type="stegano",
            filename=os.path.basename(output_path)
        )

        messagebox.showinfo("Sukses", f"Pesan disisipkan dan dikirim ke {self.current_receiver}")
        self.entry.delete(0, tk.END)
        self.show_messages()

    # 🔹 tombol global untuk ekstraksi pesan dari gambar mana pun
    def extract_stego_global(self):
        img_path = filedialog.askopenfilename(
            title="Pilih gambar PNG untuk ekstraksi",
            filetypes=[("PNG Images", "*.png")]
        )
        if not img_path:
            return
        message = self.stegano.extract_message(img_path)
        if not message:
            messagebox.showinfo("Tidak ada pesan", "Tidak ditemukan pesan tersembunyi dalam gambar ini.")
            return

        save_path = filedialog.asksaveasfilename(
            title="Simpan hasil ekstraksi",
            defaultextension=".txt",
            initialfile="pesan_tersembunyi.txt"
        )
        if not save_path:
            return
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(message)
        messagebox.showinfo("Sukses", f"Pesan berhasil diekstrak dan disimpan di:\n{save_path}")

    def auto_refresh(self):
        try:
            if self.current_receiver:
                from models.db_model import Database
                temp_db = Database()
                sql = """
                SELECT id, sender, receiver, message, msg_type, filename
                FROM messages
                WHERE (sender=%s AND receiver=%s) OR (sender=%s AND receiver=%s)
                ORDER BY id DESC LIMIT 1
                """
                last_row = temp_db.fetch(sql, (self.username, self.current_receiver, self.current_receiver, self.username))
                temp_db.close()

                if last_row:
                    last_id = last_row[0][0]
                    if getattr(self, "last_msg_id", None) != last_id:
                        self.last_msg_id = last_id
                        print(f"[AUTO REFRESH] Pesan baru terdeteksi (id={last_id})")
                        self.show_messages()

        except Exception as e:
            print(f"[AutoRefreshError] {e}")

        self.root.after(1000, self.auto_refresh)

    def run(self):
        self.root.mainloop()