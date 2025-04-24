import socket
from cryptography.fernet import Fernet

key = b'zttTbJ-MjmO6lz-FHnJLidJoaJWaeKMP7QSGWq9dRCA='
fernet = Fernet(key)

host = '192.168.56.1'
port = 9090

client = socket.socket()
client.connect((host, port))

while True:
    msg = input("You: ").encode()
    if msg.decode().lower() == "exit":
        encrypted = fernet.encrypt(msg)
        print("[Encrypted] Sent:", encrypted.decode())
        client.send(encrypted)
        print("You ended the chat.")
        break

    encrypted = fernet.encrypt(msg)
    print("[Encrypted] Sent:", encrypted.decode())
    client.send(encrypted)

    data = client.recv(1024)
    print("[Encrypted] Received:", data.decode())

    try:
        decrypted = fernet.decrypt(data)
        message = decrypted.decode()
        print("Server:", message)
        if message.lower() == "exit":
            print("Server ended the chat.")
            break
    except:
        print("Decryption failed.")

client.close()
