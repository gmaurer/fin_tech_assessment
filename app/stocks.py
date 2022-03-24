import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

class HandleData:

    def __init__(self,data_list: list, target_size: int):
        self.data = data_list
        self.target_size = target_size
        self.buy_count = 0
        self.sell_count = 0
        self.previous_buy_count = 0
        self.previous_sell_count = 0
        self.timestamp = None
        self.previous_sell_amount = None
        self.previous_buy_amount = None
        self.previous_timestamp = None
        self.df = pd.DataFrame(columns=["timestamp", "message", "order_id", "side", "price", "size"]) 
        self.log_list = []

    def na_logging_handler(self, record_of_order_id, buy_or_sell:str):
        
        if buy_or_sell == "S":
            opposite = "B"
            count = self.previous_sell_count
        else:
            opposite = "S"
            count = self.previous_buy_count
        if count >= int(self.target_size) and record_of_order_id.to_dict('records')[0]["side"] == buy_or_sell:
            reduce_logging = True
            reduce_log = f"{self.timestamp} {opposite} NA"
        else:
            reduce_logging = False
            reduce_log = None
        return(reduce_logging, reduce_log)

    def reduce_count(self, dataframe, record_of_order_id, buy_or_sell:str):
        if dataframe.to_dict('records')[0]["side"] == buy_or_sell:   
            if buy_or_sell == "S":
                self.sell_count -= int(record_of_order_id["size"])
            else:
                self.buy_count -= int(record_of_order_id["size"])

    def loop_sorted_dataframe(self,dataframe, target_size_diff:int, money:float, buy_or_sell:str):
        increase = int(self.target_size)
        for inderecord, row in dataframe.iterrows():
            if row["side"] == buy_or_sell:
                increase = increase - target_size_diff
                if increase <=0:
                    break
                target_size_diff += int(row["size"])
                
                if target_size_diff >= int(self.target_size):
                    money = money + (increase * float(row["price"]))
                elif target_size_diff < int(self.target_size):
                    money = money + (target_size_diff * float(row["price"]))
        return(money)
    
    def check_previous_amount(self, current_amount:float, current_side:str, log:str):
        if current_side == "S":
            if self.previous_sell_amount != current_amount:
                print(log)
                self.log_list.append(log)
                self.previous_sell_amount = current_amount
        elif current_side == "B":
            if self.previous_buy_amount != current_amount:
                print(log)
                self.log_list.append(log)
                self.previous_buy_amount = current_amount
        self.previous_timestamp = self.timestamp

    def handle_stock_price_calculation(self, data_record:str):
        if self.buy_count >= int(self.target_size) and data_record["side"] == "B":
            reduce_logging_buy = False
            temp_buy_df = self.df.sort_values("price", ascending=False)
            money_spent = self.loop_sorted_dataframe(temp_buy_df, 0, 0.0, "B")
            self.check_previous_amount(money_spent, "S", f"{self.timestamp} S {money_spent}")
        elif self.sell_count >= int(self.target_size) and data_record["side"] == "S":
            reduce_logging_sell = False
            temp_sell_df = self.df.sort_values("price")
            money_made = self.loop_sorted_dataframe(temp_sell_df, 0, 0.0, "S")
            self.check_previous_amount(money_made, "B", f"{self.timestamp} B {money_made}")

    def parse_object(self):
        for record in self.data:
            self.previous_buy_count = self.buy_count
            self.previous_sell_count = self.sell_count
            self.timestamp = record["timestamp"]
            reduce_logging_buy = False
            reduce_logging_sell = False
            if record["message"] == "A":
                self.df.loc[len(self.df)] = record
                if record["side"] == "B":
                    self.buy_count += int(record["size"])
                if record["side"] == "S":   
                    self.sell_count += int(record["size"]) 

            elif record["message"] == "R":
                record_to_reduce = self.df.loc[self.df.order_id == record["order_id"]]
                reduce_side = record_to_reduce.to_dict('records')[0]["side"]
                size_post_reduction = int(record_to_reduce.to_dict('records')[0]["size"]) - int(record["size"])
                self.reduce_count(record_to_reduce, record, "B")
                self.reduce_count(record_to_reduce, record, "S")
                if size_post_reduction <= 0:
                    self.df = self.df[self.df.order_id != record["order_id"]]
                    self.df = self.df.reset_index(drop=True)
                else:
                    self.df.loc[self.df["order_id"] == record["order_id"], "size"] = size_post_reduction
                temp = self.df.loc[self.df['side'] == reduce_side]

                temp_buy_df = temp.sort_values("price", ascending=False)
                temp_sell_df = temp.sort_values("price")
                if reduce_side == "S" and temp_sell_df.size != 0 and self.sell_count >= int(self.target_size):
                    money = self.loop_sorted_dataframe(temp_sell_df, 0, 0.0, "S")
                    self.check_previous_amount(money, "B", f"{self.timestamp} B {money}")
                elif reduce_side == "B" and temp_buy_df.size != 0 and self.buy_count >= int(self.target_size):
                    money = self.loop_sorted_dataframe(temp_buy_df, 0, 0.0, "B")
                    self.check_previous_amount(money, "S", f"{self.timestamp} S {money}")
                else:
                    reduce_logging_buy,reduce_log_buy = self.na_logging_handler(record_to_reduce, "B")
                    reduce_logging_sell,reduce_log_sell = self.na_logging_handler(record_to_reduce, "S")
                            
            self.handle_stock_price_calculation(record)
            if reduce_logging_buy:
                self.check_previous_amount(0.0, "S", reduce_log_buy)
            if reduce_logging_sell:
                self.check_previous_amount(0.0, "B", reduce_log_sell)
        #print(self.log_list)

            
    
