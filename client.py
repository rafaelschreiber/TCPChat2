#!/usr/bin/env python3
import socket

server_address = ("127.0.0.1", 8080)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket
client_socket.connect(server_address) # specify address

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
