from ._switzerland import Switzerland
import logging
import os
logging.basicConfig(level=os.environ.get('LOGLEVEL'))

__all__ = ["Switzerland"]
