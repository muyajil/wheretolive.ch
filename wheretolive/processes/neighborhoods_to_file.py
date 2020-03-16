from ..aggregators import NeighborhoodAggregator
from ..json_savers import FileJsonSaver
import logging
import os

logger = logging.getLogger(os.path.basename(__file__))

logger.debug('Starting process...')
aggregator = NeighborhoodAggregator(towns_by_zip_path='/home/muy/repositories/wheretolive.ch/towns_by_zip.json')
logger.debug('Mapping Switzerland...')
neighborhoods_by_zip = aggregator.aggregate()
logger.debug('Saving neighborhoods_by_zip...')
saver = FileJsonSaver()
saver.save('/home/muy/repositories/wheretolive.ch/neighborhoods_by_zip.json', neighborhoods_by_zip)
