import socket
import threading

def recevoir(s):
    """Thread pour recevoir des messages du serveur."""
    try:
        while True:
            data = s.recv(1024)
            if not data:
                print("\n📌 Serveur déconnecté.")
                break
            print("\nLui :", data.decode("utf-8"))
    except:
        pass

def envoyer(s):
    """Thread d'envoi."""
    try:
        while True:
            msg = input("Toi : ")
            if msg.strip():
                s.send(msg.encode("utf-8"))
    except:
        pass

def main():
    host = input("Adresse du serveur [127.0.0.1]: ").strip() or "127.0.0.1"
    port = int(input("Port [5000]: ").strip() or "5000")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print(f"Connexion à {host}:{port}...")
        s.connect((host, port))
        print("Connecté.")
    except Exception as e:
        print("❌ Échec de la connexion:", e)
        return

    # Threads
    threading.Thread(target=recevoir, args=(s,), daemon=True).start()
    threading.Thread(target=envoyer, args=(s,), daemon=True).start()

    # Empêche la fin du programme
    threading.Event().wait()

if __name__ == "__main__":
    main()
