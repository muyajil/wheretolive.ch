class HealthInsuranceCrawler():

    def __init__(self):
        self.base_url = "https://www.comparis.ch/immobilien/result/list?page=0"

    @property
    def ranges(self):
        return {
            "page":  [x for x in range(1000)],
        }

    def compose_url(self, ranges):
        pass

    def crawl(self):
        pass
