#!/usr/bin/env python3
import threading
import socket
from time import gmtime, strftime, sleep
import os

connectionDictionary = {} # dicrionary where to put all connection threads in
currentTime = '' # variable for displaying the current time in logs
halt = False # indicator variable for program shutdown

# building socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0", 2018))
server_socket.listen(10)

class connectedHost(threading.Thread):
    """Class for the connection Treads"""
    def __init__(self, connection, address, iD):
        self.connection = connection
        self.ip, self.port = address
        self.id = iD
        if self.ip in getConnectedIPs():
            self.rejectConnection("You are already connected with this IP")
            return
        while not halt:
            username = str(self.connection.recv(2048), "utf8")
            username = cliInterpretor(username)
            if username[0] == "%exit":
                return
            elif username[0] == "%setusername":
                if len(username) < 2:
                    continue
                self.username = username[1]
                break
        self.isonline = True
        self.broadcast(self.username + " is online")
        print(self.username + " is online on " + self.ip + ":" + str(self.port) + " with PID " + str(self.id))
        threading.Thread.__init__(self)
        self.daemon = True


    def run(self):
        while not halt:
            try:
                message = self.connection.recv(2048)
            except OSError:
                return
            if (not message) or (message == bytes("%exit", "utf8")):
                self.closeConnection()
                return
            message = str(message, "utf8")
            self.broadcast(self.username + ": " + message)
        return


    def sendMessage(self, message):
        self.connection.send(bytes(message, "utf8"))


    def changeUsername(self, newUsername):
        self.broadcast(self.username + " changed his name to " + newUsername)
        self.username = newUsername


    def broadcast(self, message):
        for connection in connectionDictionary:
            if connectionDictionary[connection].isonline is True:
                if connectionDictionary[connection].id != self.id:
                    connectionDictionary[connection].sendMessage(message)


    def rejectConnection(self, exitmessage):
        try:
            self.connection.send(bytes(exitmessage, "utf8"))
            self.connection.send(bytes("%exit", "utf8"))
        except:
            return
        self.connection.close()
        self.isonline = False
        print("Connection from " + self.ip + ":" + self.port + "rejected")
        return



    def closeConnection(self, exitmessage=False):
        if exitmessage:
            try:
                self.connection.send(bytes(exitmessage, "utf8"))
                self.connection.send(bytes("%exit", "utf8"))
            except OSError:
                return
        self.connection.close()
        self.isonline = False
        self.broadcast(self.username + " left")
        print(self.username + " on " + self.ip + ":" + str(self.port) + " with PID " + str(self.id) + " disconnected")
        return



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
            print("Username: " + connectionDictionary[args[0]].username)
            print("isonline: " + str(connectionDictionary[args[0]].isonline))
        else:
            print("ls: Connection \'" + args[0] + "\' not found")
    else:
        print("ls: Expect max. 2 arguments")


def getConnectedIPs():
    ipList = []
    for connection in connectionDictionary:
        if connectionDictionary[connection].isonline is True:
            ipList.append(connectionDictionary[connection].ip)
    print(ipList)
    return ipList



def setusername(args):
    if len(args) == 0:
        print("setusername: Of which connection do you want to change the username")
    elif len(args) == 1:
        if args[0] in connectionDictionary:
            if connectionDictionary[args[0]].isonline is True:
                print("setusername: To which username do you want to change \'" + args[0] + "\'")
            else:
                print("setusername: \'" + args[0] + "\' isn't online anymore")
        else:
            print("setusername: Connection \'" + args[0] + "\' doesn't exist")
    elif len(args) == 2:
        if args[0] in connectionDictionary:
            if connectionDictionary[args[0]].isonline is True:
                connectionDictionary[args[0]].changeUsername(args[1])
            else:
                print("setusername: \'" + args[0] + "\' isn't online anymore")
        else:
            print("setusername: Connection \'" + args[0] + "\' doesn't exist")


def kick(args):
    if len(args) == 0:
        print("kick: Which connection do you want to kick?")
    elif len(args) == 1:
        try:
            connectionDictionary[args[0]].closeConnection("You were kicked by the server")
        except KeyError:
            print("kick: the connection \'" + args[0] + "\' doesn't exist")
    elif len(args) == 2:
        try:
            connectionDictionary[args[0]].closeConnection(args[1])
        except KeyError:
            print("kick: the connection \'" + args[0] + "\' doesn't exist")
    else:
        print("kick: Expect max. 2 arguments")


def time(args):
    if len(args) == 0:
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    else:
        print("kick: Expect max. 0 arguments")



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
    exit(0)


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
        try:
            connectionDictionary["conn" + str(connectionCounter)].start()
        except RuntimeError:
            print("Connection don't created, because initialization process failed")
        connectionCounter += 1
    return


def console():
    print("Welcome to the TCPChat2 server console")
    print("I'm ready for your commands!")
    while True:
        command = str(input("$ "))
        command = cliInterpretor(command)
        if len(command) == 0:
            continue
        elif command[0] == "ls":
            ls(command[1:])
        elif command[0] == "exit":
            shutdown()
        elif command[0] == "kick":
            kick(command[1:])
        elif command[0] == "clear" or command[0] == "cls":
            os.system("clear")
        elif command[0] == "time":
            time(command[1:])
        elif command[0] == "setusername":
            setusername(command[1:])
        else:
            print("Command \'" + command[0] + "\' not found")
        print("")


# creating thread for accepting connections
acceptConnectionsThread = threading.Thread(target=acceptConnections)
acceptConnectionsThread.daemon = True
acceptConnectionsThread.start()

# creating thread for time logging
timeUpdater = threading.Thread(target=updateTime)
timeUpdater.daemon = True
timeUpdater.start()


def main():
    console()


if __name__ == "__main__":
    main()
