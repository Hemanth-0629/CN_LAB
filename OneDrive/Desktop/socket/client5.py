import socket

def establish_connection(s_host, s_port):
    C_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    C_socket.connect((s_host, s_port))
    
    return C_socket

if __name__ == "__main__":
    server_host = "127.0.0.1"  
    server_port = 8000      
    
    C_socket = establish_connection(server_host, server_port)       #Creating connectionn to server using client socket
    print("Connected to server successfully....")
    
    file_name = "send.txt"                                          #This is the name of the file we want to send

    with open(file_name, "r") as file:                              #We read the file data and store it in variable file_data
        file_data = file.read()
    
    C_socket.send(file_name.encode())                               #First seding the file_name to data
    
    C_socket.send(file_data.encode())                               #Then sending the file data 

    response = C_socket.recv(1024).decode()                         #Printing the response from server
    print("Server response:", response)
    
    file.close()
    print(f"File '{file_name}' closed.")
    
    C_socket.close()
    print("Client socket closed.")                                      #Closing the connections

