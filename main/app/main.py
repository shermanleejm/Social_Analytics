import pandas as pd 
import json
import numpy as np 
import matplotlib.pyplot as plt 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
swords = set(stopwords.words('english'))
import csv

universities = [
    "Singapore Management University|smu",
    "Nanyang Technological University|ntu",
    "National University of Singapore|nus",
    "Singapore University of Technology and Design|sutd"
]

dataFolder = "./data/"
outputfile = "./output/"

keywords = []
with open(f"{dataFolder}keywords.txt", "r") as f:
    for line in f:
        keywords.append(line.strip())

infoSys = "information systems|it|information technology|data analytics|computer science|com|computer|info systems|info sys"
simplifiedInfoSys = "computer|com|infosys|information systems|analytics|smart city"
simplifiedJC = "rank|a-level|a level|"

poly = []
with open(f"{dataFolder}poly.txt", "r") as f:
    for line in f:
        poly.append(line.strip()) 

lowtier = []
with open(f"{dataFolder}lowTierJC.txt", "r") as f:
    for line in f:
        lowtier.append(line.strip()) 

midtier = []
with open(f"{dataFolder}midTierJC.txt", "r") as f:
    for line in f:
        midtier.append(line.strip()) 

hightier = []
with open(f"{dataFolder}highTierJC.txt", "r") as f:
    for line in f:
        hightier.append(line.strip()) 

df2 = pd.read_json(f"{dataFolder}hwz.json")
df1 = pd.read_json(f"{dataFolder}reddit.json")
df1["timestamp"] = df1["timestamp"].astype(str)
df1 = df1[df1["name"].str.contains("sneakpeek_bot") == False]
df = pd.concat([df2, df1])

'''
The Positive, Negative and Neutral scores represent the proportion of text that falls in these categories. 
This means our sentence was rated as 67% Positive, 33% Neutral and 0% Negative. Hence all these should add up to 1.
The Compound score is a metric that calculates the sum of all the lexicon ratings 
which have been normalized between -1(most extreme negative) and +1 (most extreme positive).
'''

def getScore(sentence): # return dict, e.g. --> {'neg': 0.0, 'neu': 0.326, 'pos': 0.674, 'compound': 0.7351}
    analyser = SentimentIntensityAnalyzer()
    return analyser.polarity_scores(sentence)

def writeFile(filepath, uni, startYear, endYear, terms, domain=""):
    df2 = pd.read_json(f"{dataFolder}hwz.json")
    df1 = pd.read_json(f"{dataFolder}reddit.json")
    df1["timestamp"] = df1["timestamp"].astype(str)
    df1 = df1[df1["name"].str.contains("sneakpeek_bot") == False]
    df = pd.concat([df2, df1])

    f = open(filepath, "w+", encoding='utf-8')
    headerArr = ["year", "search term", "sentiment score", "Number of comments", "Negative Comments", "Neutral Comments", "Positive Comments"]
    csvWriter = csv.writer(f)
    csvWriter.writerow(headerArr)

    for year in range(startYear, endYear + 1):

        dfYear = df[df["timestamp"].str.contains(str(year))]
        yearStr = str(year)

        for term in terms:

            if domain == "" :
                listOfComments = dfYear[ dfYear["message"].str.contains(term, case=False) & dfYear["message"].str.contains(uni, case=False)]["message"].values.tolist()
            else :
                listOfComments = dfYear[ dfYear["message"].str.contains(term, case=False) & dfYear["message"].str.contains(uni, case=False) & dfYear["message"].str.contains(domain, case=False)]["message"].values.tolist()

            score = 0
            numOfComments = len(listOfComments) 
            # negative means < -0.10
            # positive means > 0.10
            # neutral mean >= -0.10 and <= 0.10
            neg_count = 0
            pos_count = 0
            neu_count = 0

            for comment in listOfComments:
                temp_score = getScore(comment)["compound"]
                score += temp_score
                if temp_score < -0.10:
                    neg_count += 1
                elif temp_score > 0.10:
                    pos_count += 1
                else:
                    neu_count += 1

            overallScore = 0
            if numOfComments != 0:
                overallScore = score / numOfComments
            row = [year, term, overallScore, numOfComments, neg_count, neu_count, pos_count]
            csvWriter.writerow(row)
    f.close()

def printWeightiestSentences(filepath, uni, startYear, endYear, terms, numOfSentences, domain=""):
    if domain != "" :
        uni += "|" + domain

    f = open(filepath, "w+", encoding='utf-8')
    headerArr = ["year", "search term", "sentence", "score"]
    csvWriter = csv.writer(f)
    csvWriter.writerow(headerArr)

    for year in range(startYear, endYear + 1):
        
        df2 = pd.read_json(f"{dataFolder}hwz.json")
        df1 = pd.read_json(f"{dataFolder}reddit.json")
        df1["timestamp"] = df1["timestamp"].astype(str)
        df1 = df1[df1["name"].str.contains("sneakpeek_bot") == False]
        df = pd.concat([df2, df1])
        yearStr = str(year)
        dfYear = df[df["timestamp"].str.contains(yearStr)]

        for term in terms:

            if domain == "" :
                listOfComments = dfYear[ dfYear["message"].str.contains(term, case=False) & dfYear["message"].str.contains(uni, case=False)]["message"].values.tolist()
            else :
                listOfComments = dfYear[ dfYear["message"].str.contains(term, case=False) & dfYear["message"].str.contains(uni, case=False) & dfYear["message"].str.contains(domain, case=False)]["message"].values.tolist()

            vectorizer = TfidfVectorizer(stop_words=swords)

            if len(listOfComments) > 0:
                if numOfSentences > len(listOfComments):
                    num = len(listOfComments)
                else :
                    num = numOfSentences    

                X = vectorizer.fit_transform(listOfComments)

                feature_names = vectorizer.get_feature_names()

                vocab = vectorizer.vocabulary_

                unsorted_result = {}

                for i in range(len(list(X.toarray()))) :
                    row = list(list(X.toarray())[i])
                    unsorted_result[listOfComments[i]] = sum(row)
                
                result = pd.DataFrame()
                result["sentence"] = unsorted_result.keys()
                result["value"] = unsorted_result.values()
                df = result.sort_values(by=["value"], ascending=False)

                top10sentences = df.nlargest(num, "value")["sentence"].tolist()
                top10values = df.nlargest(num, "value")["value"].tolist()

                for i in range(num):
                    # line = str(year) + "," + uni + "," + term + ",\"" + top10sentences[i] + "\"," + str(top10values[i]) + "\n"
                    tempArr = [str(year), term, str(top10sentences[i]), top10values[i]]
                    csvWriter.writerow(tempArr)
            
            else :
                tempArr = [str(year), uni, term, "", 0]
                csvWriter.writerow(tempArr)
                
    f.close()

def display():
    searchTermRegex = input("Enter search term > ")
    noMoreSearchTerms = False
    while (not noMoreSearchTerms) :
        newTerm = input("Enter search term or F to finish > ")
        if newTerm not in "fF":
            searchTermRegex += "|" + newTerm
        else:
            noMoreSearchTerms = True
            print ()

    validInt = False
    start = input("Enter start year > ")
    while (not validInt) :
        try:
            start = int(start)
            validInt = True
            print ()
        except:
            start = input("Enter start year > ")

    validInt = False
    end = input("Enter end year > ")
    while (not validInt) :
        try:
            end = int(end)
            validInt = True
            print ()
        except:
            end = input("Enter end year > ")

    for i in range(len(universities)):
        print (f"{i + 1}. {universities[i].split('|')[0]}")
    print ()

    chosen_unis = []
    selected_unis = input("Enter the universities separated by \" \" > ")
    for num in selected_unis.strip().split(" "):
        chosen_unis.append(int(num) - 1)

    filename = searchTermRegex.replace("|", " ")
    if len(searchTermRegex) > 20:
        filename = searchTermRegex.split("|")[0]

    numberOfComments = int(input("\nEnter number of top comments to extract > "))
    print ()

    return filename, searchTermRegex, start, end, chosen_unis, numberOfComments

filename, searchRegex, start, end, chosen_unis, numberOfComments = display()
for i in chosen_unis:
    uni = universities[i]
    uniName = uni.split('|')[0]
    print (f"Calculating sentiment scores for {uniName} now...")

    sentimentPath = f"{outputfile}{uniName} - {filename} Sentiment Scores.csv"
    writeFile(sentimentPath, uni, start, end, [searchRegex], simplifiedInfoSys)

    print (f"Finished calculating sentiment scores for {uniName}.")
    print (f"Finding most meaningful sentences for {uniName} now...")

    weightedPath = f"{outputfile}{uniName} - {filename} Weighted Sentences.csv"
    printWeightiestSentences(weightedPath, uni, start, end, [searchRegex], numberOfComments, simplifiedInfoSys)

    print (f"Finished finding most meaningful sentences for {uniName}.")

print ("Please check output folder.")