from sqlalchemy import text, create_engine, inspect
from credentials import postgres_credentials
import pandas as pd
import spotify_main as spotty


HOST = postgres_credentials.get('HOST')
USERNAME = postgres_credentials.get('USERNAME')
PASSWORD = postgres_credentials.get('PASSWORD')
PORT = postgres_credentials.get('PORT')
DB = postgres_credentials.get('DB')

# Initialize database connection
conn_string = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}'
        
# Create sql engine
engine = create_engine(conn_string, echo=False, encoding='latin1')

def read_database(table_name):
    """
    Reads open postgres databases into a pandas document

    Args:
        table_name (SQL table): RDBS Table from postgres

    Returns:
        DataFrame: DataFrame containing database values
    """
    try:
        return pd.read_sql_table(table_name, engine) 
    except Exception as e:
        return f'{e}'
 
def join_tables(song_df, features_df):
    
    # Sets the indexes of song and features dataframes
    song_df.set_index('track_id', inplace=True)
    features_df.set_index('id', inplace=True)
    
    # merge dataframes into a complete dataframe for easier manipulation
    song_feat_df = song_df.merge(features_df, left_on=song_df.index, right_on=features_df.index)
    song_feat_df = song_feat_df.drop_duplicates()
    
    song_feat_df.rename(mapper={'key_0': 'id'}, inplace=True)
    
    plist_features = song_feat_df.groupby('playlist_id').mean()
    
    return song_feat_df, plist_features
    
def get_unique_playlists(df):
    """
    Returns a list of unique playlist_ids from main datafame

    Args:
        df (DataFrame): Full DataFrame song_df merged on features_df

    Returns:
        list: unqiue playlist ids 
    """
    return list(df.playlist_id.unique())
    
def db_init():
    playlist_db = read_database('playlists')
    song_db = read_database('songs')
    feat_db = read_database('song_features')
    full_db, plist_features = join_tables(song_db, feat_db)
    target_list = get_unique_playlists(full_db)   

    return full_db, target_list, playlist_db, plist_features

def search_playlist(idx, target_list, playlist_df):
    """
        Searches playlist database for predicted database, returns a DataFrame
        and adds playlist cover art url to that DataFrame/
    Args:
        idx (int): index location of target playlist
        target_list (list): list of target playlists
        playlist_df (DataFrame): dataframe of playlist DB

    Returns:
        DataFrame: Pandas DataFrame of playlist info
    """
    #assert isinstance(idx, str) or isinstance(idx, int), 'idx value is either empty or incorrect datatype'
    assert target_list, 'No target values found in list'
    
    for i in range(len(idx)):
        selection = idx[i]
        playlist_found = [playlist_df.loc[playlist_df.id == target_list[index]] for index in selection]
            
    playlist_found = pd.concat(playlist_found)
    # Add image url to library
    try:
        playlist_found['image_url'] = playlist_found.id.apply(spotty.get_playlist_photo)
    except:
        playlist_found['image_url'] = 'https://i.scdn.co/image/ab6775700000ee8555c25988a6ac314394d3fbf5'
        return playlist_found.reset_index()
        
    return playlist_found.reset_index()
    
    
if __name__ == '__main__':
    full_db, target_list, playlist_db, plist_features = db_init()
    suggestion = search_playlist(8, target_list, playlist_db)
    print(suggestion)