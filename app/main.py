import gzip
import logging
import sys

from pathlib import Path
from stocks import HandleData


class PrepareData:
    def __init__(self):
        self.unzip_list = []
        self.unzip()
        self.target_size = None
        while True:
            self.target_size = input("Input a target size (integer only): ")
            if int(self.target_size):
                break
        handler = HandleData(self.unzip_list, self.target_size)
        handler.parse_object()


    def unzip(self):
        path = Path(__file__).parent / "../data/book_analyzer.in.gz"
        
        with gzip.open(path, 'rt') as f_in:
            for x in f_in:
                self.unzip_list.append(x) 
            


if __name__ == "__main__":
    prepare = PrepareData()