from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def scorer(sentence) :
    analyser = SentimentIntensityAnalyzer()
    return analyser.polarity_scores(sentence)

sent = "This phone is super not cool"

print (scorer(sent))