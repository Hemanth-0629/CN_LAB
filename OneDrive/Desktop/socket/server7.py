import socket
from _thread import *
import pickle
from game import Game

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

registered = {} # all registered clients to the server
logged_in = [] # all logged in clients to the server

clients = [] # list of all clients connected to the server
players = [] # list of players currently playing
queue = [] # list of clients waiting to play



def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            msg = conn.recv(4096).decode()

            if "REGISTER" in msg:
                _, mac = msg.split("/")
                if mac in registered:
                    client.conn.send("MAC already registered".encode(FORMAT))
                else:
                    registered[mac] = client
                    client.mac = mac
                    client.conn.send("OK".encode(FORMAT))
            elif "LOGIN" in msg:
                _, mac = msg.split("/")
                if mac in logged_in:
                    client.conn.send("MAC already logged in".encode(FORMAT))
                elif mac in registered:
                    client.mac = mac
                    client.time = registered[mac].time
                    if client.time <= 0:
                        client.conn.send("No time left, Please pay to continue".encode(FORMAT))
                        return
                    registered[mac] = client
                    client.conn.send("OK".encode(FORMAT))
                    time.sleep(0.1)
                    login_player(client)
                else:
                    client.conn.send("MAC not registered".encode(FORMAT))
            elif "PAY" in msg:
                _, mac, amount = msg.split("/")
                if mac in registered:
                    registered[mac].time += round(int(amount) * game_price, 2)
                    client.conn.send("OK".encode(FORMAT))
                else:
                    client.conn.send("MAC not registered".encode(FORMAT))
            elif "BALANCE" in msg:
                _, mac = msg.split("/")
                if mac in registered:
                    client.conn.send(f"OK/{registered[mac].time}".encode(FORMAT))
                else:
                    client.conn.send("MAC not registered".encode(FORMAT))

            if gameId in games:
                game = games[gameId]

                if not msg:
                    break
                else:
                    if msg == "reset":
                        game.resetWent()
                    elif msg != "get":
                        game.play(p, msg)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))