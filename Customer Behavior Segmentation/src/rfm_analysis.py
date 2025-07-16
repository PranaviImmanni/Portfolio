import pandas as pd
import numpy as np
from datetime import datetime

def calculate_rfm(df):
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('Customer ID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'Invoice': 'nunique',           # <-- changed from 'InvoiceNo'
        'TotalSum': 'sum'
    })
    rfm.rename(columns={'InvoiceDate': 'Recency', 'Invoice': 'Frequency', 'TotalSum': 'Monetary'}, inplace=True)
    return rfm

def main():
    df = pd.read_csv('data/cleaned_data.csv')
    df['TotalSum'] = df['Quantity'] * df['Price']   # <-- changed from 'UnitPrice'
    rfm = calculate_rfm(df)
    rfm.to_csv('data/rfm_table.csv')
    print("RFM table saved to data/rfm_table.csv")

if __name__ == "__main__":
    main()