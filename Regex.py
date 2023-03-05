import re


class Regex:
    def __init__(self, source, pattern, scheme, host):
        self.source = source
        self.pattern = pattern
        self.scheme = scheme
        self.host = host

    def get_images_links(self):
        images_links_regex = re.findall(self.pattern, self.source)
        images_links = []
        for link in images_links_regex:
            if self.scheme not in link:
                link = f"{self.scheme}://{self.host}/{link}"
            images_links.append(link)

        return images_links

