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
df.to_csv('sample_spotify_data.csv', index=False)
print(f"Created sample_spotify_data.csv with {len(df)} tracks")
print("Sample data preview:")
print(df.head())
