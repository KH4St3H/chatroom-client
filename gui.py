import random
import time
import string
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
from tkinter.filedialog import askopenfile

import threading
from chat_manager import ChatManager


from tkinter import ttk


class ChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")
        self.root.geometry("500x600")
        self.root.configure(bg="#2C3E50")

        self.username = None
        self.password = None
        self.chat_manager = None

        # Login/Register Frame
        self.frame_auth = tk.Frame(root, bg="#34495E", padx=20, pady=20)
        self.frame_auth.pack(pady=50)

        tk.Label(self.frame_auth, text="Username:", fg="white", bg="#34495E", font=("Arial", 12)).grid(row=0, column=0, pady=5)
        self.entry_username = tk.Entry(self.frame_auth, font=("Arial", 12))
        self.entry_username.grid(row=0, column=1, pady=5)

        tk.Label(self.frame_auth, text="Password:", fg="white", bg="#34495E", font=("Arial", 12)).grid(row=1, column=0, pady=5)
        self.entry_password = tk.Entry(self.frame_auth, show='*', font=("Arial", 12))
        self.entry_password.grid(row=1, column=1, pady=5)

        self.btn_register = ttk.Button(self.frame_auth, text="Register", command=self.register)
        self.btn_register.grid(row=2, column=0, pady=10, padx=5)

        self.btn_login = ttk.Button(self.frame_auth, text="Login", command=self.login)
        self.btn_login.grid(row=2, column=1, pady=10, padx=5)

        # Chat Frame
        self.frame_chat = tk.Frame(root, bg="#2C3E50", padx=10, pady=10)

        self.text_chat = scrolledtext.ScrolledText(self.frame_chat, state='disabled', width=60, height=20, font=("Arial", 12), bg="#ECF0F1", wrap=tk.WORD)
        self.text_chat.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.entry_message = tk.Entry(self.frame_chat, font=("Arial", 12), width=40)
        self.entry_message.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        self.btn_send_public = ttk.Button(self.frame_chat, text="Send Public", command=self.send_public)
        self.btn_send_public.pack(side=tk.LEFT, padx=5)

        self.btn_send_private = ttk.Button(self.frame_chat, text="Send Private", command=self.send_private)
        self.btn_send_private.pack(side=tk.LEFT, padx=5)

        self.btn_list_attendees = ttk.Button(self.frame_chat, text="List Attendees", command=self.list_attendees)
        self.btn_list_attendees.pack(side=tk.LEFT, padx=5)

        self.btn_send_file = ttk.Button(self.frame_chat, text="send file", command=self.send_file)
        self.btn_send_file.pack(side=tk.LEFT, padx=5)



        self.handle_exit()

    def handle_exit(self):
        def anon():
            self.chat_manager.send_bye_signal()
            self.root.destroy()
        self.root.protocol('WM_DELETE_WINDOW', anon)

    def list_attendees(self):
        self.chat_manager.list_attendees()

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if not username or not password:
            messagebox.showerror("Error", "Username and password required!")
            return

        self.chat_manager = ChatManager(username, password)
        self.chat_manager.register()
        messagebox.showinfo("Success", "Registration completed!")

    def after_login(self):
        self.frame_auth.pack_forget()
        self.frame_chat.pack(fill=tk.BOTH, expand=True)
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if not username or not password:
            messagebox.showerror("Error", "Username and password required!")
            return

        self.chat_manager = ChatManager(username, password)
        self.chat_manager.login()
        messagebox.showinfo("Success", "Logged in!")
        self.after_login()

    def send_file(self):
        filename = askopenfile()
        self.chat_manager.send_public_file(filename.name)

    def send_public(self):
        message = self.entry_message.get()
        if message:
            self.chat_manager.send_public_message(message)
            self.entry_message.delete(0, tk.END)

    def send_private(self):
        message = self.entry_message.get()
        if message:
            receivers = simpledialog.askstring("Private Message", "Enter recipient usernames (comma separated):")
            if receivers:
                self.chat_manager.send_private_message(receivers.split(','), message)
                self.entry_message.delete(0, tk.END)

    def receive_messages(self):
        while True:
            # message = self.chat_manager.readp()
            message = str(self.chat_manager.read_message())
            self.text_chat.config(state='normal')
            self.text_chat.insert(tk.END, message + "\n")
            self.text_chat.config(state='disabled')
            self.text_chat.yview(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatGUI(root)

    username = ''.join([random.choice(string.ascii_lowercase) for _ in range(5)])
    password = ''.join([random.choice(string.ascii_lowercase) for _ in range(5)])
    app.chat_manager = ChatManager(username, password)
    app.chat_manager.register()
    time.sleep(1)
    app.chat_manager.login()
    app.after_login()

    root.mainloop()
