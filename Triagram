import nltk
import string
import pandas as pd
import matplotlib.pyplot as plt
import re
from pandas import DataFrame
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import random
from itertools import chain

def ini_list(file):
    fhand = open(file)
    txt = fhand.read().upper().strip()
    txt = txt.split()
    txt = [''.join(c for c in _ if c not in string.punctuation)for _ in txt]
    txt = [re.sub('[^a-zA-Z0-9]+','',_)for _ in txt]
    txt = ' '.join(txt)
    return txt
    
def gen_triagram(ini_list):
    word_list = ini_list.split()
    triagram = {}
    for i in range(len(word_list)-2):
        word1 = word_list[i]
        word2 = word_list[i+1]
        word3 = word_list[i+2]
        pair = (word1, word2)
        if pair not in triagram:
            triagram[pair] = [word3]
        else:
            triagram[pair].append(word3)
    return triagram

def gen_words(gen_triagram, num_of_words):
    triagram = gen_triagram
    word_list = []
    sample_key = random.choice(list(triagram.keys()))
    word_list.extend([word for word in sample_key])
    word_list.append(triagram[sample_key][random.choice(range(0,len(triagram[sample_key])))])
    while len(word_list) < num_of_words:
        key1,key2 = word_list[-2:]
        word_list.append(triagram[(key1,key2)][random.choice(range(0,len(triagram[(key1,key2)])))])
    return word_list

def gen_sentences(gen_triagram, num_of_words, num_of_sentences):
    sen = []
    for i in range(num_of_sentences):
        sen.append(gen_words(gen_triagram, num_of_words))
    return list(chain(*sen))

if __name__  == "__main__":
    file = 'C:/Users/jesse/Desktop/sherlock.txt' #initial file
    ini_list(file)
    gen_triagram(ini_list(file))
    num_of_words, num_of_sentences = (5,5)
    gen_words(gen_triagram(ini_list(file)), num_of_words)
    book = gen_sentences(gen_triagram(ini_list(file)), num_of_words, num_of_sentences)
    book = ' '.join(book)
    return book
 
