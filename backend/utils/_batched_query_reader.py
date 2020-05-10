class BatchedQueryReader:
    def __init__(self, query, batch_size):
        self.query = query
        self.batch_size = batch_size

    def read(self):
        offset = 0
        limit = self.batch_size
        while True:
            entities = self.query.slice(offset, limit)
            if entities.count() < self.batch_size:
                break
            else:
                offset += self.batch_size
                limit += self.batch_size
            yield entities
