import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import sklearn
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

from app import *
import os

# from retry import *

def read_df(filename):
    return pd.DataFrame(pd.read_csv(filename, sep = '∆', engine = 'python')) #data based on the csv file it reads

def prep(filename):
    data = read_df(filename)

    #features = ['danceability','energy','loudness','valence']
    features = ['danceability','energy','loudness','instrumentalness','valence','tempo']
    minmax = MinMaxScaler()

    x_data = minmax.fit_transform(data[features])

    return x_data, features

def KMeansCluster(data, k):
    
    clustering = KMeans(init = 'k-means++', n_clusters = k, verbose = 0 ,random_state= 15)
    clustering.fit(data)

    #print(clustering.labels_)
    return clustering

def visualize(clusters, df,data_dir, creds, playlist_name):
    df['KMeans'] = clusters.labels_

    print(df.groupby(['KMeans']).mean())

    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')

    x = [df['energy']]
    y = [df['danceability']]
    z = [df['loudness']]

    ax.scatter(x,y,z, c=df['KMeans'], marker = 'o')

    ax.set_xlabel('energy')
    ax.set_ylabel('danceablity')
    ax.set_zlabel('loudness')

    
    path = os.path.dirname(data_dir)
    plt.savefig(os.path.join(path,'pltfig.png'))
    plt.show()
    

    make_playlist_final(creds['username'],
                creds['client_id'],
                creds['client_secret'],
                creds['redirect_uri'],
                df, 
                playlist_name)

