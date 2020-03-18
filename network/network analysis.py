import pandas as pd 
import sklearn 
import networkx as nx 
import numpy as np 
import json 

def getNetworkByYear(year):

    df = pd.read_json("./network/data69.json")    
    convo_df = df[df["message"].str.contains("wrote:") & df["timestamp"].str.contains(str(year))]

    network = {} 

    for index, row in convo_df.iterrows():
        recepient = row["message"].split(" wrote:")[0]
        if len(recepient) < 50:
            sender = row["name"]
            key = sender + "," + recepient
            if key not in network.keys():
                network[key] = 1
            else:
                network[key] += 1

    G = nx.Graph()

    for k, v in network.items():
        a = k.split(",")[0]
        b = k.split(",")[1]
        G.add_edge(a, b, weight=v)

    outputFileName = str(year) + ".gexf"

    nx.write_gexf(G, outputFileName)

for i in range(2014, 2021) :
    getNetworkByYear(i)