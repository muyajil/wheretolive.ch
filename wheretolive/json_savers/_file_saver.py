import json
import os


class FileJsonSaver():

    def __init__(self, encoding='utf8', overwrite=True):
        self.overwrite = overwrite
        self.encoding = encoding

    def save(self, path, data):
        if os.path.exists(path) and not(self.overwrite):
            raise RuntimeError("Target file already exists and overwrite is set to False.")
        else:
            fh = open(path, 'w', encoding=self.encoding)
        json.dump(data, fh, ensure_ascii=False)
        fh.close()
