import socket
import ssl


class DownloadHTML:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def download(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.host, self.port)
        sock.connect(server_address)
        print('Connecting to %s on port %s' % server_address)

        if self.port == 443:
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=self.host)

        request_headers = 'GET / HTTP/1.0\r\nHOST: {}' \
                          '\r\nAccept: text/html' \
                          '\r\nConnection: keep-alive' \
                          '\r\nKeep-Alive: timeout=1, max=1000' \
                          '\r\nAccept-Language: ro,en' \
                          '\r\nAllow: GET' \
                          '\r\nDNT: 1' \
                          '\r\nSave-Data: on\r\n\r\n'.format(self.host).encode()

        sock.sendall(request_headers)

        response = b''
        while True:
            data = sock.recv(2048)
            if not data:
                break
            response += data

        sock.close()

        return response
