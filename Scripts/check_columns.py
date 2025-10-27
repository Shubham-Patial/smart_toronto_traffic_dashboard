import pandas as pd

df = pd.read_csv("C:/Users/shubh/Desktop/smart_toronto_traffic_dashboard/Data/combined.csv")
print("Columns in CSV:", df.columns.tolist())
print("\nFirst 5 rows:\n", df.head())
