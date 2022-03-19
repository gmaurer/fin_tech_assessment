

class HandleData:

    def __init__(self,data_list: list, target_size: int):
        self.data = data_list
        self.target_size = target_size

    def parse_object(self):
        for x in range(10):
            print(self.data[x])
    
