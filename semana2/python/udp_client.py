# udp_client.py
import socket

HOST = "127.0.0.1"
PORT = 5001

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    for msg in [b"uno", b"dos", b"tres", b"cuatro", b"cinco"]:
        s.sendto(msg, (HOST, PORT))
        data, _ = s.recvfrom(1024)
        print(f"[UDP] Eco: {data!r}")