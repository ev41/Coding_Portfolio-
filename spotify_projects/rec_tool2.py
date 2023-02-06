"""
this code is based off my original idea of creating a spotify recommendation tool. However, whereas before I was trying to pull songs from a playlist and use all of them to create
a recommended playlist, I just realized that this is so inefficient. What I should do instead is extract / supply my code with a spotify song ID or uri (whatever info is
is accessible to the user on the front end application and can easily be copy and pasted into this code without requiring any additional code extraction), and using that one
song to create a playlist of 50 songs. This will use significantly less RAM because I'm not parsing large playlists anymore. I'm simply using one song as my training data.

"""

import os
import requests
import json
import pandas
import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
print("\n\n\n\n\n\n\n\n")

# setting relevent variables
client_id = os.getenv('spotify_client_id')
secret_client_id = os.getenv('spotify_secret_client_id')
username = os.getenv('spot_user')
rec_token = 'BQCNRDPv6mpactfyh45gLBmsvAm8afkJwgLNXR38ujRrdNISpaMJjQyHisn2VDDAMVGf6FJfbJVl3kSK6Lir8BoprgtBQSkASd3MPR5mCfL2ACREBrDwjjpsnG5acpCH78xd-6fknt-NJfbAEx1rCPaAv0HQdwvoUryURCZXO9psTq7Z8nlwS7v9K5FoaImZzvSuKYHDOhtpoA'


redirect_uri = "http://localhost/"
scope = "playlist-read-private playlist-modify-public playlist-modify-private playlist-read-collaborative user-read-recently-played user-top-read user-library-modify user-library-read"
# credentials = SpotifyClientCredentials(
# client_id=client_id, 
# client_secret=secret_client_id)

auth_url = 'https://accounts.spotify.com/api/token'
base_url = 'https://api.spotify.com/v1/'

#insert song id from song URI from spotify
#currently, this id is for paper paper, by marc e bassy
ref_track_id = '534E31ZNm91ErM7hmBWEW4?si=d7baa10dad8042af'

#lines 36 - 43 is us passing an access token and saving the response
auth_response = requests.post (auth_url, {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': secret_client_id,
} )

auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']

# #get request format for the api server w/ access token in the header 
headers = {
    "Content-Type": "application/json",
    'Authorization': 'Bearer {token}'.format(token=access_token),
}

#creating the actual GET request for audio features
r = requests.get(base_url + 'audio-features/' + ref_track_id, headers = headers)
r = r.json()
# print(r)

# getting the name of the song so I can use it in the new playlist's title
song = requests.get(base_url + 'tracks/' + ref_track_id, headers=headers)
song = song.json()
song_name = song['name']


# print(r['danceability'])

#creating new playlist

endpoint_url = 'https://api.spotify.com/v1/recommendations?'
limit = 5
seed_genres = 'indie'
seed_tracks = '534E31ZNm91ErM7hmBWEW4?si=d7baa10dad8042af'
mar='US'
t_da = r['danceability']
t_a = r['acousticness']
t_dur = r['duration_ms']
t_ene = r['energy']
t_inst = r['instrumentalness']
t_live = r['liveness']
t_loud = r['loudness']
t_spe = r['speechiness']
t_temp = r['tempo']
t_val = r['valence']


query = f'{endpoint_url}limit={limit}&market={mar}&seed_genres={seed_genres}&target_danceability={t_da}'
query += f'&seed_tracks={seed_tracks}'

response = requests.get(query,
                        headers={"Content-Type": "application/json",
                                 "Authorization": "Bearer BQABWgECNDKv72XNS5o_RN-fq2zz0KHPoVM0n34iaNCupIDYZZfIJ07s6Dk9ywYmUo8s7p-qnFWPEAojJQEHy8ywkWZRTDcn1-SOFK3xj24AMvyTqjvcSv6cNfrqc1upMjlIsSHBMoQDQKDgscuKSdAHWMqKiISXN82GPvhjCLB2z9keXs2zFmCnTE9S0wAfRoOwp9XaFzpUXA"})


# &target_duration_ms = &target_danceability={t_da}&target_acousticness={t_a}{t_dur} & target_energy = {t_ene} & target_instrumentalness = {t_inst} & target_liveness = {t_live} & target_tempo = {t_temp}


json_response = response.json()
print(json_response)

# for i in json_response['tracks']:
#     print(f"\"{i['name']}\" by {i['artists'][0]['name']}")











# #creating the csv
# header = ['artist', 'song_name', 'release_date', 'popularity']

# with open('song_info', 'w', newline='') as f:
#     writer = csv.writer(f)

#     writer.writerow(header)
#     writer.writerows(relevant_song_info)

