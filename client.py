import socket
import json


address = 'localhost'
port = 5000
package_size = 1024
closing_sequence = b'\r\n\r\n'

def run():
    client_socket = socket.socket()
    client_socket.connect((address, port))

    while True:
        #Цикл отвечающий за работу клиента
        try:
            connection, client_address = client_socket.accept()
        except OSError:
            print(f'{client_address} разорвал соединение. Внешний цикл.')
            break
        #listen_clients(connection, client_address)
        #response = generate_response(request.decode('utf-8'))
    client_socket.close()

if __name__ == '__main__':
    run()