# tcp_client.py
import socket

HOST = "127.0.0.1"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"[TCP] Conectado a {HOST}:{PORT}")
    for msg in [b"hola", b"mundo", b"adios"]:
        s.sendall(msg)
        data = s.recv(1024)
        print(f"[TCP] Eco: {data!r}")