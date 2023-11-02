import socket

SERVER_ADDRESS = ('localhost', 12345)

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(SERVER_ADDRESS)

client_name = input("Enter client name: ")
socket.send(client_name.encode())

print("Connected to the server.")

socket.close()