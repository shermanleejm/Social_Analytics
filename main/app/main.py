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

    valid_choice = False

    while (not valid_choice) :
        search_term_choice = input("Would you like to use the keywords [f]ile or [m]anually input keywords > ")
        if search_term_choice in "mM":
            searchTermRegex = input("Enter search term > ")
            noMoreSearchTerms = False
            while (not noMoreSearchTerms) :
                newTerm = input("Enter search term or F to finish > ")
                if newTerm not in "fF":
                    searchTermRegex += "|" + newTerm
                else:
                    noMoreSearchTerms = True
                    print ()
            filename = searchTermRegex.replace("|", " ")
            if len(searchTermRegex) > 20:
                filename = searchTermRegex.split("|")[0]
            searchTermRegex = [searchTermRegex]
            valid_choice = True

        elif search_term_choice in "fF" :
            keywords_file = input("Enter file name in data folder > ")
            searchTermRegex = []
            with open(f"{dataFolder}{keywords_file}.txt", "r", encoding='utf-8') as f:
                for line in f:
                    searchTermRegex.append(line.strip()) 
            filename = keywords_file

            valid_choice = True

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

    

    numberOfComments = int(input("\nEnter number of top comments to extract > "))
    print ()

    return filename, searchTermRegex, start, end, chosen_unis, numberOfComments

def printNegNeuPos(filepath, uni, startYear, endYear, terms, numOfSentences, domain=""):
    numOfSentences = numOfSentences // 2

    if domain != "" :
        uni += "|" + domain

    f = open(filepath, "w+")

    csvWriter = csv.writer(f)

    headerArr = ["year", "term", "score", "sentence"]
    csvWriter.writerow(headerArr)

    for year in range(startYear, endYear + 1):
        df = pd.read_json(f"{dataFolder}hwz.json")
        # df2 = pd.read_json("../data/data71.json")
        # df1["timestamp"] = df1["timestamp"].astype(str)
        df = df[df["name"].str.contains("sneakpeek_bot") == False]
        # df = pd.concat([df1, df2])

        yearStr = str(year)
        dfYear = df[df["timestamp"].str.contains(yearStr)]

        pos = {}
        neg = {}
        neu = {} 

        for term in terms:

            if domain == "" :
                listOfComments = dfYear[ dfYear["message"].str.contains(term, case=False) & dfYear["message"].str.contains(uni, case=False)]["message"].values.tolist()
            else :
                listOfComments = dfYear[ dfYear["message"].str.contains(term, case=False) & dfYear["message"].str.contains(uni, case=False) & dfYear["message"].str.contains(domain, case=False)]["message"].values.tolist()

            sentimentDict = {}

            if len(listOfComments) > 0:
                for comment in listOfComments:
                    comment_sentiment_score = getScore(comment)["compound"]
                    sentimentDict[comment] = comment_sentiment_score
                
                sorted_sent_arr = sorted(sentimentDict.items(), key = lambda kv: kv[1])

                result = sorted_sent_arr[0:numOfSentences] + sorted_sent_arr[-numOfSentences:]

                for row in result:
                    csvWriter.writerow([year, term, row[1], row[0]])

            else:
                csvWriter.writerow([year, term, ""])
            
                
    f.close()

def reddit(dataFolder) :
    import praw 
    import pandas as pd
    import matplotlib.pyplot as plt 
    import pprint 
    pp = pprint.PrettyPrinter(indent=2)
    import json
    import time
    import datetime

    reddit = praw.Reddit(
        client_id='qB2zYopSCvIXVQ',
        client_secret='HS_uLyox1i_ULUlqNiB-rCINduI',
        user_agent='social_analytics_scraper',
        username='noshiteinstein',
        password='Password1!'
    )

    posts = [
        "https://www.reddit.com/r/singapore/comments/65w4jb/need_help_with_choosing_between_nus_is_and_smu_sis/",
        "https://www.reddit.com/r/singapore/comments/b7zj6r/smu_interview/",
        "https://www.reddit.com/r/singapore/comments/b4v56k/is_it_really_worth_the_4_years_to_obtain_a_degree/",
        "https://www.reddit.com/r/singapore/comments/b03568/smu_admissions_2019/",
        "https://www.reddit.com/r/singapore/comments/69qpkf/degree_in_information_systems/",
        "https://www.reddit.com/r/SGExams/comments/bju38y/uni_how_is_the_culture_and_community_like_in_smu/?utm_source=share&utm_medium=ios_app",
        "https://www.reddit.com/r/singapore/comments/awfvxk/screwed_up_alevels_looking_for_advice/",
        "https://www.reddit.com/r/singapore/comments/albo22/current_student_and_alumni_of_smu_what_do_you/",
        "https://www.reddit.com/r/singapore/comments/83dh8h/anyone_willing_to_shed_some_light_on_nussmu/",
        "https://www.reddit.com/r/singapore/comments/8er108/what_are_your_views_about_smu/"
    ]

    result = {
        "name" : [],
        "message" : [],
        "timestamp" : [],
    }

    subreddit = reddit.subreddit('singapore')

    for submission in subreddit.new(limit=None):
        submission.comments.replace_more(limit=None)
        comment_queue = submission.comments[:]  # Seed with top-level
        while comment_queue:
            comment = comment_queue.pop(0)
            result["name"].append(str(comment.author))
            result["message"].append(str(comment.body).replace("\n", " "))
            timestamp = datetime.datetime.fromtimestamp(int(comment.created_utc)).strftime('%Y-%m-%d %H:%M:%S.%f')
            result["timestamp"].append(timestamp)
            comment_queue.extend(comment.replies)

    df = pd.DataFrame.from_dict(result)
    j = df.to_json(orient="records")
    j_obj = json.loads(j)
    with open(f"{dataFolder}reddit.json", "w+") as f:
        json.dump(j_obj, f, indent=2)   

def hwz(dataFolder):
    from scrapy import cmdline
    import os

    try :
        os.remove(f"{dataFolder}hwz.json")
    except:
        pass

    cmdline.execute(f"scrapy crawl hwz -o {dataFolder}hwz.json -t json".split()) 

validScrapeOption = False

while not validScrapeOption:
    scrape_choice = input("Do you want to scrape? (It can take quite a while) [Y/N] > ")
    if scrape_choice in "yY":
        reddit(dataFolder)
        hwz(dataFolder)
        validScrapeOption = True
    elif scrape_choice in "Nn":
        validScrapeOption = True


filename, searchRegexArr, start, end, chosen_unis, numberOfComments = display()
for i in chosen_unis:
    uni = universities[i]
    uniName = uni.split('|')[0]

    sentSentPath = f"{outputfile}{uniName} - {filename} Sentiment Sentences.csv"
    printNegNeuPos(sentSentPath, uni, start, end, searchRegexArr, numberOfComments)

    # print (f"Calculating sentiment scores for {uniName} now...")

    # sentimentPath = f"{outputfile}{uniName} - {filename} Sentiment Scores.csv"
    # writeFile(sentimentPath, uni, start, end, searchRegexArr, simplifiedInfoSys)

    # print (f"Finished calculating sentiment scores for {uniName}.")
    # print (f"Finding most meaningful sentences for {uniName} now...")

    # weightedPath = f"{outputfile}{uniName} - {filename} Weighted Sentences.csv"
    # printWeightiestSentences(weightedPath, uni, start, end, searchRegexArr, numberOfComments, simplifiedInfoSys)

    # print (f"Finished finding most meaningful sentences for {uniName}.")


print ("Please check output folder.")