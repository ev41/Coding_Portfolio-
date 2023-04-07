#These are the libraries you need to import in order to run this code. 'os' is for finding 
    #secret local variables that I don't want you know. Spotipy is the library I use for functions
    #in this code. The oauth library is for accessing spotify's API. 
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth




# Set up authentication flow so I can access spotify's API.
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.environ.get('spotify_client_id'),
        client_secret=os.environ.get('spotify_secret_client_id'),
        redirect_uri='http://localhost:8000/callback/',
        scope='playlist-modify-public playlist-modify-private',
    )
)



# Ask user for a song and artist
song_name = input("Enter the name of a song: ")
artist_name = input("Enter the name of the artist: ")



# Search for the track ID for the user's selected song.
#search handles case insensitivity, so you don't have to use capital letters. 
search_results = sp.search(q=f"{song_name} artist:{artist_name}", type='track')
if len(search_results['tracks']['items']) == 0:
    print(f"No results found for {song_name} by {artist_name}")
    exit()
if song_name.lower() in search_results['tracks']['items'][0]['name'].lower() and artist_name.lower() in search_results['tracks']['items'][0]['artists'][0]['name'].lower():
    seed_track_id = search_results['tracks']['items'][0]['id']
else:
    print(f"No results found for {song_name} by {artist_name}")
    exit()

    
    
# Get a list of recommended tracks based on the user-provided seed track.
recs = sp.recommendations(seed_tracks=[seed_track_id])



# Create a new playlist and add n-number of recommended tracks to it.
#You can edit how many songs in the playlist you want under the track_ids variable. Where you see
    #20, just change the number to whatever you want.
user_id = sp.me()['id']
seed_track_name = sp.track(seed_track_id)['name']
playlist_name = 'My Recommended Songs'
playlist_desc = f'Algorithmically recommended songs based off: {seed_track_name}'
playlist = sp.user_playlist_create(user_id, playlist_name, public=False, description=playlist_desc)
track_ids = [recs['tracks'][i]['id'] for i in range(min(20, len(recs['tracks'])))]
sp.user_playlist_add_tracks(user_id, playlist['id'], track_ids)

print("All set! Check out your new playlist now!")
