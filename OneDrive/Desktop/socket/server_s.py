import socket

MAX_CONNECTIONS = 5
PORT = 12345

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('localhost', PORT))
socket.listen(MAX_CONNECTIONS)

print("The server is listening...")

clients = []

while True:
    client_socket, client_address = socket.accept()
    print(f"Connected with IP Address {client_address}")
    
    if len(clients) < MAX_CONNECTIONS:
        clients.append(client_socket)
        print(f"Client {len(clients)} connected to Server.")
    else:
        print(f"Transferring client {len(clients) + 1} to Sr. Server.")
        # Here you can transfer the client_socket to Sr. Server as needed.
        pass
    