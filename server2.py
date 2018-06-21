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
        while True:
            username = str(self.connection.recv(2048), "utf8")
            username = cliInterpretor(username)
            if len(username) == 2:
                if username[0] == "%setusername":
                    self.username = username[2]
                else:
                    continue
            elif len(username) >= 1:
                if username[0] == "%exit":
                    return
                else:
                    continue
            else:
                continue
        self.isonline = True
        self.broadcast(self.username + " is online")
        print(self.username + " is online on " + self.ip + ":" + str(self.port) + " with PID " + str(self.id))
        threading.Thread.__init__(self)
        self.daemon = True

