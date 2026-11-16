import socket 
import threading 
nickname = input("Enter your nickname : ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Allows IPv4 addresses and uses TCP over UDP
server_ip = input("Enter the server IP Address: ")
client.connect((server_ip, 4000)) #connects to the server on port 4000

def receive():
    while True:
        try:
            message = client.recv(1024).decode() #Receive message from server
            if message == "NICK": #If the server asks for nickname, send it. NICK is the servers handshake.
                client.send(nickname.encode())
            else:
                print(message) #Print the message received from the server
        except:
            print("Disconnected from server")
            client.close()
            break
        
def write(): #send messages to server
    while True:
        message = f"{nickname}: {input('')}" #Get message from user
        client.send(message.encode())
        
        
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()