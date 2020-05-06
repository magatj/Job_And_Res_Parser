import random
import pandas as pd

def rand_word():
    
    '''Transform excel column and row files to a dictionary'''
    
    word_list = []
    q1 = input('What is the file location \n (file must only have on column with a header and values \n\
    example: C:/Users/jesse/Desktop/Word_list.xlsx)')#'C:/Users/jesse/Desktop/Word_list.xlsx'
    q1 = q1.replace('\\','/')
    wb = pd.read_excel(q1) #workbook
    df = pd.DataFrame.to_dict(wb)
    word_inv = list(df.values())[0]
    
    ini_inp = 'Generate Random Word?'
    add = ''
    
    while len(word_list) != len(word_inv):
   
        inp = input(ini_inp + add).strip().upper()
        if inp == 'Y':
            total_words = len(word_inv) 
            rand_num = random.randrange(total_words)
            random_word = word_inv[rand_num]
            
            '''while random word is in the word_list keep generating new word'''
            while random_word in word_list: 
                rand_num = random.randrange(total_words)
                random_word = word_inv[rand_num]
                continue
            '''when random word not in word_list append word_list and print the word'''
            if random_word not in word_list:
                word_list.append(random_word)
                print(random_word)
                ini_inp = '' #removing initial input text
                add = 'Generate Another One?'
                '''when word_list has the same values as word_inv print print warning and ask if file wants to be saved'''
                if len(word_list) == len(word_inv):
                    print('No More Words')
                    question = input('Do you want to save your list (Y | N)?').strip().upper()
                    
                    '''If file to be saved, specify location and name on where it will be saved'''
                    
                    if question == 'Y':
                        q = input('Provide folder path to save results: \n(example: C:\\Users\\user\\Desktop\)')
                        q = q.replace('\\','/')
                        q2 = input('Enter File Name').strip().upper()
                        new_dict = {'Word_List': [i for i in word_inv.values()]}
                        df = pd.DataFrame(new_dict)
                        df.to_excel(q+q2+'.xlsx', index =False, encoding='utf-8')        
                        break
        elif inp == 'N':
            break
            '''Update dictionary if user wants to add new word'''
        elif inp == 'ADD':
            key = len(word_inv)+1
            value = input('what word you want to add?')
            word_inv.update({key:value})
            add = 'Generate Another One'
        else:
            print('Select Y | N | ADD')       

            
if __name__ == "__main__":
    rand_word()