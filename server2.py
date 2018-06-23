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
debug = False # indicator variable for debugging

# creating main socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0", 2018)) # 0.0.0.0 scans for every domain and/or address
server_socket.listen(5)


class connectedClient(threading.Thread):
    def __init__(self, connection, address, iD):
        self.connection = connection
        self.ip, self.port = address
        self.id = iD
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
                    if username[1] not in getUsernames(connected=True) and username[1] != "*" and username[1] != "server":
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
            if debug:
                try:
                    print("debug: Incoming: " + message) # just for debugging
                except UnicodeEncodeError:
                    print("debug: Incoming: Error while decoding ingoing message")
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
                elif message[0] == "%getusers":
                    self.sendRaw({"username":"server", "content":"%userlist", "userlist":getUsernames(connected=True)})
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
        if debug:
            try:
                print("debug: Outgoing: Sending " + self.username + " " + data)
            except UnicodeEncodeError:
                print("debug: Outgoing: Error while decoding outgoing message") # just for debugging
        self.connection.send(bytes(data, "utf8"))


    def sendRaw(self, data):
        data = json.dumps(data, ensure_ascii=False)
        if debug:
            try:
                print("debug: Outgoing: Sending " + self.username + " " + data)
            except UnicodeEncodeError:
                print("debug: Outgoing: Error while decoding outgoing message") # just for debugging
        self.connection.send(bytes(data, "utf8"))


    def closeConnectionByClient(self):
        self.connection.close()
        self.isonline = False


    def closeConnectionByServer(self, exitmessage = False):
        if exitmessage:
            self.send("server", exitmessage)
        self.send("server", "%exit")
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


def shutdown(args):
    global server_socket
    if len(args) == 0:
        print("Closing all connections")
        for connection in connDict:
            if connDict[connection].isonline is True:
                connDict[connection].closeConnectionByServer("Server Closed")
    elif len(args) == 1:
        print("Closing all connections")
        for connection in connDict:
            if connDict[connection].isonline is True:
                connDict[connection].closeConnectionByServer(args[0])
    else:
        print("exit: Requires max. 1 argument")
        return
    print("Closing server socket")
    server_socket.close()
    print("Stopping")
    exit(0)


def ls(args):
    if len(args) == 0:
        if len(connDict) == 0:
            print("There are no connections")
            return
        for connection in connDict:
            print(connection + ": " + str(connDict[connection]))
    else:
        print("ls: Requires max. 1 argument")


def changeDebug(args):
    global debug
    if len(args) == 1:
        if args[0] == "on":
            if debug is True:
                print("Debug is already on")
            else:
                print("Turned debug on")
                debug = True
        elif args[0] == "off":
            if debug is False:
                print("Debug is already off")
            else:
                print("Turned debug off")
                debug = False
        elif args[0] == "status":
            if debug is True:
                print("Debug is currently turned on")
            else:
                print("Debug is currently turned off")
        else:
            print("debug: Unknown argument: " + args[0])
    else:
        print("debug: Requires exactly 1 argument")


# starting thread for accept connections
acceptConnectionsThread = threading.Thread(target=acceptConnections)
acceptConnectionsThread.daemon = True
acceptConnectionsThread.start()

while True:
    print()
    command = str(input("$ "))
    command = cliInterpretor(command)
    if len(command) == 0:
        print("Command not found")
        continue
    if command[0] == "exit":
        shutdown(command[1:])
    elif command[0] == "ls":
        ls(command[1:])
    elif command[0] == "debug":
        changeDebug(command[1:])
    else:
        print("Command not found")
