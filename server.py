#!/usr/bin/env python3
import threading
import socket
from time import gmtime, strftime, sleep
import os
import sys

connectionDictionary = {} # dicrionary where to put all connection threads in
currentTime = '' # variable for displaying the current time in logs
halt = False # indicator variable for program shutdown

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
        self.broadcast(self.nickname + " is online")
        print(self.nickname + " is online on " + self.ip + ":" + str(self.port) + " with PID " + str(self.id))
        threading.Thread.__init__(self)


    def run(self):
        while not halt:
            try:
                message = self.connection.recv(2048)
            except OSError:
                return
            if (not message) or (message == bytes("%exit", "utf8")):
                self.closeConnection("")
                return
            message = str(message, "utf8")
            self.broadcast(self.nickname + ": " + message)
        return


    def sendMessage(self, message):
        self.connection.send(bytes(message, "utf8"))


    def broadcast(self, message):
        for connection in connectionDictionary:
            if connectionDictionary[connection].isonline is True:
                if connectionDictionary[connection].id != self.id:
                    connectionDictionary[connection].sendMessage(message)


    def closeConnection(self, exitmessage):
        self.connection.send(bytes(exitmessage, "utf8"))
        self.connection.send(bytes("%exit", "utf8"))
        self.connection.close()
        self.isonline = False
        self.broadcast(self.nickname + " left")
        print(self.nickname + " on " + self.ip + ":" + str(self.port) + " with PID " + str(self.id) + " disconnected")



def updateTime():
    global currentTime
    while not halt:
        currentTime = "[" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "] "
        sleep(1)
    return


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
    global halt
    print("Closing connection listener...")
    halt = True # kill all threads
    print("Closing all connection threads...")
    for connection in connectionDictionary:
        if connectionDictionary[connection].isonline is True:
            connectionDictionary[connection].closeConnection("The server is shutting down you will be disconnected now")
    print("Closing socket...")
    server_socket.close()
    print("Exiting")
    sys.exit(0)


def acceptConnections():
    print("Started connection listener")
    global connectionDictionary
    connectionCounter = 0
    while not halt:
        try:
            connection, address = server_socket.accept()
        except ConnectionAbortedError:
            return
        connectionDictionary["conn" + str(connectionCounter)] = connectedHost(connection, address, connectionCounter)
        connectionDictionary["conn" + str(connectionCounter)].start()
        connectionCounter += 1
    return


def console():
    print("Welcome to the TCPChat2 server console")
    print("I'm ready for your commands!")
    while True:
        command = str(input(currentTime[:-1] + "$ "))
        command = cliInterpretor(command)
        if len(command) == 0:
            continue
        elif command[0] == "ls":
            ls(command[1:])
        elif command[0] == "exit":
            shutdown()
        elif command[0] == "clear" or command[0] == "cls":
            os.system("clear")
        else:
            print("Command \'" + command[0] + "\' not found")
        print("")


# creating thread for accepting connections
acceptConnectionsThread = threading.Thread(target=acceptConnections)
acceptConnectionsThread.start()

# creating thread for time logging
timeUpdater = threading.Thread(target=updateTime)
timeUpdater.start()


def main():
    console()


if __name__ == "__main__":
    main()
