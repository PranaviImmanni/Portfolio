# SQL Music Analysis

![Spotify Banner](visualizations/genre_avg_energy.png)

## Table of Contents
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Reusable Metrics & CTEs](#reusable-metrics--ctes)
- [Setup & Usage](#setup--usage)
- [Visualizations](#visualizations)
- [Analysis Examples](#analysis-examples)
- [License](#license)

---

## Project Overview

**SQL Music Analysis** is a comprehensive data analysis project that leverages advanced SQL techniques to explore Spotify music data. The project demonstrates professional SQL skills including Common Table Expressions (CTEs), window functions, complex aggregations, and data cleaning techniques to uncover patterns in genres, artists, and audio features.

### Key Highlights:
- **Advanced SQL Techniques**: CTEs, window functions, complex joins, and aggregations
- **Data Cleaning & Preprocessing**: Comprehensive data validation and transformation
- **Feature Engineering**: Creation of derived metrics and categorical variables
- **Time-Series Analysis**: Trend analysis across decades and years
- **Statistical Analysis**: Correlation analysis, distribution analysis, and clustering

---

## Project Structure
```
sql-music-analysis/
├── sample_data/
│   └── high_popularity_spotify_data.csv
├── schema/
│   └── create_tables.sql
├── sql/
│   ├── data_cleaning.sql
│   ├── genre_analysis.sql
│   ├── artist_analysis.sql
│   ├── feature_trends.sql
│   └── exploratory_queries.sql
├── notebooks/
│   ├── spotify_analysis_notes.md
│   └── spotify_music_analysis.ipynb
├── visualizations/
│   ├── genre_avg_energy.png
│   └── artist_valence_comparison.png
├── README.md
├── LICENSE
└── .gitignore
```

---

## Features
- **Advanced SQL queries** with CTEs and window functions for music data analysis
- **Comprehensive data cleaning** with missing value handling and data validation
- **Genre analysis** with ranking systems and trend identification
- **Artist performance analysis** with diversity metrics and evolution tracking
- **Feature trend analysis** with correlation studies and distribution analysis
- **Exploratory queries** with advanced clustering and similarity analysis
- **Interactive Google Colab notebook** for Python-based analysis
- **Professional documentation** with clear code organization and comments

---

## Reusable Metrics & CTEs
This project demonstrates advanced SQL abstraction through reusable Common Table Expressions (CTEs) and derived metrics:

### Key CTEs:
- **`genre_stats`**: Reusable genre performance metrics
- **`artist_stats`**: Artist performance and diversity calculations
- **`yearly_feature_trends`**: Time-based feature analysis
- **`feature_clusters`**: Audio feature clustering logic
- **`genre_centroids`**: Genre similarity calculations

### Derived Metrics:
- **Composite Scores**: Overall track scoring combining multiple features
- **Popularity Categories**: Categorical classification of track popularity
- **Feature Clusters**: Automatic categorization based on audio characteristics
- **Similarity Distances**: Mathematical distance calculations between genres
- **Trend Indicators**: Year-over-year change calculations

Recruiters love to see this level of abstraction and modular SQL logic for consistency and maintainability.

---

## Setup & Usage
1. **Clone the repository**
2. **Set up your SQL database environment** (PostgreSQL, MySQL, or SQLite)
3. **Import the schema from** `schema/create_tables.sql`
4. **Load the sample data from** `sample_data/high_popularity_spotify_data.csv`
5. **Run data cleaning script**: `sql/data_cleaning.sql`
6. **Execute analysis scripts** from the `sql/` directory in order:
   - `genre_analysis.sql` - Genre performance and characteristics
   - `artist_analysis.sql` - Artist diversity and evolution
   - `feature_trends.sql` - Time-based feature analysis
   - `exploratory_queries.sql` - Advanced exploratory analysis
7. **Open the Colab notebook** in `notebooks/spotify_music_analysis.ipynb` for interactive exploration

---

## Visualizations

### Genre Average Energy
![Genre Average Energy](visualizations/genre_avg_energy.png)

### Artist Valence Comparison
![Artist Valence Comparison](visualizations/artist_valence_comparison.png)

---

## Analysis Examples

### Genre Analysis
- Genre performance rankings with multiple metrics
- Decade-based genre evolution analysis
- Subgenre characteristics and popularity
- Genre feature correlation analysis

### Artist Analysis
- Top artists by track count and performance metrics
- Artist evolution over time with trend analysis
- Collaboration vs. solo performance comparison
- Artist diversity and genre coverage analysis

### Feature Trends
- Yearly feature evolution with ranking systems
- Decade comparison with statistical measures
- Feature correlation analysis with strength indicators
- Popularity vs. feature relationship analysis

### Exploratory Queries
- Advanced track scoring with composite metrics
- Seasonal analysis by release timing
- Feature clustering with automatic categorization
- Cross-genre similarity analysis using mathematical distances

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

*Part of the Portfolio collection showcasing advanced SQL and data analysis skills.* 