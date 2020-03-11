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
print (keywords)
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

def writeToFilePolyUni(poly, uni, name):
    smuf = open(f"./data/{name}.txt", "w+")
    for thing in cScorePolyUni(poly, uni):
        smuf.write(thing)
    smuf.close()
    print(f"Finished {name}")

tertiary = [
    ["Republic Polytechnic", "republic poly", "rp"],
    ["Singapore polytechnic", "singapore poly", "sp"],
    ["ngee ann polytechnic", "ngee ann poly", "np"],
    ["temasek polytechnic", "temasek poly", "tp"],
    ["nanyang polytechnic", "nanyang poly", "nyp"],
["Anderson Serangoon Junior College", "asr", "asrjc"],
["Anglo-Chinese Junior College", "ac", "acjc"],
["Catholic Junior College", "cj", "cjc"],
["Dunman High School", "dunman", "dhs"],
["Eunoia Junior College", "eunoia", "ejc"],
["Hwa Chong Junior College", "hwachong", "hcjc"],
["Innova Junior College", "ij", "ijc"],
["Jurong Junior College", "jjc", "jjc"],
["Jurong Pioneer Junior College", "jp", "jpjc"],
["Meridian Junior College", "mj", "mjc"],
["Nanyang Junior College", "ny", "nyjc"],
["National Junior College", "nj", "njc"],
["Raffles Junior College", "rj", "raffles", "rjc"],
["Saint Andrew's Junior College", "sa", "sajc"],
["St. Joseph's Institution", "sji"],
["Serangoon Junior College", "sr", "srjc"],
["Tampines Junior College", "tp", "tpjc"],
["Tampines Meridian Junior College", "tampines meridian", "tmjc"],
["Temasek Junior College", "Temasek", "tjc"],
["Victoria Junior College", "victoria", "vj", "vjc"],
["Yishun Innova Junior College", "yishun innova", "yijc"],
["Yishun Junior College", "yj", "yjc"]
]

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

tertiaryToPostTertiary(tertiary, postTertiary)

informationSystems = ["IS", "information systems", ""]



# print (smuByYear[2018][1:3])