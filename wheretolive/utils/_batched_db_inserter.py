from datetime import datetime


class BatchedDBInserter():

    def __init__(self, logger, db_session, batch_size=None):
        self.logger = logger
        self.db_session = db_session
        self.batch_size = batch_size

    def get_logline(self, idx, start_batch, start, item_name):
        now = datetime.now()
        logline = f'{item_name}s crawled: {idx}\t'
        logline += f'Batch Time elapesed: {now-start_batch}\t'
        logline += f'Total Time elapesed: {now-start}'
        return logline, now

    def insert(self, items):
        start = datetime.now()
        start_batch = datetime.now()
        for idx, item in enumerate(items):
            item_name = type(item).__name__
            self.db_session.add(item)
            if self.batch_size is not None and idx % self.batch_size == 0 and idx > 0:
                logline, start_batch = self.get_logline(idx, start_batch, start, item_name)
                self.logger.info(logline)
                self.db_session.commit()

        logline, _ = self.get_logline(idx, start_batch, start, item_name)
        self.logger.info(logline)
        self.db_session.commit()