#!/usr/bin/env python3
"""
Professional Spotify Data Analysis Project Setup Script

This script automates the setup process for the Spotify data analysis project,
including environment configuration, database setup, and sample data generation.

Author: Data Analysis Team
Date: 2024
License: MIT
"""

import os
import sys
import subprocess
import sqlite3
import pandas as pd
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ is required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} is compatible")

def create_directories():
    """Create necessary directories."""
    print("📁 Creating project directories...")
    directories = [
        "data/sample",
        "data/processed", 
        "notebooks",
        "examples",
        "docs",
        "tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def install_dependencies():
    """Install Python dependencies."""
    print("📦 Installing dependencies...")
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        return False
    
    result = run_command("pip install -r requirements.txt", "Installing Python packages")
    return result is not None

def setup_environment():
    """Set up environment configuration."""
    print("⚙️ Setting up environment configuration...")
    
    if not os.path.exists(".env"):
        if os.path.exists("env.example"):
            run_command("cp env.example .env", "Creating .env file from template")
            print("📝 Please edit .env file with your Spotify API credentials")
        else:
            print("⚠️ No env.example found, creating basic .env template")
            with open(".env", "w") as f:
                f.write("""# Spotify API Configuration
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback

# Environment Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
""")
    else:
        print("✅ .env file already exists")

def create_sample_data():
    """Create sample data for demonstration."""
    print("📊 Creating sample data...")
    
    # Create sample data script
    sample_script = """
import pandas as pd
import random
from datetime import datetime, timedelta

# Create sample Spotify data
artists = ['Taylor Swift', 'Drake', 'Billie Eilish', 'The Weeknd', 'Ariana Grande', 
           'Ed Sheeran', 'Post Malone', 'Dua Lipa', 'Harry Styles', 'Olivia Rodrigo']

genres = ['pop', 'hip-hop', 'indie', 'r&b', 'rock', 'electronic', 'country']

sample_data = []
for i in range(100):
    track = {
        'track_id': f'track_{i:03d}',
        'track_name': f'Sample Track {i+1}',
        'artist_name': random.choice(artists),
        'genre': random.choice(genres),
        'popularity': random.randint(20, 100),
        'danceability': round(random.uniform(0.2, 0.9), 3),
        'energy': round(random.uniform(0.1, 0.9), 3),
        'valence': round(random.uniform(0.1, 0.9), 3),
        'acousticness': round(random.uniform(0.0, 0.8), 3),
        'instrumentalness': round(random.uniform(0.0, 0.7), 3),
        'liveness': round(random.uniform(0.0, 0.5), 3),
        'speechiness': round(random.uniform(0.0, 0.4), 3),
        'tempo': round(random.uniform(80, 180), 2),
        'duration_ms': random.randint(120000, 300000),
        'release_year': random.randint(2015, 2024)
    }
    sample_data.append(track)

df = pd.DataFrame(sample_data)
df.to_csv('data/sample/sample_spotify_data.csv', index=False)
print(f"Created sample_spotify_data.csv with {len(df)} tracks")
"""
    
    with open("examples/create_sample_data.py", "w") as f:
        f.write(sample_script)
    
    # Run the script
    result = run_command("python examples/create_sample_data.py", "Generating sample data")
    return result is not None

def setup_database():
    """Set up SQLite database with sample data."""
    print("🗄️ Setting up database...")
    
    try:
        # Create database connection
        conn = sqlite3.connect('data/processed/spotify_analysis.db')
        
        # Load sample data
        df = pd.read_csv('data/sample/sample_spotify_data.csv')
        df.to_sql('tracks', conn, if_exists='replace', index=False)
        
        # Create a simple artists table
        artists_df = df[['artist_name']].drop_duplicates()
        artists_df['artist_id'] = range(1, len(artists_df) + 1)
        artists_df.to_sql('artists', conn, if_exists='replace', index=False)
        
        conn.close()
        print("✅ Database setup completed")
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def run_tests():
    """Run basic tests to verify setup."""
    print("🧪 Running setup tests...")
    
    # Test database connection
    try:
        conn = sqlite3.connect('data/processed/spotify_analysis.db')
        result = pd.read_sql_query("SELECT COUNT(*) as track_count FROM tracks", conn)
        print(f"✅ Database test passed: {result['track_count'].iloc[0]} tracks found")
        conn.close()
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False
    
    # Test sample data
    if os.path.exists('data/sample/sample_spotify_data.csv'):
        df = pd.read_csv('data/sample/sample_spotify_data.csv')
        print(f"✅ Sample data test passed: {len(df)} tracks in sample data")
    else:
        print("❌ Sample data test failed: file not found")
        return False
    
    return True

def main():
    """Main setup function."""
    print("🎵 Professional Spotify Data Analysis Project Setup")
    print("=" * 60)
    
    # Check prerequisites
    check_python_version()
    
    # Setup steps
    create_directories()
    
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        sys.exit(1)
    
    setup_environment()
    
    if not create_sample_data():
        print("❌ Setup failed at sample data creation")
        sys.exit(1)
    
    if not setup_database():
        print("❌ Setup failed at database setup")
        sys.exit(1)
    
    if not run_tests():
        print("❌ Setup failed at testing")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your Spotify API credentials")
    print("2. Run: python examples/test_spotify.py")
    print("3. Run: python -c \"import sqlite3; import pandas as pd; conn = sqlite3.connect('data/processed/spotify_analysis.db'); result = pd.read_sql_query('SELECT * FROM tracks LIMIT 5', conn); print(result); conn.close()\"")
    print("\n🚀 Your professional Spotify analysis project is ready!")

if __name__ == "__main__":
    main()

