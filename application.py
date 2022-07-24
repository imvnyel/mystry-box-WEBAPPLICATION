from flask import Flask, render_template, request, Markup
import json
import pandas as pd
import song_library, webplot
import spotify_main as spotty
import playlist_predict as pp


app = Flask(import_name=__name__)

# Bring database online
full_db, playlist_ids, playlist_db, plist_features = song_library.db_init()

@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/results', methods=['POST'])
def my_form_post():
    """
    Takes in url or uri from user input and sends it
    to be processed in machine learning app
    Returns:
        str: string object 
    """
    
    filter_keys = {
        'display_keys': ['name', 'artists', 'popularity'],
        'feature_keys': ['danceability', 'energy', 'valence', 'acousticness', 'liveness'],
        'playlist_keys': ['name', 'description']
        }
    
    
    spotify_uri = request.form.get('s-link')
    
    # 1. Creating a new entry from customer query
    full_df = spotty.spotify_init(spotify_uri)
    
    # 2. Playlist Predict
    idx = pp.predict_playlist(full_df)
   
    # 3. Get dataframe of predicted playlist. Returns dataframe obj
    playlist_info = song_library.search_playlist(idx, playlist_ids, playlist_db)
 
    # 4. Get playlist average stats
    for item in idx:
        p_fe = [plist_features.loc[playlist_ids[i]] for i in item]
    
    p_features = pd.concat(p_fe)
    
    #full_playlist = playlist_info.join(p_features)
    
    # Visualise new user query with webplot custom module
    playlist_features = webplot.DataFrame_read(p_features) 
    features = webplot.DataFrame_read(full_df)
    
    all_feats = pd.concat([features, playlist_features])
    
    graphJSON = webplot.create_polar_chart(all_feats)
    #graphJSONbar = webplot.create_bar_chart(playlist_features)
    
    p_features = p_features[filter_keys.get('feature_keys')].multiply(100).astype(int)
    return render_template("results.html",
                           uri=full_df.to_dict(),
                           p_info=playlist_info.to_dict(), 
                           plist_feat = p_features.to_dict(),
                           filter_keys = filter_keys, 
                           graphJSON = Markup(graphJSON),
                           #graphJSON = graphJSON
                           )



if __name__ == '__main__':
    app.run(debug=True)