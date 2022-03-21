import gzip
import logging
import sys

from pathlib import Path
from stocks import HandleData


class PrepareData:
    def __init__(self):
        self.unzip_list = []
        self.unzip()
        try:
            int(sys.argv[1])
        except:
            print("Command Line Arg was not an integer")
            quit()
        self.target_size = sys.argv[1]
        handler = HandleData(self.unzip_list, self.target_size)
        handler.parse_object()


    def unzip(self): 
        '''
        Grabs absolute path from system, appends local path and reads GZ file to list of objects
        '''
        path = Path(__file__).parent / "../data/book_analyzer.in.gz"
        
        with gzip.open(path, 'rt') as f_in:
            for x in f_in:
                new_record = BookRecord(x.split())
                self.unzip_list.append(new_record.__dict__) 


class BookRecord:
    def __init__(self, raw_record: list):
        
        self.timestamp = raw_record[0]
        self.message = raw_record[1]
        self.order_id = raw_record[2] 
        self.side = raw_record[3] if len(raw_record) == 6 else None
        self.price = raw_record[4] if len(raw_record) == 6 else None
        self.size = raw_record[5] if len(raw_record) == 6 else raw_record[3]



if __name__ == "__main__":
    prepare = PrepareData()