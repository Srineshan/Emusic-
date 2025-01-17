from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from myproject import settings

def get_spotify_search_results(query):
    # Set up the client credentials manager
    client_credentials_manager = SpotifyClientCredentials(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
    )
    
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Search for tracks on Spotify
    result = sp.search(q=query, type='track', limit=30)  # Adjust limit as needed
    tracks = result['tracks']['items']
    
    return tracks
