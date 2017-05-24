#print "hello there my friend."

import socket
import sys
import subprocess
import os

s = socket.socket()
host = socket.gethostname()
port = 1337
s.bind(('', port)) #Bind to the port
s.listen(5)
print "server started on port", port
while True:
    c, addr = s.accept()
    print "Connection succesful"
    print "Connected to address ", addr
    #c.recv(1024)
    #c.send(subprocess.check_output(['whoami']))
    c.send(os.popen('whoami').read())
    c.close()