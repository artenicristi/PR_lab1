from DownloadHTML import DownloadHTML
from DownloadImages import DownloadImages
from Regex import Regex


scheme = 'http'
host = 'me.utm.md'
port = 80
pattern = r'<img.*?src=[\'"](.*?\.(?:jpg|png|gif))[\'"].*?>'

print('1 -> me.utm.md : 80\n'
      '2 -> utm.md    : 443\n')

option = int(input('Choose an option: '))

if option == 2:
    scheme = 'https'
    host = 'utm.md'
    port = 443

links = Regex(DownloadHTML(host, port).download().decode(), pattern, scheme, host).get_images_links()
DownloadImages(host, port, links).multithreading()
