#!/usr/bin/env python3

"""
    Author:     Rafael Schreiber
    Created:    21-06-2018

    This is TCPChat2 Server. This programm is distributed as closed source. This program handles all
    ingoing connections and manage them. It also offers a feature-rich server console, where the server
    administrator can manage everything if he wants per hand.

"""

from functions import *
import socket
import threading
import json

connDict = { } # This dictionary contains all threaded connections

# creating main socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0", 2018)) # 0.0.0.0 scans for every domain and/or address
server_socket.listen(5)


class connectedClient(threading.Thread):
    def __init__(self, connection, address, id):
        self.connection = connection
        self.ip, self.port = address
        self.id = id
        self.username = ""
        while True:
            username = str(self.connection.recv(2048), "utf8")
            if not username:
                self.closeConnectionByClient()
                print(self.ip + ":" + str(self.port) + " with PID " + str(self.id) + " closed his connection without login")
                return
            username = cliInterpretor(username)
            if len(username) == 2:
                if username[0] == "%setusername":
                    if username[1] not in getUsernames():
                        self.username = username[1]
                        break
                    else:
                        self.send("server", "%usernametaken")
                        continue
                else:
                    continue
            elif len(username) >= 1:
                if username[0] == "%exit":
                    self.closeConnectionByClient()
                    print(self.ip + ":" + str(self.port) + " with PID " + str(self.id) + " closed his connection without login")
                    return
                else:
                    continue
            else:
                continue
        self.isonline = True
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()
        self.broadcast(self.username, "%isonline", metoo=False)
        print(self.username + " is online on " + self.ip + ":" + str(self.port) + " with PID " + str(self.id))


    def run(self):
        while True:
            message = str(self.connection.recv(2048), "utf8")
            if not message: # happens if socket is broken
                self.closeConnectionByClient()
                print(self.username + " on " + self.ip + ":" + str(self.port) + " with PID " + str(self.id) + " disconnected")
                self.broadcast(self.username, "%isoffline", metoo=False)
                return
            print(message)
            if message[0] != "%":
                continue # throw packet with invalid message away
            message = cliInterpretor(message)
            try:
                if message[0] == "%exit":
                    self.closeConnectionByClient()
                    print(self.username + " on " + self.ip + ":" + str(self.port) + " with PID " + str(self.id) + " disconnected")
                    self.broadcast(self.username, "%isoffline", metoo=False)
                    return
                elif message[0] == "%send":
                    if message[1] == '*':
                        self.broadcast(self.username, message[2])
                    elif message[1] in getUsernames(True):
                        connDict[usernameToConnection(message[1])].send(self.username, message[2])
                    else:
                        continue # throw packet with invalid username away
            except IndexError:
                continue # throw packet packet away when server cannot process it


    def broadcast(self, username, content, metoo = True):
        for connection in connDict:
            if connDict[connection].isonline is True:
                if not metoo:
                    if connDict[connection].username != self.username:
                        connDict[connection].send(username, content)
                else:
                    connDict[connection].send(username, content)


    def send(self, username, content):
        data = {"username":username, "content":content}
        data = json.dumps(data, ensure_ascii=False)
        print("Sending " + self.username + " " + data)
        self.connection.send(bytes(data, "utf8"))


    def closeConnectionByClient(self):
        self.connection.close()
        self.isonline = False


    def closeConnectionByServer(self, exitmessage = False):
        if exitmessage:
            self.send(bytes(exitmessage, "utf8"))
        self.send(bytes("%exit", "utf8"))
        self.connection.close()
        self.isonline = False


def getUsernames(connected = False):
    usernames = [ ]
    for connection in connDict:
        if connected:
            if connDict[connection].isonline is True:
                usernames.append(connDict[connection].username)
        else:
            usernames.append(connDict[connection].username)
    return usernames


def usernameToConnection(username):
    for connection in connDict:
        if connDict[connection].username == username:
            return connection
    return False


def connectionToUsername(connection):
    try:
        return connDict[connection].username
    except KeyError:
        return False


def acceptConnections():
    print("Started connection listener")
    global connDict
    connectionCounter = 0
    while True:
        connection, address = server_socket.accept()
        connDict["conn" + str(connectionCounter)] = connectedClient(connection, address, connectionCounter)
        connectionCounter += 1


# starting thread for accept connections
acceptConnectionsThread = threading.Thread(target=acceptConnections)
acceptConnectionsThread.daemon = True
acceptConnectionsThread.start()

while True:
    print()
    command = str(input("$ "))
    if command == "ls":
        print(connDict)
    else:
        print("Command not found")
