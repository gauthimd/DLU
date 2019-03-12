#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bluetooth import *

# Create the client socket
client_socket = BluetoothSocket(RFCOMM)

client_socket.connect(("B8:27:EB:2C:13:4C", 3))

client_socket.send("Hello World")

print "Finished"

client_socket.close()
