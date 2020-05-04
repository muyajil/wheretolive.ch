from datetime import datetime
from .log import get_batch_logline


class BatchedDBCommitter:
    def __init__(self, logger, db_session, batch_size=None):
        self.logger = logger
        self.db_session = db_session
        self.batch_size = batch_size

    def commit(self, items):
        start = datetime.now()
        start_batch = datetime.now()
        for idx, item in enumerate(items):
            item_name = type(item).__name__

            if self.batch_size is not None and idx % self.batch_size == 0 and idx > 0:
                logline, start_batch = get_batch_logline(
                    idx, start_batch, start, item_name
                )
                self.logger.info(logline)
                self.db_session.commit()

        logline, _ = get_batch_logline(idx, start_batch, start, item_name)
        self.logger.info(logline)
        self.db_session.commit()
