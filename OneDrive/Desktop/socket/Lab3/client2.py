import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            print("Error receiving message")
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('127.0.0.1', 5000)
client_socket.connect(server_address)

while True:
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    message = input("> ")

    if message.startswith("/private"):
        recipient = message.split()[1]
        private_message = input(f"Private message to {recipient}: ")
        client_socket.send(f"@{recipient} {private_message}".encode())
    else:
        client_socket.send(message.encode())