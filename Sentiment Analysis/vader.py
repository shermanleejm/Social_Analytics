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

'''
The Positive, Negative and Neutral scores represent the proportion of text that falls in these categories. 
This means our sentence was rated as 67% Positive, 33% Neutral and 0% Negative. Hence all these should add up to 1.
The Compound score is a metric that calculates the sum of all the lexicon ratings 
which have been normalized between -1(most extreme negative) and +1 (most extreme positive).
'''