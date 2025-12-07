# tcp_server.py
import socket

HOST = "0.0.0.0"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[TCP] Servidor escuchando en {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"[TCP] Conexión de {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    print(f"[TCP] Cliente {addr} cerró la conexión")
                    break
                print(f"[TCP] Recibido: {data!r}")
                conn.sendall(data)  # eco