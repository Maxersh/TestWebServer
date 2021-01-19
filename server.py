import socket
import json
import ytbscrapper.ytbscrapper

STANDART_URLS = {
    '/': '<body><h1>Youtube scrapper.</h1>\n'
         'Please enter channel_id.\n'
         'Like that: localhost:5000/<channel_id></body>',
    '/favicon.ico': ''
}

def generate_headers(method, url):
    if method != 'GET':
        return '<body><h1>Method not allowed.</h1></body>', 405
    if url in STANDART_URLS:
        return STANDART_URLS[url], 200
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
    headers, code = generate_headers(method, url)
    return headers.encode()



def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Need to delete in prodaction?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(('localhost', 5000))
    server_socket.listen(5)

    quit = False
    print('Server Started.')

    while not quit:
        try:
            client_socket, addr = server_socket.accept()
            request = client_socket.recv(1024)
            print(request)
            print(addr)

            response = generate_response(request.decode('utf-8'))
            print(response)

            client_socket.sendto(response, addr)
            client_socket.close()

        except Exception as ex:
            print(ex)
            print('Server Stopped.')
            quit = True

if __name__ == '__main__':
    run()