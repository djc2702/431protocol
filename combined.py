import socket, sys, os, subprocess, argparse

def server(port):
    sock = socket.socket()
    sock.bind(('0.0.0.0', port)) # accept from any local machine
    sock.listen(5)
    print('Listening at {}'.format(sock.getsockname()))
    while True:
        c, addr = sock.accept()
        print('Connected succesfully to address', addr)
        text = os.popen('whoami').read()
        data = text.encode('ascii')
        c.send(data)
        c.close()

def client(port):
    sock = socket.socket()
    sock.connect(('flatline', port))
    data = sock.recv(1024)
    text = data.decode('ascii')
    print('Active user on remote machine is:', text)
    data = 'Received username'
    text = data.encode('ascii')
    #print(sock.send(text))
    sys.exit(0)

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    parser.add_argument('role', choices=choices, help='Which role to play: server or client')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)
