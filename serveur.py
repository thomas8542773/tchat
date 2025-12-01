import socket
import threading

def recevoir(conn):
    """Thread de réception des messages du client."""
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print("\n📌 Le client s'est déconnecté.")
                break
            print("\nLui :", data.decode("utf-8"))
    except:
        pass

def envoyer(conn):
    """Thread d'envoi des messages au client."""
    try:
        while True:
            msg = input("Toi : ")
            if msg.strip():
                conn.send(msg.encode("utf-8"))
    except:
        pass

def main():
    host = "0.0.0.0"
    port = int(input("Port [5000]: ").strip() or "5000")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind((host, port))
    except OSError as e:
        print("❌ Échec du bind:", e)
        return

    s.listen(1)
    print(f"Serveur en écoute sur {host}:{port} ...")
    conn, addr = s.accept()
    print("Connexion établie avec", addr)

    # Threads
    threading.Thread(target=recevoir, args=(conn,), daemon=True).start()
    threading.Thread(target=envoyer, args=(conn,), daemon=True).start()

    # Empêche la fin du programme
    threading.Event().wait()

if __name__ == "__main__":
    main()
