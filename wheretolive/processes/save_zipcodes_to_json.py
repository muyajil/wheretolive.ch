from ..item_savers import JsonSaver
from ..crawlers import PostleitzahlenschweizCrawler


print(f'Starting process {__file__}')
crawler = PostleitzahlenschweizCrawler()
saver = JsonSaver("/home/muy/repositories/wheretolive.ch/zip_codes.json", crawler.crawl())
saver.save()