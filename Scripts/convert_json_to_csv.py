import pandas as pd
import json

with open("C:/Users/shubh/Desktop/smart_toronto_traffic_dashboard/Data/Motor_Vehicle_Collisions_Data.json") as file:
    raw_data =  json.load(file)

data_list = [feature["properties"] for feature in raw_data["features"]]

df = pd.DataFrame(data_list)

df.to_csv("C:/Users/shubh/Desktop/smart_toronto_traffic_dashboard/Data/Motor_Vehicle_Collisions_Data.csv", index=False)

print("Data converted successfully!")
