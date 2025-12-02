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

        # Frame utama
        self.main_frame = tk.Frame(self.root, bg="#111")
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar kiri
        self.sidebar = tk.Frame(self.main_frame, width=180, bg="#222")
        self.sidebar.pack(side="left", fill="y")
        tk.Label(self.sidebar, text="User Online", fg="white", bg="#222",
                 font=("Arial", 11, "bold")).pack(pady=5)

        self.user_listbox = tk.Listbox(self.sidebar, bg="#333", fg="white", selectbackground="#555")
        self.user_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.user_listbox.bind("<<ListboxSelect>>", self.select_user)

        self.list_user_map = {}

        # Area chat
        self.chat_frame = tk.Frame(self.main_frame, bg="#111")
        self.chat_frame.pack(side="right", fill="both", expand=True)

        self.chat_display = tk.Text(self.chat_frame, state='disabled', width=60, height=20,
                                    bg="#111", fg="white")
        self.chat_display.pack(padx=10, pady=10)

        # Variabel untuk posisi gambar dan file
        self.image_positions = {}
        self.file_positions = {}

        # Input + tombol
        input_frame = tk.Frame(self.chat_frame, bg="#111")
        input_frame.pack(pady=5)

        self.entry = tk.Entry(input_frame, width=45)
        self.entry.grid(row=0, column=0, padx=5)

        tk.Button(input_frame, text="Send", command=self.send_message,
                  bg="#2a9d8f", fg="white").grid(row=0, column=1, padx=5)

        tk.Button(input_frame, text="File", command=self.send_file,
                  bg="#264653", fg="white").grid(row=1, column=0, pady=5)

        tk.Button(input_frame, text="Stego Image", command=self.send_stegano,
                  bg="#e9c46a", fg="black").grid(row=1, column=1, pady=5)

        tk.Button(self.chat_frame, text="Ekstrak Pesan dari Gambar",
                  command=self.extract_stego_global, bg="#f4a261",
                  fg="black", font=("Arial", 10, "bold")).pack(pady=(10, 5))

        self.current_receiver = None
        self.img_refs = []
        self.last_message_count = 0

        # SINGLE handler untuk klik
        self.chat_display.bind("<Button-1>", self.on_click)

        # Load user otomatis
        self.load_user_list()
        self.auto_refresh()

    def on_click(self, event):
        self.on_image_click(event)
        self.on_file_click(event)

    def load_user_list(self):
        users = self.chat.get_all_users(self.username)
        self.user_listbox.delete(0, tk.END)

        now = datetime.datetime.now()

        self.list_user_map = {}

        for idx, (uname, last) in enumerate(users):
            delta = (now - last).total_seconds()
            status = "🟢" if delta < 15 else "⚪"

            show_text = f"{status} {uname}"
            self.user_listbox.insert(tk.END, show_text)

            self.list_user_map[idx] = uname

        self.root.after(5000, self.load_user_list)

    def select_user(self, event):
        selection = self.user_listbox.curselection()
        if not selection:
            return

        idx = selection[0]
        self.current_receiver = self.list_user_map.get(idx)

        if self.current_receiver:
            self.show_messages()

    def show_messages(self):
        if not self.current_receiver:
            return

        self.chat_display.config(state='normal')
        self.chat_display.delete("1.0", tk.END)

        self.image_positions.clear()
        self.file_positions.clear()
        self.img_refs.clear()

        messages = self.chat.get_messages(self.username, self.current_receiver)

        for s, r, c, msg_type, filename in messages:

            if msg_type == "text":
                text = f"Me: {c}\n" if s == self.username else f"{s}: {c}\n"
                self.chat_display.insert(tk.END, text)

            elif msg_type == "file":
                sender = "Me" if s == self.username else s
                clean_name = filename.replace(".enc", "")

                # Tampilkan teks tombol (klik)
                start_pos = self.chat_display.index("end-1c")
                self.chat_display.insert(tk.END, f"📁 {sender} mengirim file: {clean_name}\n")

                # Simpan posisi untuk klik
                self.file_positions[start_pos] = filename

            elif msg_type == "stegano":
                label = f"🖼️ Me mengirim gambar:\n" if s == self.username else f"🖼️ {s} mengirim gambar:\n"
                self.chat_display.insert(tk.END, label)
                img_path = f"samba_share/images/{filename}"

                if os.path.exists(img_path):
                    try:
                        img = Image.open(img_path)
                        img.thumbnail((200, 200))
                        img_tk = ImageTk.PhotoImage(img)
                        pos_index = self.chat_display.index(tk.END)

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

    def on_image_click(self, event):
        try:
            index = self.chat_display.index(f"@{event.x},{event.y}")

            nearest_pos = None
            min_diff = 999999

            for pos in self.image_positions.keys():
                diff = abs(float(self.chat_display.index(pos).split('.')[0])
                           - float(index.split('.')[0]))
                if diff < min_diff:
                    nearest_pos = pos
                    min_diff = diff

            if nearest_pos and min_diff < 2:
                img_path = self.image_positions[nearest_pos]
                if not os.path.exists(img_path):
                    messagebox.showerror("Error", "Gambar tidak ditemukan.")
                    return

                save_path = filedialog.asksaveasfilename(
                    title="Simpan Gambar",
                    defaultextension=".png",
                    initialfile=os.path.basename(img_path)
                )
                if save_path:
                    shutil.copy(img_path, save_path)
                    messagebox.showinfo("Sukses", f"Gambar disimpan di:\n{save_path}")

        except Exception as e:
            print(f"[KlikGambarError] {e}")

    def on_file_click(self, event):
        try:
            index = self.chat_display.index(f"@{event.x},{event.y}")

            nearest_pos = None
            min_diff = 999999

            for pos in self.file_positions.keys():
                diff = abs(float(self.chat_display.index(pos).split('.')[0])
                        - float(index.split('.')[0]))
                if diff < min_diff:
                    nearest_pos = pos
                    min_diff = diff

            # Jika klik tepat (maksimal selisih 1 baris)
            if nearest_pos and min_diff < 1.0:
                filename = self.file_positions[nearest_pos]
                enc_path = f"samba_share/files/{filename}"

                if not os.path.exists(enc_path):
                    messagebox.showerror("Error", "File terenkripsi tidak ditemukan.")
                    return

                # Read encrypted base64
                with open(enc_path, "r", encoding="utf-8") as f:
                    enc_base64 = f.read().strip()

                # Decrypt
                try:
                    decrypted_bytes = self.file_ctrl.decrypt_file(enc_base64)
                except Exception as e:
                    messagebox.showerror("Error", f"Decrypt gagal: {e}")
                    return

                # Save file hasil decrypt
                save_path = filedialog.asksaveasfilename(
                    title="Simpan File",
                    initialfile=filename.replace(".enc", "")
                )
                if not save_path:
                    return

                with open(save_path, "wb") as f:
                    f.write(decrypted_bytes)

                messagebox.showinfo("Sukses", f"File berhasil disimpan:\n{save_path}")

        except Exception as e:
            print(f"[KlikFileError] {e}")

    def send_message(self):
        msg = self.entry.get()
        if not msg or not self.current_receiver:
            messagebox.showwarning("Error", "Pilih penerima dan isi pesan.")
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

        encrypted_base64 = self.file_ctrl.encrypt_file(path)

        filename = os.path.basename(path)
        enc_name = filename + ".enc"

        os.makedirs("samba_share/files", exist_ok=True)
        save_path = f"samba_share/files/{enc_name}"

        with open(save_path, "w") as f:
            f.write(encrypted_base64)

        self.chat.send_file(
            self.username,
            self.current_receiver,
            enc_name
        )

        messagebox.showinfo("Sukses", f"File {filename} terenkripsi dan dikirim.")
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
            messagebox.showwarning("Kosong", "Masukkan pesan.")
            return

        os.makedirs("samba_share/images", exist_ok=True)
        output_path = f"samba_share/images/stego_{self.username}_{self.current_receiver}.png"

        success = self.stegano.embed_message(img_path, msg, output_path)
        if not success:
            messagebox.showerror("Gagal", "Pesan terlalu panjang.")
            return

        self.chat.send_message(
            self.username,
            self.current_receiver,
            f"[Gambar steganografi: {os.path.basename(output_path)}]",
            msg_type="stegano",
            filename=os.path.basename(output_path)
        )

        messagebox.showinfo("Sukses", f"Gambar stego terkirim.")
        self.entry.delete(0, tk.END)
        self.show_messages()

    def download_file(self, msg):
        enc_data = msg["message"]
        filename = msg["filename"]

        try:
            decrypted = self.file_ctrl.decrypt_file(enc_data)
        except Exception as e:
            messagebox.showerror("Error", f"Tidak bisa mendekripsi file:\n{e}")
            return

        os.makedirs("downloads", exist_ok=True)
        save_path = f"downloads/{filename.replace('.enc', '')}"

        with open(save_path, "wb") as f:
            f.write(decrypted)

        messagebox.showinfo("Berhasil", f"File berhasil diunduh ke:\n{save_path}")

    def extract_stego_global(self):
        img_path = filedialog.askopenfilename(
            title="Pilih gambar PNG",
            filetypes=[("PNG Images", "*.png")]
        )
        if not img_path:
            return

        message = self.stegano.extract_message(img_path)
        if not message:
            messagebox.showinfo("Tidak ada pesan", "Tidak ditemukan pesan.")
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

        messagebox.showinfo("Sukses", f"Pesan disimpan di:\n{save_path}")

    def auto_refresh(self):
        try:
            if self.current_receiver:
                from models.db_model import Database
                temp_db = Database()

                sql = """
                SELECT id FROM messages
                WHERE (sender=%s AND receiver=%s) OR (sender=%s AND receiver=%s)
                ORDER BY id DESC LIMIT 1
                """

                last_row = temp_db.fetch(sql, (
                    self.username, self.current_receiver,
                    self.current_receiver, self.username
                ))
                temp_db.close()

                if last_row:
                    last_id = last_row[0][0]
                    if getattr(self, "last_msg_id", None) != last_id:
                        self.last_msg_id = last_id
                        self.show_messages()

        except Exception as e:
            print(f"[AutoRefreshError] {e}")

        self.root.after(1000, self.auto_refresh)

    def run(self):
        self.root.mainloop()