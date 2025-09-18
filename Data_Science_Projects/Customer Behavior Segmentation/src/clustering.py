import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def main():
    rfm = pd.read_csv('data/rfm_table.csv', index_col=0)  # removed '../'
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm)
    kmeans = KMeans(n_clusters=4, random_state=42)
    rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)
    rfm.to_csv('data/rfm_clusters.csv')  # removed '../'
    print("Clustered RFM table saved to data/rfm_clusters.csv")

if __name__ == "__main__":
    main()