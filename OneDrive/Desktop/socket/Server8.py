import threading
import socket
import pickle
import asyncio


ROOM_ID = {}
NO_OF_PLAYERS = 2
MAC_ID = {}
TimeLeft = {}
# Function to handle individual clients
option = []
id = 0


def calling(clinet_number, msg):
    thread = threading.Thread(target=handle_client, args=(
        connections[client_number-1], addresses[client_number-1]))
    thread.start()


def Room(conn, msg):
    global id
    info = conn.recv(SIZE)
    info = pickle.loads(info)
    times = int(info["amount"])/10
    MAC = info["mac"]

    flag = 0
    id = info["id"]
    ROOM_ID[conn] = (id)
    id_count = 0
    Time = times*60

    TimeLeft[msg] = times*60

    for i, j in ROOM_ID.items():
        if j == id:
            id_count += 1
    # print(f"count:{id_count}")
    if id_count > NO_OF_PLAYERS:
        flag = 1

    if MAC_ID.get(MAC):
        MAC_ID[MAC] += times
    else:
        MAC_ID[MAC] = times
    msg = {
        "flag": flag,
        "time": times
    }
    msg = pickle.dumps(msg)
    conn.send(msg)


IP = socket.gethostbyname(socket.gethostname())
PORT = 8000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "BYE"

# List to store client connections and addresses
connections = []
addresses = []
sizes = 0


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            msg = conn.recv(SIZE)
            msg = pickle.loads(msg)
            option.append(msg)
            # print(f"Message:{msg}")
            for item in option:
                if isinstance(item, dict):
                    TimeLeft[item['Mac']] = item['Timeleft']

            if msg == DISCONNECT_MSG:
                connections.remove(conn)
                addresses.remove(addr)
                if conn in ROOM_ID.keys():
                    del ROOM_ID[conn]
                connected = False

            else:
                length = len(connections)
                for i in range(0, len(connections)):
                    if (msg == "Scissors" or msg == "Rock" or msg == "Paper") and conn != connections[i]:
                        msg = pickle.dumps(msg)
                        connections[i].send(msg)
        except ConnectionResetError:
            print(f"[{addr}] Client connection forcibly closed.")
            connections.remove(conn)
            addresses.remove(addr)
            break

    conn.close()


print("[Starting] server is starting...")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
print(f"[Listening] Server is listening on {IP}:{PORT}")

while True:
    conn, addr = server.accept()
    connections.append(conn)
    addresses.append(addr)

    client_number = len(connections)
    msg = conn.recv(SIZE)
    msg = pickle.loads(msg)
    print(msg)
    print(f"count:{len(ROOM_ID)}")
    print(len(TimeLeft))

    if msg in TimeLeft.keys():
        if len(ROOM_ID) >= 2:
            # del TimeLeft[msg]
            print("Hello")
            timesleft = pickle.dumps(-1)
            conn.send(timesleft)
            msg = {
                "flag": 1,
                "time": 0
            }
            msg = pickle.dumps(msg)
            conn.send(msg)
        elif TimeLeft[msg] > 0:
            ROOM_ID[conn] = (id)
            timesleft = pickle.dumps(TimeLeft[msg])
            conn.send(timesleft)
        else:
            # print("Hiii")
            conn.send(pickle.dumps(0))
            Room(conn, msg)
    else:
        # print("Hi")
        conn.send(pickle.dumps(0))
        Room(conn, msg)

    if len(ROOM_ID) <= 2:
        # print("Hii")
        calling(client_number, msg)  # Call the function to handle the client

    print(f"[Active connections] {threading.active_count() - 1}")
