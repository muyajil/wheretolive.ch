from ..crawlers import TownsCrawler
from ..json_savers import FileJsonSaver
import logging
import os

logger = logging.getLogger(os.path.basename(__file__))

logger.debug('Starting process...')
crawler = TownsCrawler()
logger.debug('Mapping Switzerland...')
towns_by_zip = crawler.crawl()
logger.debug('Saving towns_by_zip...')
saver = FileJsonSaver()
saver.save('/home/muy/repositories/wheretolive.ch/towns_by_zip.json', towns_by_zip)
