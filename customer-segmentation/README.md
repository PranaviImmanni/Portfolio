# Customer Segmentation Project

## Project Overview
This project applies customer segmentation techniques to retail transaction data, enabling targeted marketing and business strategies. Using RFM (Recency, Frequency, Monetary) analysis and clustering algorithms, we identify distinct customer groups and provide actionable business insights.

## Objective
- Segment customers based on purchasing behavior
- Uncover actionable insights for marketing and retention
- Demonstrate end-to-end data science workflow: data cleaning, analysis, modeling, visualization, and reporting

## Tools Used
- Python (pandas, numpy, scikit-learn, matplotlib, seaborn)
- Jupyter Notebook
- Streamlit (optional, for dashboard)

## How to Run the Code
1. Place your raw dataset (e.g., `online_retail_II.csv`) in the `data/` folder as `raw_data.csv`.
2. Run the scripts in `/src/` for data cleaning, RFM analysis, clustering, and visualizations.
3. Explore the analysis in the Jupyter notebook: `notebooks/segmentation_analysis.ipynb`.
4. (Optional) Launch the dashboard:
   ```bash
   streamlit run dashboard/streamlit_app.py
   ```
5. Review the executive summary in `/reports/segmentation_summary.pdf` and visualizations in `/reports/figures/`.

## Key Business Insights
- Identify high-value, at-risk, and loyal customer segments
- Recommend targeted marketing strategies for each segment
- Visualize customer distribution and segment characteristics

---

## Directory Structure & File Descriptions

```
customer-segmentation/
├── README.md                # Project overview and instructions
├── data/
│   ├── raw_data.csv         # Original data (real or simulated)
│   └── cleaned_data.csv     # Data after preprocessing
├── notebooks/
│   └── segmentation_analysis.ipynb  # Walkthrough: RFM, clustering, viz, recommendations
├── src/
│   ├── data_cleaning.py     # Load, clean, format raw data
│   ├── rfm_analysis.py      # Score customers (R, F, M)
│   ├── clustering.py        # KMeans or other clustering
│   └── visualizations.py    # Charts/plots
├── reports/
│   ├── segmentation_summary.pdf     # Executive summary (1-pager or slides)
│   └── figures/
│       ├── rfm_distribution.png
│       ├── clusters_plot.png
│       └── customer_segments_chart.png
├── dashboard/ (optional)
│   └── streamlit_app.py     # Interactive dashboard
├── requirements.txt         # Python dependencies
└── .gitignore               # Ignore patterns
```
