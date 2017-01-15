import requests
import os
import spotipy
import spotipy.util as sutil

def compareOldAndNew(current, update):
	to_remove = current
	to_add = []
	for uri in update:
		if uri not in current:
			to_add.append(uri)
		else:
			to_remove.remove(uri)
	return to_add, to_remove

def addNewTracks(playlist_id, track_uris):
	if len(track_uris) > 0:
		sp.user_playlist_add_tracks(username, playlist_id, track_uris)

def removeOldTracks(playlist_id, track_uris):
	if len(track_uris) > 0:
		sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, track_uris)

def getPlaylistId(term):

	def playlistExists(name):
		results = sp.user_playlists(username)
		playlists = results["items"]
		num_playlists = len(playlists)
		exists = False
		while num_playlists > 0:
			num_playlists -= 1
			playlist = playlists[num_playlists]
			if playlist["name"] == name:
				exists = True
				playlist_id = playlist["id"]
				break
		if not exists:
			playlist_id = createPlaylist(name, term)
		return playlist_id

	split_term = term.split("_", 1)
	pretty_term = " ".join(split_term).title()
	name = "Top Tracks: " + pretty_term
	playlist_id = playlistExists(name)
	return playlist_id

def createPlaylist(name, term):
	playlist_name = name
	new_playlist = sp.user_playlist_create(username, playlist_name)
	playlist_id = new_playlist["id"]
	return playlist_id

def getCurrentPlaylist(term):
	playlist_id = getPlaylistId(term)
	tracks = sp.user_playlist_tracks(username, playlist_id)
	track_uris = [track["track"]["uri"] for track in tracks["items"]]
	return playlist_id, track_uris

def getTopTracks(term):
    results = sp.current_user_top_tracks(limit=50, time_range=term)
    items = results['items']
    track_uris = [item['uri'] for item in items]
    return track_uris

scope = 'user-top-read playlist-modify-public'
username = os.getenv('SPOTIFY_USERNAME')
token = sutil.prompt_for_user_token(username, scope)

if token:
	sp = spotipy.Spotify(auth=token)
	time_ranges = ["short_term", "medium_term", "long_term"]
	for term in time_ranges:
		top_tracks = getTopTracks(term)
		current_playlist_id, current_playlist_tracks = getCurrentPlaylist(term)
		add, remove = compareOldAndNew(current_playlist_tracks, top_tracks)
		addNewTracks(current_playlist_id, add)
		removeOldTracks(current_playlist_id, remove)
else:
	    print("Can't authorize for " + username)