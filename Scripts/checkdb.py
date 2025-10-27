import sqlite3
import pandas as pd

conn = sqlite3.connect("../database/traffic.db")
df = pd.read_sql("SELECT COUNT(*) AS total_rows FROM traffic_data", conn)
print(df)
conn.close()
