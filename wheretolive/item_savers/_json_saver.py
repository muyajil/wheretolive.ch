import json
import os


class JsonSaver():

    def __init__(self, file_path, generator):
        self.file_path = file_path
        self.generator = generator
    
    def save(self, overwrite=True):
        items = [item for item in self.generator]
        if os.path.exists(self.file_path) and not(overwrite):
            raise RuntimeError("Target file already exists and overwrite is set to False.")
        else:
            fh = open(self.file_path, 'w')
        json.dump(items, fh)
        fh.close()
