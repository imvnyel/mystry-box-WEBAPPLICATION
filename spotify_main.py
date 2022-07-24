#import spotify
#import spotifyclientcredentials

import spotipy
import pandas as pd
from credentials import spotify_credentials
from spotipy.oauth2 import SpotifyClientCredentials
CLIENT_ID = spotify_credentials.get('CLIENT_ID')
CLIENT_SECRET = spotify_credentials.get('CLIENT_SECRET')
auth_manager = SpotifyClientCredentials(client_id = CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)
     
    
def get_track_attr(temp_idx):
    """
    Search through dictionary key values and return list of track attributes
    """
    keys = ['id', 'uri', 'name', 'artists', 'popularity', 'album', 'preview_url']

    #assert temp_idx, 'None'
    temp_list = []
    temp_dict = {}    
    for key in keys:
        try:
            if key == 'artists':
                temp_value = [temp_idx[key][i]['name'] for i in range(len(temp_idx[key]))]
                temp_value = ', '.join(temp_value)         
            elif key == 'uri':
                temp_value = temp_idx[key]
                key = 'track_uri'
            elif key == 'album':
                temp_value = temp_idx[key]['images'][0].get('url')
                key = 'artwork_url'
            else:
                temp_value = temp_idx[key]
            

            temp_dict.update({key:temp_value})
        except Exception as e:
            print(e)
            pass
        
    temp_list.append(temp_dict)
    return temp_list
    
def get_song_and_features(link):
    """
    Call to spotipy method audio_features.
    
    returns spotipy object
    """
    try:
        temp_song_var  = sp.track(link)
        
        query_song = get_track_attr(temp_song_var)
        
        query_features = sp.audio_features(link)     
        
    except Exception as e:
        print(e)
        pass
    
    return query_song, query_features
    

    
def make_dataframes(song, features):
    """
    Make DataFrames of both song information and features and merge then at the end
    """
    columns_to_drop = ['type', 'uri', 'type', 'track_href']
    
    song_df = pd.DataFrame.from_dict(song).set_index('id')
    features_df = pd.DataFrame.from_dict(features).set_index('id') 
    
    complete_df = song_df.merge(features_df, left_on=song_df.index, right_on=features_df.index)
    complete_df = complete_df.drop(columns_to_drop, axis=1).reset_index()
            
    
    return complete_df

def spotify_init(spotify_uri):
    
    try:
        assert isinstance(spotify_uri, str), "Please input valid url, uri"
        assert "spotify:track" in spotify_uri or "spotify.com/track" \
        in spotify_uri or 'spotify:album' in spotify_uri, "Please use valid url or uri"
    except Exception as e:
        print('New Query')
    
    query_song, query_features = get_song_and_features(spotify_uri)
    full_df = make_dataframes(query_song, query_features)
    
    return full_df

def get_playlist_photo(playlist_id):

    return sp.playlist_cover_image(playlist_id)[0].get('url')
    
if __name__ == '__main__':
    spotify_uri = 'https://open.spotify.com/track/7MouZmAL2n18HGV4XhwN30?si=e592226ebd0e4b17'
    d = spotify_init(spotify_uri)
    print(d.head(1))