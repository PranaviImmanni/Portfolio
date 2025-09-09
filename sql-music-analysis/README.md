# 🎵 Professional Spotify Data Analysis Project (SQL)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![SQL](https://img.shields.io/badge/SQL-Advanced-green.svg)](https://sql.org)
[![Spotify API](https://img.shields.io/badge/Spotify-Web%20API-1DB954.svg)](https://developer.spotify.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive, enterprise-grade data analysis project demonstrating advanced SQL techniques, real-time API integration, and business intelligence for music streaming analytics. This project showcases professional data engineering skills perfect for demonstrating technical expertise to recruiters and data teams.

## 🎯 Project Overview

This project provides a complete end-to-end solution for analyzing Spotify music data using:

- **Real-time Data Collection**: Spotify Web API integration with OAuth authentication
- **Advanced Database Design**: PostgreSQL schema with proper normalization and indexing
- **Professional SQL Analysis**: CTEs, window functions, and complex business intelligence queries
- **Production-Ready Code**: Error handling, logging, configuration management, and testing
- **Business Intelligence**: Actionable insights for music industry analysis

## 🚀 Key Features

### Data Engineering
- **ETL Pipelines**: Automated data collection and transformation
- **API Integration**: Real-time Spotify Web API with rate limiting
- **Database Design**: Production-ready schema with constraints and triggers
- **Data Validation**: Comprehensive error handling and data quality checks

### Advanced Analytics
- **SQL Expertise**: CTEs, window functions, complex aggregations
- **Statistical Analysis**: Correlation analysis, trend identification
- **Business Intelligence**: Market potential assessment, competitive analysis
- **Performance Optimization**: Indexed queries and efficient data processing

### Professional Development
- **Code Quality**: Type hints, documentation, error handling
- **Configuration Management**: Environment-based settings
- **Logging & Monitoring**: Comprehensive audit trails
- **Testing Framework**: Unit tests and integration testing

## 📊 Business Value

### Market Analysis
- Genre popularity trends and market potential assessment
- Artist performance correlation with market factors
- Seasonal listening pattern analysis and user behavior insights

### Strategic Insights
- Content strategy recommendations based on audio features
- Artist development insights and collaboration impact analysis
- Optimal release timing and feature-based track categorization

### Competitive Intelligence
- Market saturation analysis by genre and artist
- Cross-genre listening behavior and user segmentation
- Real-time trend identification and growth opportunity assessment

## 🗄️ Database Architecture

### Core Tables
```sql
-- Artists with comprehensive metadata
CREATE TABLE artists (
    artist_id VARCHAR(50) PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL,
    genres TEXT[],
    popularity INTEGER CHECK (popularity >= 0 AND popularity <= 100),
    followers_count INTEGER DEFAULT 0,
    market VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tracks with full audio feature analysis
CREATE TABLE tracks (
    track_id VARCHAR(50) PRIMARY KEY,
    track_name VARCHAR(255) NOT NULL,
    artist_id VARCHAR(50) REFERENCES artists(artist_id),
    popularity INTEGER CHECK (popularity >= 0 AND popularity <= 100),
    danceability DECIMAL(3,2) CHECK (danceability >= 0.0 AND danceability <= 1.0),
    energy DECIMAL(3,2) CHECK (energy >= 0.0 AND energy <= 1.0),
    valence DECIMAL(3,2) CHECK (valence >= 0.0 AND valence <= 1.0),
    -- Additional audio features...
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Streaming history with user behavior
CREATE TABLE streaming_history (
    stream_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(50),
    track_id VARCHAR(50) REFERENCES tracks(track_id),
    played_at TIMESTAMP NOT NULL,
    ms_played INTEGER CHECK (ms_played > 0),
    context_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Performance Optimizations
- **Indexes**: Optimized for common query patterns
- **Constraints**: Data integrity and validation
- **Triggers**: Automated timestamp updates
- **Partitioning**: Efficient data management for large datasets

## 🔧 Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL 13+ (or SQLite for development)
- Spotify Developer Account

### 1. Environment Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd sql-music-analysis

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Spotify API Configuration
1. Create a [Spotify Developer Account](https://developer.spotify.com/dashboard)
2. Create a new app and get your credentials
3. Set up environment variables:

```bash
# Create .env file
cat > .env << 'EOF'
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
ENVIRONMENT=development
LOG_LEVEL=INFO
EOF
```

### 3. Database Setup

#### PostgreSQL (Production)
```bash
# Create database
createdb spotify_analysis

# Run schema
psql -d spotify_analysis -f schema/create_tables.sql
```

#### SQLite (Development)
```bash
# Schema will be created automatically
sqlite3 data/processed/spotify_analysis.db < schema/create_tables.sql
```

### 4. Data Collection
```bash
# Authenticate with Spotify
python src/data_collection/spotify_api.py

# Collect sample data (if needed)
python examples/create_sample_data.py
```

## 📈 Analysis Examples

### Advanced Genre Analysis with CTEs
```sql
WITH genre_performance AS (
    SELECT 
        unnest(artists.genres) AS genre,
        COUNT(DISTINCT tracks.track_id) AS track_count,
        AVG(tracks.popularity) AS avg_popularity,
        AVG(tracks.danceability) AS avg_danceability,
        AVG(tracks.energy) AS avg_energy
    FROM tracks
    JOIN artists ON tracks.artist_id = artists.artist_id
    GROUP BY unnest(artists.genres)
),
genre_rankings AS (
    SELECT 
        genre,
        track_count,
        ROUND(avg_popularity, 2) AS avg_popularity,
        RANK() OVER (ORDER BY avg_popularity DESC) AS popularity_rank,
        RANK() OVER (ORDER BY avg_danceability DESC) AS danceability_rank
    FROM genre_performance
)
SELECT 
    genre,
    track_count,
    avg_popularity,
    popularity_rank,
    danceability_rank,
    CASE 
        WHEN avg_popularity > 70 THEN 'High Potential'
        WHEN avg_popularity > 60 THEN 'Growing Market'
        ELSE 'Emerging Market'
    END AS market_potential
FROM genre_rankings
ORDER BY popularity_rank;
```

### Artist Evolution Analysis with Window Functions
```sql
WITH artist_yearly_stats AS (
    SELECT 
        artists.artist_name,
        EXTRACT(YEAR FROM tracks.release_date) AS release_year,
        COUNT(tracks.track_id) AS tracks_released,
        AVG(tracks.popularity) AS avg_popularity,
        LAG(AVG(tracks.popularity)) OVER (
            PARTITION BY artists.artist_id 
            ORDER BY EXTRACT(YEAR FROM tracks.release_date)
        ) AS prev_year_popularity
    FROM tracks
    JOIN artists ON tracks.artist_id = artists.artist_id
    WHERE tracks.release_date IS NOT NULL
    GROUP BY artists.artist_id, artists.artist_name, EXTRACT(YEAR FROM tracks.release_date)
)
SELECT 
    artist_name,
    release_year,
    tracks_released,
    ROUND(avg_popularity, 2) AS avg_popularity,
    CASE 
        WHEN prev_year_popularity IS NOT NULL 
        THEN ROUND(avg_popularity - prev_year_popularity, 2)
        ELSE 0 
    END AS popularity_change,
    CASE 
        WHEN avg_popularity - prev_year_popularity > 5 THEN 'Rising Star'
        WHEN avg_popularity - prev_year_popularity > 0 THEN 'Growing'
        WHEN avg_popularity - prev_year_popularity > -5 THEN 'Stable'
        ELSE 'Declining'
    END AS trend_category
FROM artist_yearly_stats
ORDER BY artist_name, release_year DESC;
```

## 📁 Project Structure

```
sql-music-analysis/
├── 📊 README.md                          # Project documentation
├── 📋 requirements.txt                   # Python dependencies
├── 📄 LICENSE                           # MIT License
├── 🔧 .gitignore                        # Git ignore rules
├── ⚙️ .env.example                      # Environment variables template
│
├── 🗄️ schema/                          # Database schema
│   └── create_tables.sql                # PostgreSQL schema with indexes
│
├── 🐍 src/                              # Source code
│   ├── data_collection/                 # Data collection modules
│   │   ├── spotify_api.py              # Spotify API integration
│   │   └── data_loader.py              # Data loading utilities
│   ├── analysis/                        # Analysis modules
│   │   ├── genre_analysis.py           # Genre analysis functions
│   │   ├── artist_analysis.py          # Artist analysis functions
│   │   └── trend_analysis.py           # Trend analysis functions
│   └── visualization/                   # Visualization modules
│       ├── tableau_connector.py        # Tableau integration
│       └── powerbi_connector.py        # Power BI integration
│
├── 📊 sql/                              # SQL analysis scripts
│   ├── schema/                          # Database schema files
│   │   └── create_tables.sql           # Main schema
│   ├── analysis/                        # Analysis queries
│   │   ├── genre_analysis.sql          # Genre analysis queries
│   │   ├── artist_analysis.sql         # Artist analysis queries
│   │   └── trend_analysis.sql          # Trend analysis queries
│   └── maintenance/                     # Database maintenance
│       └── data_refresh.sql            # Data refresh procedures
│
├── 📓 notebooks/                        # Jupyter notebooks
│   ├── exploratory_analysis.ipynb      # Exploratory data analysis
│   └── model_development.ipynb         # ML model development
│
├── 📁 data/                             # Data directory
│   ├── sample/                          # Sample data files
│   │   └── sample_spotify_data.csv     # Sample dataset
│   └── processed/                       # Processed data files
│       ├── my_top_tracks.csv           # User top tracks
│       ├── recent_tracks.csv           # Recently played tracks
│       └── spotify_analysis.db         # SQLite database
│
├── 🎯 examples/                         # Example scripts
│   ├── test_spotify.py                 # API testing script
│   └── create_sample_data.py           # Sample data generator
│
├── 📚 docs/                             # Documentation
│   ├── api_reference.md                # API documentation
│   ├── database_schema.md              # Database documentation
│   └── analysis_guide.md               # Analysis guide
│
└── 🧪 tests/                            # Test files
    ├── test_data_collection.py         # Data collection tests
    ├── test_analysis.py                # Analysis tests
    └── test_database.py                # Database tests
```

## 🚀 Quick Start

### 1. Basic Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Spotify credentials

# Create sample data
python examples/create_sample_data.py
```

### 2. Run Analysis
```bash
# Test Spotify API connection
python examples/test_spotify.py

# Run genre analysis
python -c "
import sqlite3
import pandas as pd
conn = sqlite3.connect('data/processed/spotify_analysis.db')
result = pd.read_sql_query('SELECT * FROM tracks LIMIT 5', conn)
print(result)
conn.close()
"
```

### 3. Advanced Analysis
```bash
# Run comprehensive genre analysis
psql -d spotify_analysis -f sql/analysis/genre_analysis.sql

# Run artist performance analysis
psql -d spotify_analysis -f sql/analysis/artist_analysis.sql
```

## 📊 Sample Results

### Genre Performance Analysis
| Genre | Track Count | Avg Popularity | Market Potential | Danceability Rank |
|-------|-------------|----------------|------------------|-------------------|
| Pop | 17 | 72.76 | High Potential | 3 |
| R&B | 6 | 71.00 | High Potential | 6 |
| Country | 21 | 67.43 | Growing Market | 5 |
| Hip-hop | 10 | 66.60 | Growing Market | 1 |

### Top Artists by Performance
| Artist | Track Count | Avg Popularity | Characteristic |
|--------|-------------|----------------|----------------|
| Dua Lipa | 8 | 78.25 | Balanced |
| Ed Sheeran | 8 | 75.50 | Balanced |
| Olivia Rodrigo | 11 | 73.18 | Balanced |
| Taylor Swift | 14 | 71.43 | Balanced |

## 🎯 Business Insights

### Market Opportunities
- **High Potential Genres**: Pop and R&B show strong market potential with >70% average popularity
- **Growth Markets**: Country and Hip-hop demonstrate growing market opportunities
- **Danceability Leaders**: Hip-hop leads in danceability, indicating strong party/club market potential

### Content Strategy
- **High Energy Focus**: Genres with high danceability and energy scores target party/club audiences
- **Acoustic Focus**: Genres with high acousticness target relaxation and study audiences
- **Positive Mood**: High valence genres target uplifting and motivational content

### Artist Development
- **Balanced Artists**: Most successful artists maintain balanced audio feature profiles
- **Market Entry**: Genres with fewer artists present lower competition opportunities
- **Collaboration Impact**: Cross-genre collaborations can expand market reach

## 💼 Professional Value

This project demonstrates:

### Technical Skills
- **Data Engineering**: ETL pipelines, API integration, database design
- **Advanced SQL**: CTEs, window functions, complex aggregations
- **Python Development**: Professional code structure, error handling, testing
- **Business Intelligence**: KPI development, dashboard creation, insights generation

### Industry Knowledge
- **Music Streaming Analytics**: Understanding of audio features and user behavior
- **Market Analysis**: Genre trends, artist performance, competitive landscape
- **Data-Driven Decision Making**: Evidence-based insights for business strategy

### Production Readiness
- **Scalable Architecture**: Designed for enterprise deployment
- **Error Handling**: Comprehensive logging and error management
- **Configuration Management**: Environment-based settings and security
- **Documentation**: Professional documentation and code comments

## 🔒 Security & Privacy

- **OAuth 2.0**: Secure authentication with Spotify
- **Environment Variables**: Sensitive credentials stored securely
- **Data Privacy**: User data handling follows best practices
- **API Rate Limiting**: Respectful API usage with proper delays

