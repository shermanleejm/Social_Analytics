from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
import pandas as pd 

rawData = open("./hwzScraper/data.json", "r")

data = json.load(rawData)
df = pd.read_json("./hwzScraper/data.json")

results = pd.DataFrame()

keywords = []
with open("./Sentiment Analysis/keywords.txt", "r") as f:
    for line in f:
        keywords.append(line.strip())
print (keywords)

for 

def scorer(sentence) :
    analyser = SentimentIntensityAnalyzer()
    return analyser.polarity_scores(sentence)

