import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Put your credentials directly here (replace with your real values)
CLIENT_ID = "d75f06dbcc9d42d88cfa6c9a356b87f7"
CLIENT_SECRET = "79ad2a4f67994eeda0b00104d062a950"
REDIRECT_URI = "http://127.0.0.1:8888/callback"

try:
    # Create Spotify client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-read-recently-played user-top-read"
    ))
    
    # Test connection
    user = sp.current_user()
    print(f"Success! Connected as: {user['display_name']}")
    
    # Get top tracks
    top_tracks = sp.current_user_top_tracks(limit=5)
    print(f"Found {len(top_tracks['items'])} top tracks")
    
except Exception as e:
    print(f"Error: {e}")
