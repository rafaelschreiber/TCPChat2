#!/usr/bin/env python3
import socket
import threading
import json



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def getConnectionInfo():
    print("Please type in the server address:")
    address = str(input(">>> "))
    print("Please type in the port: (Default: 2018)")
    while True:
        port = str(input(">>> "))
        if port == "":
            port = 2018
            break
        try:
            port = int(port)
            break
        except ValueError:
            print("Please type in a number\n")
    print("Please type in your username:")
    username = str(input(">>> "))
    return [address, port, username]


def shutdown():
    client_socket.close()
    exit(0)


connectionInfo = getConnectionInfo()
try:
    client_socket.connect((connectionInfo[0], connectionInfo[1]))
except ConnectionRefusedError:
    print("There is no connection to the server")
    shutdown()


def recvMessages():
    print("Started Message Reciever")
    while True:
        data = str(client_socket.recv(2048), "utf8")
        data = json.loads(data)
        if data == "%exit":
            print("Connection closed by Server")
            shutdown()
        else:
            sender = data["username"]
            message = data["content"]
            print(sender + ": " + message)


def sendMessage(message):
    data = {"username": connectionInfo[2], "content": message}
    data = json.dumps(data)
    client_socket.send(bytes(data, "utf8"))


acceptConnectionsThread = threading.Thread(target=recvMessages)
acceptConnectionsThread.daemon = True
acceptConnectionsThread.start()

client_socket.send(bytes("%setusername " + connectionInfo[2], "utf8"))


print("Welcome " + connectionInfo[2])
while True:
    msg = str(input(">>> "))
    if msg == "%exit":
        sendMessage(msg)
        print("Connection closed by you")
        shutdown()
    else:
        sendMessage(msg)


