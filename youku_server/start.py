import os,sys
from tcp_server import socket_server

sys.path.append(os.path.dirname(__file__))


server = socket_server.SocketServer()
if __name__ == '__main__':
    server.run()