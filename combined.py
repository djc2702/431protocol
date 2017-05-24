import socket, sys, os, subprocess, argparse

def server(host, port):
    sock = socket.socket()
    sock.bind((host, port)) # accept from any local machine
    sock.listen(5)
    print('Listening at {}'.format(sock.getsockname()))
    while True:
        c, addr = sock.accept()
        print('Connected succesfully to address', addr)
        text = os.popen('whoami').read()
        data = text.encode('ascii')
        c.send(data)
        c.close()

def client(host, port):
    sock = socket.socket()
    sock.connect((host, port))
    data = sock.recv(1024)
    text = data.decode('ascii')
    print('Client has been assigned socket name', sock.getsockname())
    print('Active user on remote machine is:', text)
    data = 'Received username'
    text = data.encode('ascii')
    #print(sock.send(text))
    sys.exit(0)

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='Which role to play: server or client')
    parser.add_argument('host', help='interface the server listens at;''host the client responds to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
