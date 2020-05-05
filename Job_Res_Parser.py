import nltk
import string
import pandas as pd
import matplotlib.pyplot as plt
import re
from pandas import DataFrame
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
%matplotlib inline

'''Reading and cleaning up initial text'''
class Job_Desc_Parser():
    
    def ini_list(file):
        fhand = open(file)
        txt = fhand.read().strip().upper()
        txt = txt.split()
        txt = [''.join(c for c in _ if c not in string.punctuation)for _ in txt]
        txt = [re.sub('[^a-zA-Z0-9]+','',_)for _ in txt]
        txt = ' '.join(txt)
        return txt

    '''Creating one word list and using stopwords to filter non valuble words for word parsing'''
    def one_word(file):
        word_tokens = word_tokenize(Job_Desc_Parser.ini_list(file))
        stop_words = set(stopwords.words('english'))
        filtered_sentence = [w for w in word_tokens if w not in stop_words]
        return filtered_sentence
    
    '''Create word count dictionary '''    
    def dict_count(file):
        word_dict = {}
        for wds in Job_Desc_Parser.one_word(file):
            if wds not in word_dict:
                word_dict[wds] = 1
            else:
                word_dict[wds]+= 1
                
        delete = ('WILL','WE','AND', 'THE', 'TO', 'WITH', 'OF', 'A', 'FOR', 'OR',\
                  'YOU', 'IS', 'IN', 'AN', 'ARE', 'YOUR', 'BE', 'AS', 'AT','WE', 'THAT')
        
        
        for d in delete:
            if d in word_dict:
                word_dict.pop(d)
        word_dict = sorted(word_dict.items(), key = lambda kv:kv[1], reverse = True)
        return word_dict
    
    '''Filter out words'''    
    def filter_OneWord(filterWords, file):
        df_OneWord = Job_Desc_Parser.dict_count(file)
        df_OneWord = DataFrame(df_OneWord, columns = ['Key_Word', 'Word_Count'])
        df_OneWord = df_OneWord[:filterWords]
        return df_OneWord
    
    '''Create sentence dictionary and includes stopwords and prepositions'''
    def sentence(file, start, finish, increment):
        sen_dict = {}
        txt = Job_Desc_Parser.ini_list(file).strip().upper()
        txt = txt.split()
        word_list = [w for w in txt]
        
        multi_word_list = []
        for word in word_list:
            word = ' '.join(word_list[start:finish])
            start += increment
            finish += increment
            multi_word_list.append(word)
        multi_word_list = [x for x in multi_word_list if x !='']
        
        for sentence in multi_word_list:
            if sentence not in sen_dict:
                sen_dict[sentence] = 1
            else:
                sen_dict[sentence] += 1
        sen_dict = sorted(sen_dict.items(), key = lambda kv:kv[1], reverse = True)
        sen_dict = DataFrame(sen_dict, columns = ['Sentence', 'Count_of_Sentence_Repeatition'])
        return sen_dict       

    '''Main function to load file. Includes file location input from users'''
    def main(self,num_of_wds = 10): 
        file_loc = input('Paste file location of Job Posting: ')
        file = file_loc.replace('\\','/')
        Job_Desc_Parser.ini_list(file)
        Job_Desc_Parser.one_word(file)
        Job_Desc_Parser.dict_count(file)
        
        f = Job_Desc_Parser.filter_OneWord(num_of_wds, file)
        sen = Job_Desc_Parser.sentence(file,0,num_of_wds,num_of_wds)
        df = pd.DataFrame()
        fil = f['Key_Word']
        for i in range(num_of_wds):
            sen['Key_Word'] = fil[i]
            new = sen[sen['Sentence'].str.contains(fil[i])]
            df =  df.append(new)
        df = df[['Key_Word','Sentence', 'Count_of_Sentence_Repeatition']]
        return df
    
'''Created a Resume Parser class in which inherits the job parser class'''    
class Resume_Parser(Job_Desc_Parser):
    def main(self, num_of_words=5):
        file_loc = input('Paste in file location of Resume: ')
        file = file_loc.replace('\\','/')
        Resume_Parser.ini_list(file)
        Resume_Parser.one_word(file)
        Resume_Parser.dict_count(file)
        f = Resume_Parser.filter_OneWord(num_of_words, file)
        sen = Resume_Parser.sentence(file, 0, num_of_words, num_of_words)
        df = pd.DataFrame()
        fil = f['Key_Word']
        for i in range(num_of_words):
            sen['Key_Word'] = fil[i]
            new = sen[sen['Sentence'].str.contains(fil[i])]
            df = df.append(new)
        return df

jdp = Job_Desc_Parser() 
rp = Resume_Parser()

    
df_job_parser = jdp.main() #defaulf of 5 common word fiter

df_job_parser = df_job_parser.rename(columns={'Key_Word': 'Key_Word_in_Job_Req',
                        'Sentence': 'Sentence_Job_Req', 
                        'Count_of_Sentence_Repeatition': 'Count_of_Sentence_Repeatition_Job_Req'})

df_Resume_Parser = rp.main()

df_Resume_Parser = df_Resume_Parser.rename(columns={'Key_Word': 'Key_Word_in_Resume',
                        'Sentence': 'Sentence_in_Resume', 
                        'Count_of_Sentence_Repeatition': 'Count_of_Sentence_Repeatition_Resume'})

t = pd.merge(df_job_parser, df_Resume_Parser, left_on = 'Key_Word_in_Job_Req', right_on = 'Key_Word_in_Resume',how = 'outer')   

t1 = pd.merge(df_job_parser, df_Resume_Parser, left_on = 'Key_Word_in_Job_Req', right_on = 'Key_Word_in_Resume',how = 'outer')   


'''Ask path to save exported file'''

q = input('Provide folder path to save results: \n(example: C:\\Users\\user\\Desktop\)')
q = q.replace('\\','/')



words_Not_in_Resume = t[t['Key_Word_in_Resume'].isnull()].fillna('add key words/ phrase to resume') #Show missing key word in resume in top 5 words count in job posting
words_Not_in_Resume = words_Not_in_Resume.iloc[:,0:4]  #filtering columns
words_Not_in_Resume = words_Not_in_Resume.to_excel(q+'Words_Not_in_Resume'+'.xlsx',index =False, encoding='utf-8')


word_match = t1[t1['Key_Word_in_Resume'].notnull() & t1['Key_Word_in_Job_Req'].notnull()]
word_match = word_match[['Key_Word_in_Job_Req','Sentence_Job_Req', 'Sentence_in_Resume']]
word_match = word_match.rename(columns = {'Key_Word_in_Job_Req': 'Matched_Key Word'})

word_match = word_match.to_excel(q+'Resume_Job_desc_Word_Match'+'.xlsx',index =False, encoding='utf-8')

