import socket
import threading
import rsa
import os
from dotenv import load_dotenv

load_dotenv()

public_key, private_key = rsa.newkeys(1024)
public_teammate = None


choice = input("Select (1) for host or (2) to connect: ")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((os.getenv("SERVER_IP"), 9999))
    server.listen()

    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_teammate = rsa.PublicKey.load_pkcs1(client.recv(1024))
elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((os.getenv("CLIENT_IP"), 9999))
    public_teammate = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))
else:
    exit()


def sending_messages(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), public_teammate))
        print("You: " + message)

def receiving_messages(c):
    while True:
        print("Teammate: " + rsa.decrypt(c.recv(1024), private_key).decode())

threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()
