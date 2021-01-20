import socket
import json


address = 'localhost'
port = 5000
package_size = 1024
closing_sequence = b'\r\n\r\n'

def run():
    socket = socket.socket()
    socket.connect((address, port))
    socket.listen()

if __name__ == '__main__':
    run()