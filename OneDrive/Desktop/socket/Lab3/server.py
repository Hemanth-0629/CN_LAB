import socket
import threading

def handle_client(client_socket, client_address, username):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                print("Client disconnected:", client_address)
                del clients[username]
                break

            if message.startswith("#"):
                recipient = message.split()[0][1:]
                if recipient in clients:
                    recipient_socket = clients[recipient]
                    recipient_socket.send(f"~{username}~: {message.split(' ', 1)[1]}".encode())
                else:
                    client_socket.send(f"Recipient '{recipient}' not found.".encode())
            else:
                print(f"Received from {username}: {message}")
                for client in clients.values():
                    client.send(f"~{username}~: {message}".encode())
        except Exception as e:
            print("Client disconnected:", client_address)
            del clients[username]
            break

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 5000)
server_socket.bind(server_address)
server_socket.listen(5)

clients = {}

def main():
    while True:
        print("Server is listening: ")
        client_socket, client_address = server_socket.accept()
        print("Connected:", client_address)

        # Prompt the client to enter a username
        client_socket.send("Please enter your name: ".encode())
        username = client_socket.recv(1024).decode()

        clients[username] = client_socket

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, username))
        client_thread.start()

if __name__ == "__main__":
    main()
