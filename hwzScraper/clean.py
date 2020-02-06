import pandas as pd
from collections import Counter
import nltk 
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt 

ps = PorterStemmer()

stop_words = set( stopwords.words('english') )

df = pd.read_json("data.json")

temp_df = df.head(5)

messages = []

wordcloud_str = ''
frequency_chart = []

for index, row in df.iterrows():
    msg = row["msg"]
    temp_msg = ""
    for word in msg.split(" "):
        clean_word = word.strip(".").strip(",").strip(":").lower()
        if clean_word not in stop_words:
            temp_msg += word + " "
            frequency_chart.append(clean_word)
    messages.append(temp_msg)
    wordcloud_str += temp_msg

top_few_words = 30
word_count = dict(Counter(frequency_chart))
word_count = dict(sorted(word_count.items(), key=lambda x:-x[1])[1:top_few_words])
# print (dict(word_count))
freq_df = pd.DataFrame.from_dict(word_count, orient="index")
freq_df.plot(kind="bar")
plt.show()

wc = WordCloud().generate(wordcloud_str)

plt.imshow(wc)
plt.axis("off")
plt.show()