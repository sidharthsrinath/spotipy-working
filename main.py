
from analysis import *
from app import *

from flask import Flask, request, redirect, g, render_template
git remote add origin https://github.com/sidharthsrinath/spotipy-working.git

if __name__ == "__main__":

	#STEP 1: get playlist from input
	playlist_id = ""
	try:
		playlist_id = sys.argv[1]
	except IndexError:
		print("Incorrect number of arguments")
		sys.exit(0)

	#STEP 2: Authorization
	sp = authorize()

	#STEP 3: Data Extraction
	playlist_name, tracks, user, local_tracks = get_playlist(sp, playlist_id)
	userid = user['uri']
	print(userid)
	song_dict, head, names = song_information(sp, playlist_name, tracks, user)
	to_csv(song_dict,head,names)
	data_dir = os.path.join(os.getcwd(), names[1],names[0]+'.csv')


	#STEP 4: Data Prep
	df = read_df(data_dir)
	cluster_data, feats = prep(data_dir)

	#STEP 5: data clustering
	clusters = KMeansCluster(cluster_data, 2)


	creds = {
		'username' : userid, 
		'client_id' : os.environ['SPOTIPY_CLIENT_ID'],
		'client_secret' : os.environ['SPOTIPY_CLIENT_SECRET'],
		'redirect_uri' : 'https://www.google.com/'
	}

	#STEP 6: data plotting
	visualize(clusters, df, data_dir, creds, playlist_name)

	#STEP 7: creating playlists
	make_playlist(sp, userid, df, playlist_name)
	
	#STEP 7: delete cache
	delete_cache()