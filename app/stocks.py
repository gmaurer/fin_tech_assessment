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
        test_data = self.data[:10]
        for x in test_data:
            if x["message"] == "A":
                print("ADD")
                self.df.loc[len(self.df)] = x
                if x["side"] == "B":
                    self.buy_count += int(x["size"])
                if x["side"] == "S":   
                    self.sell_count += int(x["size"]) 

            elif x["message"] == "R":  
                print("REDUCE")
                y = self.df.loc[self.df.order_id == x["order_id"]]
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
            print("BEFORE LOGS")
            if self.buy_count >= int(self.target_size):
                print("BUY")
                temp_buy_df = self.df.sort_values("price")
                print(temp_buy_df)
                money_spent = 
                print(f"{timestamp} B {self.target_size}")
            if self.sell_count >= int(self.target_size):
                print("SELL")
                temp_sell_df = self.df.sort_values("price", ascending=False)
                print(temp_sell_df)
                money_made = 
                print(f"{timestamp} S {self.target_size}")
            print("AFTER LOGS")


                

        print(self.df)


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
         

            
    
