import sys
import spotipy
import spotipy.util as util
# from __future__ import print_function
import sys
import spotipy
import spotipy.util as util
from spotipy import SpotifyClientCredentials, util


client_id='393026174b4d48d49bd6e371412c8a59'
client_secret='80e439830b084c6da52058c955d0da2f'
redirect_uri='https://localhost/'
username = 'spotify:user:226bsgo33f4ltd5dqkc2slf6i'
scope = 'playlist-modify-public'

#Credentials to access the Spotify Music Data
manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=manager)

#Credentials to access to  the Spotify User's Playlist, Favorite Songs, etc. 
token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri) 
spotify = spotipy.Spotify(auth=token)


def make_playlist_final(username, client_id, client_secret, redirect_uri, df, playlist_name):
	
	hi_name = 'High Energy: ' + playlist_name
	lo_name = 'Low Energy: ' + playlist_name
	username = username.replace('spotify:user:','')
	
	high_energy = spotify.user_playlist_create(user=username,
											name=hi_name,
											description= 'High energy songs from' + playlist_name)
	print('Created High Energy Playlist')
	low_energy = spotify.user_playlist_create(user=username,
											name=lo_name, 
											description = 'Low energy songs from' + playlist_name)
	print('Created Low Energy Playlist')

	playlist_1 = df[df['KMeans']==0] #low energy
	playlist_2 = df[df['KMeans']==1] #high energy

	id0 = list(playlist_1['song_id']) #low energy
	id1 = list(playlist_2['song_id']) #high energy

	for x in id0:
		thisid = x
		thisidN = thisid.strip()
		spotify.user_playlist_add_tracks(user = username,playlist_id= low_energy['id'],tracks = [thisidN])
	print('Added Songs to Low Energy Playlist')
	for x in id1:
		thisid = x
		thisidN = thisid.strip()
		spotify.user_playlist_add_tracks(user = username,playlist_id= high_energy['id'],tracks = [thisidN])
	print('Added Songs to Low Energy Playlist')
