import plotly
import plotly.graph_objects as go
import json
import pandas as pd

def JSON_read(json_pkg):
    print(json_pkg.values())
    #df = pd.DataFrame.from_dict(json_pkg.values(), columns=json_pkg.keys())
    #temp_df = df[['danceability','energy','valence']] * 100
    #temp_df = temp_df + df.popularity
    
    #print(temp_df)
    
def DataFrame_read(dataframe):

    temp_df = dataframe[['danceability','energy','valence', 'acousticness', 'liveness']] * 100
    
    if 'name' in list(dataframe):
        temp_df[['popularity', 'title']] = dataframe[['popularity', 'name']]
        temp_df = temp_df.set_index('title')
    elif 'title' in list(dataframe):
        temp_df = temp_df.set_index('title') 
    else:
        pass
    
    
    
    temp_df_transposed = temp_df.T
    
    return temp_df_transposed

def create_polar_chart(dataframe):
    dictionary = dataframe.to_dict()

    fig = go.Figure()

    for title, values in dictionary.items():
        fig.add_trace(go.Scatterpolargl(
            name = title,
            r = list(values.values()),
            theta = list(values.keys()),
            r0 = [0,100],
            opacity=0.75
        ))

    fig.update_traces(fill='toself')

    fig.update_layout(
        polar = dict(bgcolor = "rgb(253, 253, 253)", 
                    radialaxis = dict(angle = 0, visible=False, range = [0,100], linecolor='black'),
        angularaxis = dict(direction = "clockwise", period = 4, linecolor='black')))

    graphJSON = fig.to_html()
    
    return graphJSON

def create_bar_chart(dataframe):
    dictionary = dataframe.to_dict()
    
    fig = go.Figure()
    bar_graphs = []
    print(dictionary.items())
    for title, values in dictionary.items():
        fig.add_trace(go.Bar(y = [title],
                             x=[values],
                             orientation='h'
                             ))
        
        graphJSON = fig.to_html()
        bar_graphs.append(graphJSON)
    return bar_graphs