import socket, sys, os, argparse

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
        #print(c.recv(1024).decode('ascii')) #print the receipt
        if text.strip() != 'root': #make sure the server isn't logged in as root
            data = c.recv(1024) #receive input
            command = data.decode('ascii') #decode the command
            result = os.popen(command).read() #run the command
            rdata = result.encode('ascii') #encode and send the output back
            c.send(rdata)
            recdata = c.recv(1024) #receive and print the receipt
            print(recdata.decode('ascii'))
            c.close()
        else:
            print('Server is root, accepting no further commands.')
            receipt = c.recv(1024) #receive the receipt and print it
            print(receipt.decode('ascii'))
            c.close() #close the connection

def client(host, command, port):
    sock = socket.socket() #instantiate the socket
    sock.connect((host, port)) #connect to the specified host and port
    print('Client has been assigned socket name', sock.getsockname())
    data = sock.recv(1024) #receive 1024 bytes
    text = data.decode('ascii') #decode the data
    print('Active user on remote machine is:', text) #print the results of the remote command
    user = text
    if user.strip() == 'root': #kill the connection if the remote server is logged in as root
        print('Remote machine active as root -- no further commands accepted')
        receipt = "Client received server's output" #encode and send the receipt
        recdata = receipt.encode('ascii')
        sock.send(recdata)
        sys.exit(0)
    else:
        data = command #encode and send the command, then receive and print the output
        dtext = data.encode('ascii')
        sock.send(dtext)
        data = sock.recv(1024)
        text = data.decode('ascii')
        print('Received output of command ', command, ": \n", text)
        receipt = "Client received server's output" #encode and send the receipt
        recdata = receipt.encode('ascii')
        sock.send(recdata)
        sys.exit(0)

if __name__ == '__main__':
    choices = {'client': client, 'server': server} #dictionary containing choices in client/server option
    parser = argparse.ArgumentParser(description='Run a remote command line command') #instantiate new argument parser
    parser.add_argument('role', choices=choices, help='Which role to play: server or client') #add the role argument
    parser.add_argument('host', help='interface the server listens at;''host the client responds to') #add the host argument
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port (default 1060)') #add the port argument
    parser.add_argument('command', help='command to execute remotely') #add the command argument
    args = parser.parse_args()
    function = choices[args.role]
    if function == choices['server']:
        function(args.host, args.p)
    else:
        function(args.host, args.command, args.p)
