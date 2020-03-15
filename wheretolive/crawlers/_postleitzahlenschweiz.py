import urllib.request
from bs4 import BeautifulSoup


class PostleitzahlenschweizCrawler():

    def __init__(self):
        pass

    @property
    def base_url(self):
        return "https://postleitzahlenschweiz.ch/tabelle/"

    def crawl(self):
        request = urllib.request.Request(self.base_url)
        response = urllib.request.urlopen(request).read()
        soup = BeautifulSoup(response, features="html.parser")
        table = soup.findAll('table', class_="tableizer-table")[0]
        rows = table.findAll('tr')
        for row in rows[1:]:
            cells = row.findChildren('td')
            yield {
                "zip_code": cells[0].string,
                "name": cells[1].string,
                "state_de": cells[2].string,
                "state_fr": cells[3].string,
                "state_it": cells[4].string,
                "state_short": cells[5].string
            }