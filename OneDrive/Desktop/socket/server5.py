import socket

def start_server(server_host, server_port):
    S_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    S_socket.bind((server_host, server_port))
    S_socket.listen(1)                                                        #Maximum no. of clients can be in queue
    
    print("Server listening...")
    
    C_socket, C_address = S_socket.accept()                                    #Accepting the connection
    print(f"Connection from {C_address}")
                              
    file_name = C_socket.recv(1024).decode()                                #Ask for the file Name
    
    text_data = C_socket.recv(1024).decode()                                #This is the data that we receive
    
    server_filename = "minato.txt"                                          #The file in which we will save the contents we got
    
    with open(server_filename, "w") as file:                                #Writing the received data on the file
        file.write(text_data)
    
    response = f"Data written to file '{server_filename}' on the server."   #Sending the response to client
    C_socket.send(response.encode())
    
    C_socket.close()                                                        #Closing connections
    S_socket.close()

if __name__ == "__main__":
    server_host = "127.0.0.1"                                               #Ip address
    server_port = 8000                                                      #Port no
    
    start_server(server_host, server_port)

