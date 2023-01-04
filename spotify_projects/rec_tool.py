import os
import json
import pandas
import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
print("\n\n\n")

#setting relevent variables
client_id = os.getenv('spotify_client_id')
secret_client_id = os.getenv('spotify_secret_client_id')
username = os.getenv('spot_user')
uri = "http://localhost:8050/callback"
scope = "playlist-read-private playlist-modify-public playlist-modify-private playlist-read-collaborative user-read-recently-played user-top-read user-library-modify user-library-read"
credentials = SpotifyClientCredentials(client_id=client_id, client_secret=secret_client_id)
sp = spotipy.Spotify(client_credentials_manager=credentials)

# acquiring playlist data
good_playlist_id = "0N3sawfZEZ3hRgN40gjKlk?si=9605e95a486d460a"
playlist_data = sp.user_playlist_tracks(user=username, playlist_id=good_playlist_id, offset=0, limit = 200)
track_data = playlist_data['tracks']

#isolating relevant song data from corresponding playlist^^
parent_track_dicts = track_data['items']

parent_track_list = []
target_track_list = []

for i in parent_track_dicts:
    parent_track_list.append(i)

for i in parent_track_list:
    target_track_list.append(i['track'])

relevant_song_info = []


for i in target_track_list:
    artist = i['artists'][0]['name']
    song_name = i['name']
    song_release_date = i['album']['release_date']
    song_popularity = i['popularity']
    song_id = i['id']
    relevant_song_info.append((artist, song_name, song_release_date, song_popularity, song_id))


for i in relevant_song_info:
    feats = sp.audio_features(tracks=[i[4]])
    print(feats)









# #creating the csv
# header = ['artist', 'song_name', 'release_date', 'popularity']

# with open('song_info', 'w', newline='') as f:
#     writer = csv.writer(f)

#     writer.writerow(header)
#     writer.writerows(relevant_song_info)


# #spotipy functins to consider using

# #user_playlist_tracks(user=None, playlist_id=None,fields=None, limit=100, offset=0, market=None)
# #user_playlist_create(user, name, public=True, collaborative=False, description='')
# #user_playlist_add_tracks(user, playlist_id, tracks, position=None)
# #playlist_tracks(playlist_id, fields=None, limit=100, offset=0, market=None, additional_types=('track', 'episode'))
