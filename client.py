#!/usr/bin/env python3
import socket
import threading
import sys


halt = False # indicator variable for program shutdown


def recvMessages():
    print("Started Message Reciever")
    while not halt:
        try:
            message = client_socket.recv(2048)
        except OSError:
            return
        message = str(message, "utf8")
        if message == "%exit":
            shutdown()
            return
        else:
            print(message)
    return


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
    global halt
    halt = True
    client_socket.close()
    sys.exit(0)



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connectionInfo = getConnectionInfo()
try:
    client_socket.connect((connectionInfo[0], connectionInfo[1]))
except ConnectionRefusedError:
    print("There is no connection to the server")
    client_socket.close()
    sys.exit(0)


acceptConnectionsThread = threading.Thread(target=recvMessages)             #Funtkionen machen wäre sinnvoll fresse sebi
acceptConnectionsThread.start()
client_socket.send(bytes(connectionInfo[2], "utf8"))
print("Welcome " + connectionInfo[2])
while not halt:
    try:
        msg = str(input(">>> "))
        if msg == "%exit":
            client_socket.send(bytes("%exit", "utf8"))
            print("Connection closed")
            shutdown()
            exit(0)
        client_socket.send(bytes(msg, "utf8"))
    except KeyboardInterrupt:
        client_socket.send(bytes("%exit", "utf8"))
        print("Connection closed")
        shutdown()
        exit(0)
    except OSError:
        pass

