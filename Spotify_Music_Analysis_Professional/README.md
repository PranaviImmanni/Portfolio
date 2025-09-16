# 🎵 Professional Spotify Music Analysis Project

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![SQL](https://img.shields.io/badge/SQL-Advanced-green.svg)](https://sql.org)
[![Spotify API](https://img.shields.io/badge/Spotify-Web%20API-1DB954.svg)](https://developer.spotify.com)
[![Google Colab](https://img.shields.io/badge/Google-Colab-orange.svg)](https://colab.research.google.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive, enterprise-grade data analysis project demonstrating advanced SQL techniques, real-time API integration, and business intelligence for music streaming analytics. This project showcases professional data engineering skills perfect for demonstrating technical expertise to recruiters and data teams.

## 🎯 Project Overview

This project provides a complete end-to-end solution for analyzing Spotify music data using:

- **Real-time Data Collection**: Spotify Web API integration with OAuth authentication
- **Advanced Database Design**: SQLite schema with proper normalization and indexing
- **Professional SQL Analysis**: Complex queries, aggregations, and business intelligence
- **Production-Ready Code**: Error handling, logging, configuration management, and testing
- **Business Intelligence**: Actionable insights for music industry analysis

## 🚀 Quick Start

### Google Colab (Recommended)
1. Open the notebook in Google Colab: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/spotify-music-analysis)
2. Run all cells to see the complete analysis
3. Optionally add your Spotify API credentials for real data

### Local Development
```bash
# Clone the repository
git clone https://github.com/yourusername/spotify-music-analysis.git
cd spotify-music-analysis

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Spotify API credentials

# Run the analysis
python -m src.data_collection.spotify_collector
python -m src.analysis.music_analyzer
```

## 📊 Key Features

### Data Engineering
- **ETL Pipelines**: Automated data collection and transformation
- **API Integration**: Real-time Spotify Web API with rate limiting
- **Database Design**: Production-ready schema with constraints and triggers
- **Data Validation**: Comprehensive error handling and data quality checks

### Advanced Analytics
- **SQL Expertise**: Complex queries, aggregations, and window functions
- **Statistical Analysis**: Correlation analysis, trend identification
- **Business Intelligence**: Market potential assessment, competitive analysis
- **Performance Optimization**: Indexed queries and efficient data processing

### Professional Development
- **Code Quality**: Type hints, documentation, error handling
- **Configuration Management**: Environment-based settings
- **Logging & Monitoring**: Comprehensive audit trails
- **Testing Framework**: Unit tests and integration testing

## 🗄️ Database Architecture

### Core Tables
```sql
-- Artists with comprehensive metadata
CREATE TABLE artists (
    artist_id VARCHAR(50) PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL,
    genres TEXT,
    popularity INTEGER CHECK (popularity >= 0 AND popularity <= 100),
    followers_count INTEGER DEFAULT 0,
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
```

## 📈 Sample Analysis Results

### Top Artists by Performance
| Artist | Track Count | Avg Popularity | Characteristic |
|--------|-------------|----------------|----------------|
| Taylor Swift | 8 | 78.25 | Balanced |
| Ed Sheeran | 8 | 75.50 | Balanced |
| Olivia Rodrigo | 11 | 73.18 | Balanced |

### Genre Performance Analysis
| Genre | Track Count | Avg Popularity | Market Potential | Danceability Rank |
|-------|-------------|----------------|------------------|-------------------|
| Pop | 17 | 72.76 | High Potential | 3 |
| R&B | 6 | 71.00 | High Potential | 6 |
| Country | 21 | 67.43 | Growing Market | 5 |

## 🎯 Business Insights

### Market Opportunities
- **High Potential Genres**: Pop and R&B show strong market potential with >70% average popularity
- **Growth Markets**: Country and Hip-hop demonstrate growing market opportunities
- **Danceability Leaders**: Hip-hop leads in danceability, indicating strong party/club market potential

### Content Strategy
- **High Energy Focus**: Genres with high danceability and energy scores target party/club audiences
- **Acoustic Focus**: Genres with high acousticness target relaxation and study audiences
- **Positive Mood**: High valence genres target uplifting and motivational content

## 💼 Professional Value

This project demonstrates:

### Technical Skills
- **Data Engineering**: ETL pipelines, API integration, database design
- **Advanced SQL**: Complex queries, window functions, aggregations
- **Python Development**: Professional code structure, error handling, testing
- **Business Intelligence**: KPI development, dashboard creation, insights generation

### Industry Knowledge
- **Music Streaming Analytics**: Understanding of audio features and user behavior
- **Market Analysis**: Genre trends, artist performance, competitive landscape
- **Data-Driven Decision Making**: Evidence-based insights for business strategy

## 📁 Project Structure

```
spotify-music-analysis/
├── 📊 README.md                          # Project documentation
├── 📋 requirements.txt                   # Python dependencies
├── 📄 LICENSE                           # MIT License
├── ⚙️ .env.example                      # Environment variables template
│
├── 🗄️ config/                          # Configuration files
│   └── settings.py                      # Main configuration
│
├── 🐍 src/                              # Source code
│   ├── data_collection/                 # Data collection modules
│   │   └── spotify_collector.py        # Spotify API integration
│   ├── analysis/                        # Analysis modules
│   │   └── music_analyzer.py           # Music analysis functions
│   └── visualization/                   # Visualization modules
│       └── plot_generator.py           # Plot generation
│
├── 📓 notebooks/                        # Jupyter notebooks
│   └── Spotify_Music_Analysis_Colab.ipynb  # Google Colab notebook
│
├── 📁 data/                             # Data directory
│   ├── sample/                          # Sample data files
│   └── processed/                       # Processed data files
│
└── 📚 docs/                             # Documentation
    └── analysis_guide.md               # Analysis guide
```

## 🔧 Configuration

### Spotify API Setup
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy your Client ID and Client Secret
4. Add them to your environment variables

### Environment Variables
```bash
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

## 📊 Usage Examples

### Basic Analysis
```python
from src.analysis.music_analyzer import MusicAnalyzer

analyzer = MusicAnalyzer()
analyzer.load_data()
insights = analyzer.generate_insights()
```

### Data Collection
```python
from src.data_collection.spotify_collector import SpotifyDataCollector

collector = SpotifyDataCollector()
tracks = collector.search_tracks('pop music', limit=50)
collector.save_to_database(tracks)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Spotify for providing the Web API
- The open-source community for excellent Python libraries
- Data science community for inspiration and best practices

---

**⭐ If you found this project helpful, please give it a star!**

**🚀 Ready to analyze music data like a pro? Start with the Google Colab notebook!**
