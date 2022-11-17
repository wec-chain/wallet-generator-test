from Server import Server
import sys

if __name__ == '__main__':
    ip = sys.argv[1]
    port = int(sys.argv[2])

    node = Server(ip, port)
    node.startAPI(port)
