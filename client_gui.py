import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ClientGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Client Chat TCP")

        # Zone d'affichage des messages
        self.chat_window = scrolledtext.ScrolledText(self.root, state='disabled', width=60, height=20)
        self.chat_window.pack(padx=10, pady=10)

        # Zone de saisie
        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(side=tk.LEFT, padx=10)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.root, text="Envoyer", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        # Connexion socket
        self.client_socket = None
        self.connect_to_server()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def connect_to_server(self):
        host = "127.0.0.1"
        port = 5000

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client_socket.connect((host, port))
            self.append_message("✔️ Connecté au serveur.\n")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de se connecter : {e}")
            self.root.destroy()
            return

        # Thread de réception
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    self.append_message("❌ Serveur déconnecté.\n")
                    break
                self.append_message("Serveur : " + data.decode("utf-8") + "\n")
            except:
                break

    def send_message(self, event=None):
        msg = self.entry.get().strip()
        if msg:
            self.append_message("Toi : " + msg + "\n")
            try:
                self.client_socket.send(msg.encode("utf-8"))
            except:
                self.append_message("❌ Impossible d’envoyer le message.\n")
        self.entry.delete(0, tk.END)

    def append_message(self, msg):
        self.chat_window.config(state='normal')
        self.chat_window.insert(tk.END, msg)
        self.chat_window.yview(tk.END)
        self.chat_window.config(state='disabled')

    def on_close(self):
        try:
            self.client_socket.close()
        except:
            pass
        self.root.destroy()


if __name__ == "__main__":
    ClientGUI()
