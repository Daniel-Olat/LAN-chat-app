import socket 
import threading 
nickname = input("Enter your nickname : ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Allows IPv4 addresses and uses TCP over UDP
client.connect(("127.0.0.1", 4000)) #Connect to the server

def receive():
    while True:
        try:
            message = client.recv(1024).decode() #Receive message from server
            if message == "NICK": #If the server asks for nickname, send it
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