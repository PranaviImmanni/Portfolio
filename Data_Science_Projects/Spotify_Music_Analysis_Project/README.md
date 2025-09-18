# 🎵 Spotify Music Analysis Project

A comprehensive data analysis platform that demonstrates advanced SQL techniques, real-time API integration, and business intelligence for music streaming analytics. This project showcases professional data science skills through the analysis of Spotify music data using Python, SQLite, and machine learning.

## 📋 Project Overview

The Spotify Music Analysis Project is a complete end-to-end data analysis solution that:

- **Collects** real-time music data from Spotify's Web API
- **Stores** data in a professionally designed SQLite database
- **Analyzes** music patterns, trends, and characteristics using advanced SQL queries
- **Visualizes** insights through professional charts and dashboards
- **Generates** actionable business intelligence reports

## 🎯 What This Project Does

### 1. **Data Collection & Storage**
- Integrates with Spotify Web API to collect real-time music data
- Stores data in a normalized SQLite database with proper relationships
- Handles rate limiting, error recovery, and data validation
- Provides sample data generation for demonstration purposes

### 2. **Advanced Music Analysis**
- **Audio Feature Analysis**: Analyzes danceability, energy, valence, acousticness, and other musical characteristics
- **Genre Analysis**: Categorizes and analyzes music genres with performance metrics
- **Artist Performance**: Tracks artist popularity, track counts, and performance trends
- **Trend Identification**: Uses machine learning clustering to identify music patterns
- **Statistical Analysis**: Provides comprehensive statistical insights and correlations

### 3. **Professional Visualizations**
- Creates high-quality charts and graphs using matplotlib and seaborn
- Generates interactive dashboards for business intelligence
- Produces correlation heatmaps and distribution plots
- Exports publication-ready visualizations

### 4. **Business Intelligence**
- Generates actionable insights for music industry analysis
- Provides recommendations for music discovery and curation
- Identifies trends and patterns in music consumption
- Creates reports suitable for stakeholder presentations

## 🚀 Key Features

### **Technical Capabilities**
- **Real-time API Integration**: Spotify Web API with OAuth authentication
- **Advanced Database Design**: SQLite with proper normalization and indexing
- **Machine Learning**: K-means clustering for pattern recognition
- **Statistical Analysis**: Comprehensive correlation and trend analysis
- **Professional Code**: Error handling, logging, configuration management

### **Analysis Capabilities**
- **Audio Feature Analysis**: 11 different audio characteristics
- **Genre Categorization**: 10 major genre categories with sub-genres
- **Artist Performance Metrics**: Popularity, track counts, and trends
- **Tempo Analysis**: Categorization by speed (Slow/Medium/Fast)
- **Correlation Analysis**: Relationships between different audio features

### **Visualization Features**
- **Top Artists Charts**: Popularity and performance rankings
- **Genre Analysis Plots**: Energy vs Valence scatter plots
- **Audio Features Dashboard**: Comprehensive feature analysis
- **Correlation Heatmaps**: Feature relationship visualization
- **Tempo Distribution**: Track categorization by tempo

## 📊 Sample Analysis Results

The project analyzes music data to answer questions like:

- **Which artists are most popular?** - Top 10 artists by popularity score
- **What genres perform best?** - Genre analysis with energy and valence metrics
- **How do audio features correlate?** - Correlation matrix of musical characteristics
- **What tempo categories are most common?** - Distribution of slow, medium, and fast tracks
- **Which artists produce the most content?** - Track count analysis by artist

## 🛠️ Technology Stack

- **Python 3.8+** - Core programming language
- **SQLite** - Database management and storage
- **Spotify Web API** - Real-time music data collection
- **pandas** - Data manipulation and analysis
- **matplotlib/seaborn** - Data visualization
- **scikit-learn** - Machine learning and clustering
- **numpy** - Numerical computing
- **sqlite3** - Database operations

## 📁 Project Structure

```
Spotify_Music_Analysis_Project/
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── main.py                           # Main execution script
├── config.py                         # Configuration settings
├── env.example                       # Environment variables template
│
├── src/                              # Source code
│   ├── data_collection/              # Data collection modules
│   │   ├── spotify_api.py           # Spotify API integration
│   │   └── sample_data_generator.py # Sample data generation
│   ├── database/                     # Database modules
│   │   └── database_manager.py      # Database operations
│   ├── analysis/                     # Analysis modules
│   │   └── music_analyzer.py        # Music analysis functions
│   ├── visualization/                # Visualization modules
│   │   └── plot_generator.py        # Plot generation
│   └── utils/                        # Utility modules
│       ├── helpers.py               # Helper functions
│       └── logger.py                # Logging configuration
│
├── data/                             # Data directory
│   ├── raw/                          # Raw data files
│   ├── processed/                    # Processed data files
│   └── sample/                       # Sample data files
│
├── reports/                          # Generated reports
│   ├── figures/                      # Generated plots
│   └── insights/                     # Analysis insights
│
└── tests/                            # Test files
    └── test_basic.py                 # Unit tests
```

## 🚀 Quick Start

### 1. **Installation**
```bash
# Clone or download the project
cd Spotify_Music_Analysis_Project

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your Spotify API credentials
```

### 2. **Configuration**
Create a `.env` file with your Spotify API credentials:
```bash
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

### 3. **Run the Analysis**
```bash
# Run the complete analysis pipeline
python main.py

# Or run specific modules
python -m src.data_collection.sample_data_generator
python -m src.analysis.music_analyzer
python -m src.visualization.plot_generator
```

## 📈 What You'll Get

### **Data Analysis Results**
- **Database**: SQLite database with artists, albums, and tracks
- **Insights**: JSON file with key findings and recommendations
- **Statistics**: CSV files with detailed analysis results
- **Visualizations**: High-quality PNG plots and charts

### **Sample Outputs**
- Top 10 artists by popularity
- Genre analysis with energy and valence metrics
- Audio features correlation matrix
- Tempo distribution analysis
- Comprehensive dashboard with multiple visualizations

## 🔧 Customization

### **Analysis Parameters**
- Modify clustering parameters in `config.py`
- Adjust audio feature thresholds
- Change visualization styles and colors
- Customize genre categories

### **Data Collection**
- Add new Spotify API endpoints
- Implement additional data sources
- Modify sample data generation
- Add new analysis metrics

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
python -m pytest tests/

# Run specific test modules
python -m pytest tests/test_basic.py
```

## 📚 Use Cases

This project is perfect for:

- **Data Science Portfolios**: Demonstrates advanced analytical skills
- **Music Industry Analysis**: Business intelligence for music companies
- **Academic Research**: Music pattern analysis and trend identification
- **Learning Projects**: Understanding API integration and data analysis
- **Business Presentations**: Professional visualizations and insights

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Spotify for providing the Web API
- The open-source community for excellent Python libraries
- Data science community for inspiration and best practices

---

**Ready to analyze music data like a pro?** 🎵 Start with `python main.py` and explore the world of music analytics!
