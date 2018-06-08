#!/usr/bin/env python3
import threading
import socket

class connectedHost(threading.Thread):
    """Class for the connection Treads"""
    def __init__(self, connection, address, id):
        self.connection = connection
        self.ip, self.port = address
        self.id = id
        self.nickname = str(self.connection.recv(2048), "utf8")
        print(self.nickname + " is online on " + self.ip + ":" + str(self.port) + " with PID " + str(self.id))
        threading.Thread.__init__(self)


    def run(self):
        while True:
            msg = self.connection.recv(2048)
            msg = str(msg, "utf8")
            if msg == "%exit":
                print(self.nickname + " on " + self.ip + ":" + str(self.port) + " with PID " + str(self.id) + " left")
                return True #
            print(self.nickname + ": " + msg)



server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 8080))
server_socket.listen(10)
connectionDictionary = {}
connectionCounter = 0
while True:
    (client_socket, addr) = server_socket.accept()
    connectionDictionary["conn" + str(connectionCounter)] = connectedHost(client_socket, addr, connectionCounter)
    connectionDictionary["conn" + str(connectionCounter)].start()
    connectionCounter += 1
    #print(connectionDictionary)
