import os
import re
import socket
import ssl
from urllib.parse import urlparse
import threading


class DownloadImages:
    def __init__(self, host, port, images_links):
        self.host = host
        self.port = port
        self.images_links = images_links
        self.sem = threading.Semaphore(3)

    def download(self):
        while len(self.images_links):
            self.sem.acquire()

            if not len(self.images_links):
                break

            link = self.images_links.pop()

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (self.host, self.port)
            sock.connect(server_address)
            print(f"Downloading in thread: {threading.current_thread()}")

            if self.port == 443:
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=self.host)

            url = urlparse(link)
            request = "GET {} HTTP/1.1\r\nHost: {}\r\n\r\n".format(url.path, self.host)

            sock.sendall(request.encode())
            response = sock.recv(1024)
            headers, image_data = response.split(b"\r\n\r\n", 1)

            content_length_match = re.search(r'content-length:\s*(\d+)', headers.decode().lower())
            content_length = int(content_length_match.group(1))

            while len(image_data) < content_length:
                image_data += sock.recv(1024)

            image_path = "C:/py/img/" + os.path.basename(url.path)
            with open(image_path, "wb") as f:
                f.write(image_data)

            sock.close()
            self.sem.release()

    def multithreading(self):
        t1 = threading.Thread(target=self.download)
        t2 = threading.Thread(target=self.download)
        t3 = threading.Thread(target=self.download)
        t4 = threading.Thread(target=self.download)

        t1.start()
        t2.start()
        t3.start()
        t4.start()