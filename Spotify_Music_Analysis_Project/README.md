# Professional Spotify Music Analysis Project

A comprehensive data analysis project demonstrating advanced SQL techniques, real-time API integration, and business intelligence for music streaming analytics.

## Project Overview

This project provides a complete end-to-end solution for analyzing Spotify music data using:

- **Real-time Data Collection**: Spotify Web API integration with OAuth authentication
- **Advanced Database Design**: SQLite schema with proper normalization and indexing
- **Professional SQL Analysis**: Complex queries, aggregations, and business intelligence
- **Production-Ready Code**: Error handling, logging, configuration management, and testing
- **Business Intelligence**: Actionable insights for music industry analysis

## Project Structure

```
Spotify_Music_Analysis_Project/
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── main.py                           # Main execution script
├── config.py                         # Configuration settings
├── .env.example                      # Environment variables template
│
├── src/                              # Source code
│   ├── data_collection/              # Data collection modules
│   │   ├── __init__.py
│   │   ├── spotify_api.py           # Spotify API integration
│   │   └── sample_data_generator.py # Sample data generation
│   ├── database/                     # Database modules
│   │   ├── __init__.py
│   │   ├── database_manager.py      # Database operations
│   │   └── schema.sql               # Database schema
│   ├── analysis/                     # Analysis modules
│   │   ├── __init__.py
│   │   ├── music_analyzer.py        # Music analysis functions
│   │   └── sql_queries.py           # SQL query definitions
│   ├── visualization/                # Visualization modules
│   │   ├── __init__.py
│   │   ├── plot_generator.py        # Plot generation
│   │   └── dashboard.py             # Dashboard creation
│   └── utils/                        # Utility modules
│       ├── __init__.py
│       ├── helpers.py               # Helper functions
│       └── logger.py                # Logging configuration
│
├── data/                             # Data directory
│   ├── raw/                          # Raw data files
│   ├── processed/                    # Processed data files
│   └── sample/                       # Sample data files
│
├── sql/                              # SQL scripts
│   ├── queries/                      # Analysis queries
│   └── schema/                       # Database schema files
│
├── reports/                          # Generated reports
│   ├── figures/                      # Generated plots
│   └── insights/                     # Analysis insights
│
├── tests/                            # Test files
│   ├── __init__.py
│   ├── test_data_collection.py
│   ├── test_analysis.py
│   └── test_database.py
│
└── docs/                             # Documentation
    ├── api_reference.md
    ├── database_schema.md
    └── analysis_guide.md
```

## Quick Start

### 1. Installation

```bash
# Clone or download the project
cd Spotify_Music_Analysis_Project

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Spotify API credentials
```

### 2. Configuration

Create a `.env` file with your Spotify API credentials:

```bash
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

### 3. Run the Analysis

```bash
# Run the complete analysis pipeline
python main.py

# Or run specific modules
python -m src.data_collection.spotify_api
python -m src.analysis.music_analyzer
python -m src.visualization.plot_generator
```

## Features

### Data Collection
- **Spotify Web API Integration** - Real-time music data collection
- **Sample Data Generation** - Comprehensive demo data for testing
- **Error Handling** - Robust error handling and fallback mechanisms
- **Rate Limiting** - Respectful API usage with proper delays

### Database Management
- **SQLite Database** - Lightweight, serverless database
- **Normalized Schema** - Proper database design with relationships
- **Indexing** - Optimized queries with proper indexing
- **Data Validation** - Input validation and data integrity checks

### Analysis Capabilities
- **Advanced SQL Queries** - Complex analytical queries with CTEs and window functions
- **Audio Feature Analysis** - Comprehensive analysis of musical characteristics
- **Genre Analysis** - Genre distribution and performance metrics
- **Artist Performance** - Artist popularity and track analysis
- **Trend Identification** - Pattern recognition and trend analysis

### Visualization
- **Professional Charts** - High-quality matplotlib/seaborn visualizations
- **Interactive Plots** - Engaging data visualizations
- **Statistical Plots** - Distribution and correlation analysis
- **Business Intelligence** - Dashboard-ready visualizations

## API Reference

### Data Collection Module

```python
from src.data_collection.spotify_api import SpotifyDataCollector

# Initialize collector
collector = SpotifyDataCollector()

# Collect data
tracks = collector.search_tracks('pop music', limit=50)
collector.save_to_database(tracks)
```

### Analysis Module

```python
from src.analysis.music_analyzer import MusicAnalyzer

# Initialize analyzer
analyzer = MusicAnalyzer()

# Perform analysis
insights = analyzer.generate_insights()
analyzer.export_results('reports/insights/')
```

### Database Module

```python
from src.database.database_manager import DatabaseManager

# Initialize database
db = DatabaseManager('data/processed/spotify_analysis.db')

# Execute queries
results = db.execute_query("SELECT * FROM tracks LIMIT 10")
```

## Configuration

The project uses a centralized configuration system in `config.py`:

- **Database Settings** - SQLite database configuration
- **API Settings** - Spotify API configuration
- **Analysis Settings** - Analysis parameters and thresholds
- **Visualization Settings** - Plot styling and formatting

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test modules
python -m pytest tests/test_data_collection.py
python -m pytest tests/test_analysis.py
python -m pytest tests/test_database.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Spotify for providing the Web API
- The open-source community for excellent Python libraries
- Data science community for inspiration and best practices
