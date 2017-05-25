import socket, sys, os, subprocess, argparse

def server(host, port):
    sock = socket.socket() #instantiate socket
    sock.bind((host, port)) # accept from any local machine
    sock.listen() # listen
    print('Listening at {}'.format(sock.getsockname()))
    while True:
        c, addr = sock.accept() #accept connections
        print('Connected succesfully to address', addr) #print address of connected machine
        text = os.popen('whoami').read() #run the whoami command
        data = text.encode('ascii') #encode the results of whoami to ascii
        c.send(data) #send the ascii-encoded results
        print(c.recv(1024).decode('ascii')) #print the receipt
        c.close() #close the connection

def client(host, port):
    sock = socket.socket() #instantiate the socket
    sock.connect((host, port)) #connecto to the specified host and port
    print('Client has been assigned socket name', sock.getsockname())
    data = sock.recv(1024) #receive 1024 bytes
    text = data.decode('ascii') #decode the data
    print('Active user on remote machine is:', text) #print the results of the remote command
    data = 'Client successfully received username'
    text = data.encode('ascii')
    sock.send(text) #encode and send acknowledgment
    sys.exit(0)

if __name__ == '__main__':
    choices = {'client': client, 'server': server} #dictionary containing choices in client/server option
    parser = argparse.ArgumentParser(description='Run a remote command line command') #instantiate new argument parser
    parser.add_argument('role', choices=choices, help='Which role to play: server or client') #add the role argument
    parser.add_argument('host', help='interface the server listens at;''host the client responds to') #add the host argument
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port (default 1060)') #add the port argument
    args = parser.parse_args() 
    function = choices[args.role]
    function(args.host, args.p)
