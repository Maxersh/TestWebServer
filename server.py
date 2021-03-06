import socket
import json
from views import *
import ytbscrapper.ytbscrapper

STANDART_URLS = {
    '/': root,
    '/favicon.ico': favicon
}

address = 'localhost'
port = 5000
package_size = 1024
closing_sequence = b'\r\n\r\n'

def generate_headers(method, url):
    if method != 'GET':
        return '<body><h1>Method not allowed.</h1></body>', 405
    if url in STANDART_URLS:
        return STANDART_URLS[url](), 200
    video_path, info_path = ytbscrapper.ytbscrapper.get_info(url[1:])
    with open(info_path, 'r') as file:
        info = str(json.load(file))[:100]
    return info, 200

def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url    = parsed[1]
    return method, url

def generate_response(request):
    method, url = parse_request(request)
    print(f'request parsed: {method}, {url}')
    headers, code = generate_headers(method, url)
    print(f'header generated: {headers}, {code}')
    return headers.encode('utf-8')

def listen_clients(connection, client_address):
    data_lst = []
    while True:
        #Цикл отвечающий за приём целого сообщения
        try:
            buff = connection.recv(package_size)
        except ConnectionError:
            print(f'{client_address} разорвал соединение. Внутренний цикл.')
            break
        if not buff:
            break
        data_lst.append(buff.decode('utf-8'))
        if not buff.endswith(closing_sequence):
            continue
        data = ''.join(data_lst)[:-len(closing_sequence)]
        print(data)
        data_lst.clear()
        #Payload
        response = generate_response(data)
        print(f'response generated: {response}')
        connection.sendall(response)

def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Need to delete in prodaction?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((address, port))
    server_socket.listen(1)

    print('Server Started.')

    while True:
        #Цикл отвечающий за работу сервера
        try:
            connection, client_address = server_socket.accept()
        except OSError:
            print(f'{client_address} разорвал соединение. Внешний цикл.')
            break
        listen_clients(connection, client_address)
        print('cycle is alive')
        #response = generate_response(request.decode('utf-8'))
    server_socket.close()

if __name__ == '__main__':
    run()