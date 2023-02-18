import socket
import threading

PORT=11111
# SERVER="0.0.0.0"
SERVER="127.0.0.1"

ADDRESS=(SERVER,PORT)

FORMAT="utf-8"

client,names=[],[]

server=socket.socket()

server.bind(ADDRESS)
def StartChat():
    print("Server is working on "+SERVER)

    server.listen(2)
    while True:
        try:
            conn,addr=server.accept()
            name=conn.recv(1024).decode(FORMAT)
            names.append(name)
            client.append(conn)
            conn.send(f"Hello {name} you are connected sucessfully!!\n".encode(FORMAT))
            broadcastMessage(f"{name} has joined the chat!",name,conn)
            thread=threading.Thread(target=handle,args=(conn,addr,name))
            thread.start()
            print(f"\nActive connections: {threading.activeCount()-1}\n")
        except ConnectionAbortedError:
            print("!!ConnectionAbortedError arrived!! Retry once")
            continue
def handle(conn,addr,name):
    print(f"\nNew connection{addr}\n")
    while True:
        message=conn.recv(1024).decode(FORMAT)
        if message:
            for c in client:
                if c!=conn:
                    c.send((name.split(" ")[0]+": "+message.strip("\n")).encode(FORMAT))
                else:
                    c.send(("You: "+message.strip("\n")).encode(FORMAT))

def broadcastMessage(message,name,conn):
    for c in client:
        if c!=conn:
            c.send(message.encode(FORMAT))
        else:
            c.send("Now you can start your chat\n".encode(FORMAT))

StartChat()
