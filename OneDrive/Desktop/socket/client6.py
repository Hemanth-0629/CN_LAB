import socket

# Creating the client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server IP and port to connect to
server_ip = '127.0.0.1'
server_port = 8080

server_address = (server_ip, server_port)

# Connecting to the server
client.connect(server_address)

# Sending the file name to the server
file_name = input("Enter the filename you want to send: ")  # Replace with the name of the file you want to send
client.send(file_name.encode())

# Sending the file to the server
with open(file_name, "rb") as file:
    print(f"Sending {file_name} to server...")
    for data in file:
        client.send(data)

print("File sent successfully")

# Close the connection
client.close()
