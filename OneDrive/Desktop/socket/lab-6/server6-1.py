import socket

# Creating the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Creating the address to bind to (IP and port)
ip = '127.0.0.1'  # This is your local IP address
port = 8080  # Your chosen port

address = (ip, port)

server.bind(address)  # Binding server to IP and port

server.listen(5)  # Setting the server in listening mode

while True:
    print("Server is listening...")
    conn, addr = server.accept()

    # Receiving the file name from the client
    file_name = conn.recv(1024).decode()
    print("Received file name:", file_name)

    # Receiving and saving the file
    with open(file_name, "wb") as file:
        print("Receiving file...")
        while True:
            buffer = conn.recv(1024)
            if not buffer:
                break
            file.write(buffer)

    print("File successfully received from client:", addr)

    # Close the connection
    conn.close()
