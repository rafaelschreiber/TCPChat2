#!/usr/bin/env python3
import socket
import threading


server_address = ("127.0.0.1", 2018)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket
client_socket.connect(server_address) # specify address

def recvMessages():
    print("Started Message Reciever")
    while True:
        message = client_socket.recv(2048)
        message = str(message, "utf8")
        print(message)



acceptConnectionsThread = threading.Thread(target=recvMessages)
acceptConnectionsThread.start()
print("Type in your username:")
username = str(input(">>> "))
client_socket.send(bytes(username, "utf8"))
print("Welcome " + username)


while True:
    try:
        msg = str(input(">>> "))
        if msg == "%exit":
            client_socket.send(bytes("%exit", "utf8"))
            print("Connection closed")
            exit(0)
        client_socket.send(bytes(msg, "utf8"))
    except KeyboardInterrupt:
        client_socket.send(bytes("%exit", "utf8"))
        print("Connection closed")
        exit(0)
