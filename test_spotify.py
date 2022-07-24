import spotipy
import webplot
import requests
import json
from sqlalchemy import null
from credentials import spotify_credentials
from spotipy.oauth2 import SpotifyClientCredentials
CLIENT_ID = spotify_credentials.get('CLIENT_ID')
CLIENT_SECRET = spotify_credentials.get('CLIENT_SECRET')
auth_manager = SpotifyClientCredentials(client_id = CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

from spotify import NewQuery

def test_init():
    
    link = 'https://open.spotify.com/track/3sOC0HXzXHE6tKqb1mvzEH?si=69bb969f1bef4525'

    q = NewQuery(link, genre='rnb')
    
    q.link
    #assert isinstance(q.link, str), "Please input valid url, uri"
    assert "spotify:track" in q.link or "spotify.com/track" or 'spotify:album', "Please use valid url or uri" 
        
def test_get_features():
    """
    Call to spotipy method audio_features.
    
    returns spotipy object
    """
    link = 'https://open.spotify.com/track/3sOC0HXzXHE6tKqb1mvzEH?si=69bb969f1bef4525'
    q = NewQuery(link, genre='rnb')
    
    output = q.query_song
    #assert isinstance(output, dict)

def test_make_features_dataframe():
        """
        Create dataframe of song features using track_id from songs dataframe
        returns new dataframe
        """
        link = 'https://open.spotify.com/track/3sOC0HXzXHE6tKqb1mvzEH?si=69bb969f1bef4525'
        q = NewQuery(link, genre='rnb')
        q.get_song_and_features()
        
        song_json, features_df, full_df = q.make_dataframes()
        parsed = json.loads(song_json)
        return parsed, features_df, full_df

def test_JSON_read(json_pkg):
    #assert isinstance(json_pkg, dict)
    return webplot.JSON_read(json_pkg)
    
def test_dataframe_read(dataframe):
    return webplot.DataFrame_read(dataframe)
    
def test_create_polar_chart(dataframe):
    return webplot.create_polar_chart(dataframe)

if __name__ == '__main__':
    #test_init()
    #test_get_features()
    json_pkg, features_df, full_df = test_make_features_dataframe()
    #test_df = test_dataframe_read(features_df)
    print(full_df.to_dict().get('name').get(0))
    try:
        pass
        test_create_polar_chart(full_df)
    except Exception as e:
        print('polar chart')