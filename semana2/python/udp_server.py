# udp_server.py
import socket

HOST = "0.0.0.0"
PORT = 5001

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"[UDP] Servidor escuchando en {HOST}:{PORT}")
    while True:
        data, addr = s.recvfrom(1024)
        print(f"[UDP] De {addr} -> {data!r}")
        s.sendto(data, addr)  # eco