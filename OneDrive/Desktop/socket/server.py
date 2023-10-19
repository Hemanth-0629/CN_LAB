import socket
import threading

s = socket.socket()
print ("Socket is successfully created")

port = 8000

s.bind(('127.0.0.1', port))
print ("socket binded to %s" %(port))

def handle_clients(conn,addr):
    print(f"Connection received from {addr}")
    connected = True
    while connected:
        msg = conn.recv(1024).decode('utf-8')
        print(f"Message from {addr}: {msg}")
        if(msg=="!DISCONNECT"):
            connection = False
            conn.close()
            break
        else:
            conn.send(msg.encode('utf-8'))


s.listen(5)
print ("socket is listening")

while True:
    c, addr = s.accept()
    print ('Got connection from', addr )
    thread = threading.Thread(target=handle_clients,args=(c,addr))
    thread.start()
    print(f"Active_connections: {threading.active_count()-1}")
    break
