import socket
from cryptography.fernet import Fernet

key = b'zttTbJ-MjmO6lz-FHnJLidJoaJWaeKMP7QSGWq9dRCA='
fernet = Fernet(key)

host = '0.0.0.0'
port = 9090

server = socket.socket()
server.bind((host, port))
server.listen(1)
print("Server listening on port 9090...")

conn, addr = server.accept()
print(f"Connected by {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        break

    print("[Encrypted] Received:", data.decode())

    try:
        decrypted = fernet.decrypt(data)
        message = decrypted.decode()
        print("Client:", message)
    except:
        print("Decryption failed.")
        continue

    if message.lower() == "exit":
        print("Client ended the chat.")
        break

    msg = input("You: ").encode()
    if msg.decode().lower() == "exit":
        encrypted = fernet.encrypt(msg)
        print("[Encrypted] Sent:", encrypted.decode())
        conn.send(encrypted)
        print("You ended the chat.")
        break

    encrypted = fernet.encrypt(msg)
    print("[Encrypted] Sent:", encrypted.decode())
    conn.send(encrypted)

conn.close()
