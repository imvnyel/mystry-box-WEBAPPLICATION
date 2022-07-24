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

class NewQuery:
    
    def __init__(self, link, genre):
        try:
            assert isinstance(link, str), "Please input valid url, uri"
            assert "spotify:track" in link or "spotify.com/track" \
            in link or 'spotify:album' in link, "Please use valid url or uri"
        except Exception as e:
            print('New Query')
        
        self.link = link
        self.genre = genre
        self.query_song = {}
        self.query_features = {}
        self.song_df = []
        self.features_df = []
        self.analysis_url = ''
      
    
    def __get_track_attr(self, temp_idx):
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
    
    def get_song_and_features(self):
        """
        Call to spotipy method audio_features.
        
        returns spotipy object
        """
        try:
            temp_song_var  = sp.track(self.link)
           
            self.query_song = self.__get_track_attr(temp_song_var)
            
            self.query_features = sp.audio_features(self.link)
            
            
        except Exception as e:
            print('Song Features')
            print(e)
            pass
        
        return 'Song information and features downloaded'  
    

    
    def make_dataframes(self):
        """
        Make DataFrames of both song information and features and merge then at the end
        """
        columns_to_drop = ['type', 'uri', 'type', 'track_href']
        
        self.song_df = pd.DataFrame.from_dict(self.query_song).set_index('id')
        self.features_df = pd.DataFrame.from_dict(self.query_features).set_index('id') 
        
        self.complete_df = self.song_df.merge(self.features_df, left_on=self.song_df.index, right_on=self.features_df.index)
        self.complete_df = self.complete_df.drop(columns_to_drop, axis=1).reset_index()
        
        return self.complete_df