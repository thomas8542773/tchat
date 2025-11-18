import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ServerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Serveur Chat TCP")

        self.chat_window = scrolledtext.ScrolledText(self.root, state='disabled', width=60, height=20)
        self.chat_window.pack(padx=10, pady=10)

        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(side=tk.LEFT, padx=10)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.root, text="Envoyer", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        self.server_socket = None
        self.client_conn = None

        threading.Thread(target=self.start_server, daemon=True).start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def start_server(self):
        host = "0.0.0.0"
        port = 5000

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)

        self.append_message(f"🟢 Serveur en écoute sur {host}:{port}\n")

        self.client_conn, addr = self.server_socket.accept()
        self.append_message(f"✔️ Client connecté depuis {addr}\n")

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                data = self.client_conn.recv(1024)
                if not data:
                    self.append_message("❌ Client déconnecté.\n")
                    break
                self.append_message("Client : " + data.decode("utf-8") + "\n")
            except:
                break

    def send_message(self, event=None):
        msg = self.entry.get().strip()
        if msg:
            self.append_message("Toi : " + msg + "\n")
            try:
                self.client_conn.send(msg.encode("utf-8"))
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
            if self.client_conn:
                self.client_conn.close()
            if self.server_socket:
                self.server_socket.close()
        except:
            pass
        self.root.destroy()


if __name__ == "__main__":
    ServerGUI()
