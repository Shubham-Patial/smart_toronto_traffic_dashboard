import pandas as pd
import sqlite3
import os

csv_path = os.path.join("C:/Users/shubh/Desktop/smart_toronto_traffic_dashboard/data", "combined.csv")
db_path = os.path.join("C:/Users/shubh/Desktop/smart_toronto_traffic_dashboard/database", "traffic.db")

data = pd.read_csv(csv_path)

conn = sqlite3.connect(db_path)

data.to_sql("traffic_data", conn, if_exists="replace", index=False)

count = pd.read_sql("SELECT COUNT(*) AS total_rows FROM traffic_data", conn)
print(count)

conn.close()
print("✅ Data successfully loaded into traffic.db")
