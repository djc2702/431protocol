import socket
import sys

server = '127.0.0.1'
port = 1337

s = socket.socket()
s.connect((server,port))
#command = raw_input("Command: ")

#s.send(command)
print s.recv(1024)
print s.send("Recieved username")
sys.exit(0)
