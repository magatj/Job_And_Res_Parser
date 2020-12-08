import string
import pandas as pd
import re
from pandas import DataFrame
from textblob import TextBlob
from itertools import chain
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as mpLib

#Parsing problem sentences
def problem():
    with open('**FILE HERE***') as fhand:
        #fhand = fhand.read()
        word_list = []
        for line in fhand:
            if 'Describe Your Pain Point or Business Problem Here:' in line:
                line = line.rstrip()
                line = line.replace('Describe Your Pain Point or Business Problem Here:','')
                line = line.split()
                line = [re.sub('[^a-zA-Z0-9]+','',_)for _ in line] #remove special characters
                line = ' '.join(line) #unlisting each line
                word_list.append(line)                
        return word_list

#Parsing users
def user():
    with open('**FILE HERE***.txt') as fhand:
        word_list = []
        for line in fhand:
            if 'By: Full Name/Business Unit/Function/Program/Site:' in line:
                line = line.rstrip()
                line = line.replace('By: Full Name/Business Unit/Function/Program/Site:','')
                line = line.split()
                line = [re.sub('[^a-zA-Z0-9/]+','',_)for _ in line] #remove special characters
                line = ' '.join(line)
                word_list.append(line)
        return word_list

# Splitting each word in problem sentences to a list
def one_word():
    word = problem() # multi word list
    word = ' '.join(word) #remove all items from list
    return word.split() #splitting words

#Counting each word and filtering it to top n words
def dict_count(filter):
    d ={}
    for word in one_word():
        word = word.upper()
        if word not in d:
            d[word] = 1
        else:
            d[word]+= 1
    delete = ('OF',  'WITH','AT','FROM', 'BE') #Deleting prepositions and non value added nouns
    for prep in delete:
        if prep in d:
            d.pop(prep)           
    d = sorted(d.items(), key = lambda kv:kv[1], reverse = True)
    d = DataFrame(d, columns = ['Word', 'Word_Count'])
    d = d[:filter]
    return d


#Combining problem and user values so it can be seen in a pivoted view 
def prb_usr():
    word_list = []
    for i in range(len(problem())):
        try:
            i = (user()[i],  problem()[i]) # length of user sometimes does not match problem
            word_list.append(i)
        except:
            continue
    return word_list

#Combining problem and user values so it can be seen in a pivoted view -- making it a DataFrame
def prb_usr_df():
    df = DataFrame(prb_usr(), columns = ['USER', 'PAIN_POINT'])
    return df

#Sentiment analysis using TextBlob library
def prb_sentiment():
    reviews = problem()
    print('{:40} :   {:10}   : {:10}'.format("Review", "Polarity","Subjectivity") ) #Header
    for review in reviews:
        sentiment = TextBlob(review)
        print('{:<40} :  {: 01.2f}         :{:01.2f}'.format(review[:40], sentiment.polarity, sentiment.subjectivity))
        
        
print('\n','Pain Points Word Count', '\n' '\n', dict_count(10)) #top 10 on dict_count
'\n'
prb_sentiment()
prb_usr_df()    

filedata = one_word()
filedata = ' '.join(filedata)
stopwords = set(STOPWORDS)        
wordcloud = WordCloud(stopwords=stopwords,max_words=25,\
                     background_color="white").generate(filedata) 
'\n'
mpLib.imshow(wordcloud)
mpLib.axis("off")
mpLib.show()