import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title('Customer Segmentation Dashboard')

@st.cache_data
def load_data():
    return pd.read_csv('../data/rfm_clusters.csv', index_col=0)

df = load_data()

st.header('Segment Counts')
fig, ax = plt.subplots()
sns.countplot(x='Cluster', data=df, palette='tab10', ax=ax)
st.pyplot(fig)

clusters = df['Cluster'].unique()
selected = st.multiselect('Filter by Cluster', clusters, default=list(clusters))
filtered = df[df['Cluster'].isin(selected)]
st.write(filtered.head())
