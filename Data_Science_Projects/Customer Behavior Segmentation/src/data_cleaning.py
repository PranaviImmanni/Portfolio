import pandas as pd

def load_data(path):
    return pd.read_csv(path)

def clean_data(df):
    df = df.drop_duplicates()
    df = df.dropna(subset=['Customer ID'])
    return df

def save_data(df, path):
    df.to_csv(path, index=False)

if __name__ == "__main__":
    raw_path = "data/raw_data.csv"
    cleaned_path = "data/cleaned_data.csv"
    df = load_data(raw_path)
    df_clean = clean_data(df)
    save_data(df_clean, cleaned_path)
    print(f"Cleaned data saved to {cleaned_path}")
