import socket
import threading

host = "0.0.0.0"
port  = 4000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Allows IPv4 addresses and uses TCP over UDP
server.bind((host,port))
server.listen()

clients = []
nicknames = []

def broadcastmessages(message,client_socket):
    for client in clients:
        if client != client_socket: #Do not send the message to the client that sent it
            client.send(message)
            
def handle_client(client):
    while True:
        try: 
            message  = client.recv(1024) #Receive message from client
            if message:
                print(f"[message] {message.decode()}")
                broadcastmessages(message,client)
        except:
            #if client disconnects, remove it from the list of clients and close the connection
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames.pop(index)
            broadcastmessages(f"{nickname} left the chat!".encode(), client) #message is decoded during broadcastmessages function
            break
        
def receive_connections():
    print("Server is running and listening for connections...")
    while True:
        client, addr = server.accept()
        print(f"Connected with {str(addr)}")
        client.send("NICK".encode()) #Ask for nickname
        nickname = client.recv(1024).decode() #1024 bytes is the maximum size of the message that can be received at once
        clients.append(client)
        nicknames.append(nickname)
        print(f"Nickname of the client is {nickname}")
        broadcastmessages(f"{nickname} joined the chat!".encode(), client)
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
        
        
receive_connections()
    