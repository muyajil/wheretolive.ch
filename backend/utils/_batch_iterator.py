from itertools import islice


class BatchIterator:
    def __init__(self, batch_size, iterable):
        self.batch_size = batch_size
        self.iterable = iterable

    @property
    def batches(self):
        if self.batch_size is None:
            return self.iterable
        it = iter(self.iterable)
        while True:
            batch = list(islice(it, self.batch_size))
            if batch == []:
                return
            yield batch
