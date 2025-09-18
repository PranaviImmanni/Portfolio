import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_rfm_distribution(rfm):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    sns.histplot(rfm['Recency'], ax=axes[0], kde=True)
    axes[0].set_title('Recency Distribution')
    sns.histplot(rfm['Frequency'], ax=axes[1], kde=True)
    axes[1].set_title('Frequency Distribution')
    sns.histplot(rfm['Monetary'], ax=axes[2], kde=True)
    axes[2].set_title('Monetary Distribution')
    plt.tight_layout()
    plt.savefig('reports/figures/rfm_distribution.png')  # removed '../'
    plt.close()

def plot_clusters(rfm):
    plt.figure(figsize=(8,6))
    sns.scatterplot(x='Recency', y='Monetary', hue='Cluster', data=rfm, palette='tab10')
    plt.title('Customer Segments (Recency vs Monetary)')
    plt.savefig('reports/figures/clusters_plot.png')  # removed '../'
    plt.close()

def plot_segment_counts(rfm):
    plt.figure(figsize=(6,4))
    sns.countplot(x='Cluster', data=rfm, palette='tab10')
    plt.title('Customer Segment Counts')
    plt.savefig('reports/figures/customer_segments_chart.png')  # removed '../'
    plt.close()

def main():
    rfm = pd.read_csv('data/rfm_clusters.csv', index_col=0)  # removed '../'
    plot_rfm_distribution(rfm)
    plot_clusters(rfm)
    plot_segment_counts(rfm)
    print("Figures saved to reports/figures/")  # removed '../'

if __name__ == "__main__":
    main()