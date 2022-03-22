import pandas as pd

class HandleData:

    def __init__(self,data_list: list, target_size: int):
        self.data = data_list
        self.target_size = target_size
        self.sell_group = []
        self.buy_group = []
        self.buy_count = 0
        self.sell_count = 0
        self.df = pd.DataFrame(columns=["timestamp", "message", "order_id", "side", "price", "size"]) 

    def parse_object(self):
        test_data = self.data[:50]
        for x in test_data:
            reduce_logging = False
            if x["message"] == "A":
                self.df.loc[len(self.df)] = x
                if x["side"] == "B":
                    self.buy_count += int(x["size"])
                if x["side"] == "S":   
                    self.sell_count += int(x["size"]) 

            elif x["message"] == "R":
                y = self.df.loc[self.df.order_id == x["order_id"]]  
                if self.buy_count >= int(self.target_size) and y.to_dict('records')[0]["side"] == "B":
                    reduce_logging = True
                    buy_timestamp = x["timestamp"]
                    reduce_log = f"{buy_timestamp} S NA"
                elif self.sell_count >= int(self.target_size) and y.to_dict('records')[0]["side"] == "S":
                    reduce_logging = True
                    sell_timestamp = x["timestamp"]
                    reduce_log = f"{sell_timestamp} B NA"
                
                size_post_reduction = int(y.to_dict('records')[0]["size"]) - int(x["size"])
                if y.to_dict('records')[0]["side"] == "B":
                    self.buy_count -= int(x["size"])
                if y.to_dict('records')[0]["side"] == "S":   
                    self.sell_count -= int(x["size"])
                if size_post_reduction <= 0:
                    self.df = self.df[self.df.order_id != x["order_id"]]
                    self.df = self.df.reset_index(drop=True)
                else:
                    self.df.loc[self.df["order_id"] == x["order_id"], "size"] = size_post_reduction
                
            timestamp = x["timestamp"]
            index_count = 0
            if self.buy_count >= int(self.target_size) and x["side"] == "B":
                reduce_logging = False
                temp_buy_df = self.df.sort_values("price", ascending=False)
                money_spent = 0.0
                target_size_diff = 0
                increase_b = int(self.target_size)
                for index, row in temp_buy_df.iterrows():
                    if row["side"] == "B":
                        increase_b = increase_b- target_size_diff
                        if increase_b <=0:
                            break
                        target_size_diff += int(row["size"])
                        
                        if target_size_diff >= int(self.target_size):
                            money_spent = money_spent + (increase_b * float(row["price"]))
                        elif target_size_diff < int(self.target_size):
                            money_spent = money_spent + (target_size_diff * float(row["price"]))
                print(f"{timestamp} S {money_spent}")
            elif self.sell_count >= int(self.target_size) and x["side"] == "S":
                reduce_logging = False
                temp_sell_df = self.df.sort_values("price")
                money_made = 0.0
                target_size_diff = 0
                increase = int(self.target_size)
                for index, row in temp_sell_df.iterrows():
                    if row["side"] == "S":
                        increase = increase- target_size_diff
                        if increase <=0:
                            break
                        target_size_diff += int(row["size"])

                        if target_size_diff >= int(self.target_size):
                            money_made = money_made + (increase * float(row["price"]))
                        elif target_size_diff < int(self.target_size):
                            money_made = money_made + (target_size_diff * float(row["price"]))
                            
                print(f"{timestamp} B {money_made}")
            if reduce_logging:
                print(reduce_log)

    def parse_object1(self):
        test_data = self.data[:10]
        for x in test_data:
            print("_____")
            print(x)
            if x["message"] == "A":
                print("Add")
                if x["side"] == "B":
                    print("BUY Order")
                    self.buy_group.append(x)
                else:
                    print("SELL Order")
                    self.buy_group.append(x)
                    #self.buy_group[x["order_id"]] = x
                self.buy_group = sorted(self.buy_group, key=lambda price: float(price["price"]))

            elif x["message"] == "R":
                print("R")
                """ if int(x["size"]) - int(self.buy_group[x["order_id"]].get("size")) <= 0:
                    print("Remove")
                    self.buy_group.pop(x["order_id"], "not_found")
                else:
                    print("Reduce")
                    y = self.buy_group[x["order_id"]].get("size")
                    self.buy_group[x["order_id"]]["size"] = y- x["size"] """
                #self.sell_group.pop(x["order_id"], "not_found")
        print("END")
        print(self.sell_group)
        print(self.buy_group)
         

            
    
