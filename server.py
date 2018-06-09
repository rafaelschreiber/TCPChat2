#!/usr/bin/env python3
import threading
import socket
import time

connectionDictionary = {} # dicrionary where to put all connection threads in

class connectedHost(threading.Thread):
    """Class for the connection Treads"""
    def __init__(self, connection, address, id):
        self.connection = connection
        self.ip, self.port = address
        self.id = id
        self.nickname = str(self.connection.recv(2048), "utf8")
        self.isonline = True
        print(self.nickname + " is online on " + self.ip + ":" + str(self.port) + " with PID " + str(self.id))
        threading.Thread.__init__(self)


    def run(self):
        while True:
            msg = self.connection.recv(2048)
            msg = str(msg, "utf8")
            if msg == "%exit":
                print(self.nickname + " on " + self.ip + ":" + str(self.port) + " with PID " + str(self.id) + " left")
                self.isonline = False
                return True
            print(self.nickname + ": " + msg)


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
            print(key + ": " + connectionDictionary[key])
    elif len(args) == 1:
        if args[0] in connectionDictionary:
            print("Properties of \'" + args[0] + "\':")
            print("ID: " + connectionDictionary[args[0]].id)
            print("IP: " + connectionDictionary[args[0]].ip)
            print("Port: " + connectionDictionary[args[0]].port)
            print("Nickname: " + connectionDictionary[args[0]].nickname)
            print("isOnline: " + connectionDictionary[args[0]].isOnline)
        else:
            print("ls: Connection \'" + args[0] + "\' not found")
    else:
        print("ls: Expect max. 2 arguments")



def shutdown():
    print("Closing all connections...")
    exit(0)


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





"""
while True:
    command = str(input("$"))
    break
           
    
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 2018))
server_socket.listen(10)
connectionCounter = 0
while True:
    (client_socket, addr) = server_socket.accept()
    connectionDictionary["conn" + str(connectionCounter)] = connectedHost(client_socket, addr, connectionCounter)
    connectionDictionary["conn" + str(connectionCounter)].start()
    connectionCounter += 1
    print(connectionDictionary)
"""
