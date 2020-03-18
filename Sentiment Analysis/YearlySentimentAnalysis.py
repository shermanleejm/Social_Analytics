import pandas as pd 
import json
import numpy as np 
import matplotlib.pyplot as plt 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

'''
The Positive, Negative and Neutral scores represent the proportion of text that falls in these categories. 
This means our sentence was rated as 67% Positive, 33% Neutral and 0% Negative. Hence all these should add up to 1.
The Compound score is a metric that calculates the sum of all the lexicon ratings 
which have been normalized between -1(most extreme negative) and +1 (most extreme positive).
'''
def getScore(sentence): # return dict, e.g. --> {'neg': 0.0, 'neu': 0.326, 'pos': 0.674, 'compound': 0.7351}
    analyser = SentimentIntensityAnalyzer()
    return analyser.polarity_scores(sentence)

keywords = []
with open("./Sentiment Analysis/keywords.txt", "r") as f:
    for line in f:
        line = line.strip()
        keywords.append(line)

keywordsRegex = "|".join(keywords)

df = pd.read_json("./Sentiment Analysis/data69.json")

years = []

for i in range(2014, 2021):
    years.append(i)

dfYears = {} # dict of dataframes of each year

for year in years:
    year_str = "-" + str(year)
    temp = df[df["timestamp"].str.contains(year_str)]
    dfYears[year] = temp

dfYearsWithRelevantKeywords = {}

# General sentiments regarding nus, ntu, smu

smuByYear = {}
ntuByYear = {}
nusByYear = {}

# SMU
def compoundScoreByYear(regex): # list
    scores = []
    for year in dfYears.keys():
        uniYear = dfYears[year]
        listOfComments = uniYear[uniYear["message"].str.contains(regex, case=False)]["message"].values.tolist()
        score = 0
        numOfComments = len(listOfComments)
        for comment in listOfComments:
            score += getScore(comment)["compound"]
        overallScore = score / numOfComments
        string = f"{year},{overallScore}\n"
        scores.append(string)
    return scores
    # for msg in dfInQuestion[dfInQuestion["message"].contains(keywordsRegex)]:

def cScorePolyUni(poly, uni):
    scores = []
    for year in dfYears.keys():
        uniYear = dfYears[year]
        listOfComments = uniYear[uniYear["message"].str.contains(poly, case=False) & uniYear["message"].str.contains(uni, case=False)]["message"].values.tolist()
        score = 0
        numOfComments = len(listOfComments)
        if numOfComments == 0:
            numOfComments = 1
        for comment in listOfComments:
            score += getScore(comment)["compound"]
        overallScore = score / numOfComments
        string = f"{year},{overallScore}\n"
        scores.append(string)
    return scores

def writeToFileBasic(name):
    smuf = open(f"./data/{name}.txt", "w+")
    for thing in compoundScoreByYear(name):
        smuf.write(thing)
    smuf.close()
    print(f"Finished {name}")

def writeToFileTwoKeywords(poly, uni, name):
    smuf = open(f"{name}.txt", "w+")
    for thing in cScorePolyUni(poly, uni):
        smuf.write(thing)
    smuf.close()
    print(f"Finished {name}")

def textToArray(filePath) :
    raw = []
    with open(filePath, "r") as f:
        for line in f:
            raw.append(line.strip())
    
    # output = []
    # for school in raw:
    #     acronym = ""
    #     shortForm = ""
    #     for word in school.split(" "):
    #         if word.lower() not in ["junior", "college", "polytechnic"]:
    #             shortForm += word + " "
    #         acronym += word[0]
    #     output.append( [school, shortForm[:-1], acronym] )
    # return output
        

tertiary = textToArray("./Sentiment Analysis/polyjc.txt")

# print (tertiary)

postTertiary = [
    ["Singapore Management University", "smu"],
    ["nanyang technological university", "ntu"],
    ["National University of Singapore", "nus"]
]

def listToRegex(arr) :
    return "|".join(arr)

def tertiaryToPostTertiary(tertiary, postTertiary):
    count = 1
    for uni in postTertiary:
        uniRegex = listToRegex(uni)
        for polyJC in tertiary:
            polyJCRegex = listToRegex(polyJC)
            name = uni[-1] + " " + polyJC[-1]
            writeToFilePolyUni(polyJCRegex, uniRegex, name)
            print (f"done {count} pair")
            count += 1

# tertiaryToPostTertiary(tertiary, postTertiary)

with open("./Sentiment Analysis/keywords.txt", "r") as f:
    for line in f:
        word = line.strip()
        for uni in postTertiary:
            uniName = uni[1]
            filename = "./keyworduni/" + uniName + " " + word
            uniRegex = listToRegex(uni)
            writeToFileTwoKeywords(word, uniRegex, filename)

# print (smuByYear[2018][1:3])