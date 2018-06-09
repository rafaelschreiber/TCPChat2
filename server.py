#!/usr/bin/env python3
import threading
import socket
import time

connectionDictionary = {} # dicrionary where to put all connection threads in

# building socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 2018))
server_socket.listen(10)

class connectedHost(threading.Thread):
    """Class for the connection Treads"""
    def __init__(self, connection, address, iD):
        self.connection = connection
        self.ip, self.port = address
        self.id = iD
        self.nickname = str(self.connection.recv(2048), "utf8")
        self.isonline = True
        broadcast(self.nickname + " is online on " + self.ip + ":" + str(self.port) + " with PID " + str(self.id))
        print(self.nickname + " is online on " + self.ip + ":" + str(self.port) + " with PID " + str(self.id))
        threading.Thread.__init__(self)


    def run(self):
        while True:
            message = self.connection.recv(2048)
            if (not message) or (message == bytes("%exit", "utf8")):
                self.connection.close()
                self.isonline = False
                print(self.nickname + " on " + self.ip + ":" + str(self.port) + " with PID " + str(self.id) + " left")
                broadcast(self.nickname + " on " + self.ip + ":" + str(self.port) + " with PID " + str(self.id) + " left")
                return
            message = str(message, "utf8")
            broadcast(self.nickname + ": " + message)


    def sendMessage(self, message):
        self.connection.send(bytes(message, "utf8"))




def broadcast(message):
    print("Broadcasted")
    for connection in connectionDictionary:
        if connectionDictionary[connection].isonline is True:
            connectionDictionary[connection].sendMessage(message)


def cliInterpretor(string):
    keywords = []
    currentWord = ''
    isInWord = False
    isInString = False
    for char in string:
        if isInString:
            if char == "\"" or char == "\'":
                keywords.append(currentWord)
                currentWord = ''
                isInString = False
            else:
                currentWord += char
        elif isInWord:
            if char == ' ':
                keywords.append(currentWord)
                currentWord = ''
                isInWord = False
            else:
                currentWord += char
        else:
            if char == "\"" or char == "\'":
                isInString = True
            elif char != ' ':
                isInWord = True
                currentWord += char
    if currentWord != '':
        keywords.append(currentWord)
    return keywords


def ls(args):
    if len(args) == 0:
        if len(connectionDictionary) == 0:
            print("ls: There are no connections")
        for key in connectionDictionary:
            print(key + ": " + str(connectionDictionary[key]))
    elif len(args) == 1:
        if args[0] in connectionDictionary:
            print("Properties of \'" + args[0] + "\':")
            print("ID: " + str(connectionDictionary[args[0]].id))
            print("IP: " + connectionDictionary[args[0]].ip)
            print("Port: " + str(connectionDictionary[args[0]].port))
            print("Nickname: " + connectionDictionary[args[0]].nickname)
            print("isonline: " + str(connectionDictionary[args[0]].isonline))
        else:
            print("ls: Connection \'" + args[0] + "\' not found")
    else:
        print("ls: Expect max. 2 arguments")



def shutdown():
    print("Closing all connections...")
    exit(0)


def acceptConnections():
    print("Started connection listener")
    global connectionDictionary
    connectionCounter = 0
    while True:
        connection, address = server_socket.accept()
        connectionDictionary["conn" + str(connectionCounter)] = connectedHost(connection, address, connectionCounter)
        connectionDictionary["conn" + str(connectionCounter)].start()
        connectionCounter += 1


# creating thread for accepting connections
acceptConnectionsThread = threading.Thread(target=acceptConnections)
acceptConnectionsThread.start()

print("Welcome to the TCPChat2 server console")
print("I'm ready for your commands!")
while True:
    command = str(input("$ "))
    command = cliInterpretor(command)
    if command[0] == "ls":
        ls(command[1:])
    elif command[0] == "exit":
        shutdown()
    else:
        print("Command \'" + command[0] + "\' not found")
    print("")
