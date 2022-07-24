import pandas as pd
import joblib
#from json import dump, load
import numpy as np


def open_model():
    # load the model
    try:
        model = joblib.load(open('models/model.pkl', 'rb'))
    except Exception as e:
        return f'Model failed to open: {e}'
 
    # load kmeans model
    try:
        kmeans = joblib.load(open('models/kmeans.pkl', 'rb'))
    except Exception as e:
        return f'Kmeans failed to open: {e}'
        
    # load the transformer
    try:
        transformer = joblib.load(open('models/scaler.pkl', 'rb'))
        
    except Exception as e:
        return f'Transformer failed to open: {e}'
    
    return transformer, model, kmeans

def drop_columns(dataframe):
    columns_to_drop = ['name', 'artists', 'track_uri', 'popularity',
                       'artwork_url', 'preview_url', 'uri', 'analysis_url', 'time_signature']
    
    features_list = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 
                     'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', ]
    
    dataframe = dataframe[features_list]
    return dataframe

def kmean_cluster(dataframe, kmeans):
    
    #assert dataframe, 'DataFrame cannot be empty'
    cluster = kmeans.predict(dataframe)[0]
    dataframe['cluster'] = cluster
    return dataframe
    
    
def transform_new_entry(df, transformer):
    
    return transformer.transform(df)


def predict_new_entry(df, model):
    possibilities = model.predict_proba(df)
    
    return possibilities

def predict_decipher(probs_list):
    """
    Used to find the most likely playlist you'd find your song on 

    Args:
        probs_list (list): probability values of prediction outcome
    """
    
    idx_list = []
    maxfeats = np.sort(probs_list, axis=1)[:,-2:]
    idx = np.argpartition(probs_list, -2,  axis=1)[:,-2:]
    
    
    
    #idx = np.argmax(probs_list[0])
    idx_list = [i for i in idx]
    #likelihoods = probs_list[0][idx]
    
    
    return idx_list


def predict_playlist(df):
    """
    - Opens saved transformer and model from file locations. 
    - predicts kmeans cluster value for onehotencode
    - Scales and OHE dataframe

    Args:
        df (_type_): _description_

    Returns:
        idx: index of max value in probs list
        likelihoods: list of probabilities of target
    """
    transformer, model, kmeans = open_model()
    df_c = drop_columns(df)
    df_kmeans = kmean_cluster(df_c, kmeans)
    transformered_df = transform_new_entry(df_kmeans, transformer)
    probs = predict_new_entry(transformered_df, model)
    idx = predict_decipher(probs)
    return idx