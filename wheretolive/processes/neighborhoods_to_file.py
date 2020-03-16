from ..crawlers import NeighborhoodMappingCrawler
from ..json_savers import FileJsonSaver
import logging
import os

logger = logging.getLogger(os.path.basename(__file__))

logger.debug('Starting process...')
mapper = NeighborhoodMappingCrawler()
logger.debug('Mapping Switzerland...')
towns_by_zip, neighborhoods_by_zip = mapper.crawl()
logger.debug('Saving towns_by_zip...')
saver = FileJsonSaver()
saver.save('/home/muy/repositories/wheretolive.ch/towns_by_zip.json', towns_by_zip)
logger.debug('Saving neighborhoods_by_zip...')
saver.save('/home/muy/repositories/wheretolive.ch/neighborhoods_by_zip.json', neighborhoods_by_zip)
