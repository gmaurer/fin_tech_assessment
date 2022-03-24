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
                raw_record = x.split()
                new_record = {
                    "timestamp":raw_record[0],
                    "message":raw_record[1],
                    "order_id":raw_record[2],
                    "side":raw_record[3] if len(raw_record) == 6 else None,
                    "price":raw_record[4] if len(raw_record) == 6 else None,
                    "size":raw_record[5] if len(raw_record) == 6 else raw_record[3]
                }
                try:
                    self.unzip_list.append(new_record) 
                except:
                    "Bad Record, proceeding to next"

if __name__ == "__main__":
    import time
    start_time = time.time()
    prepare = PrepareData()
    print("--- %s seconds ---" % (time.time() - start_time))
