from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter
import nltk
import csv
import pandas as pd

nltk.download()

list1=[]
list2=[]
list3=[]
list4=[]
list5=[]
list6=[]
list_of_tokens=[]
list_of_tokens.append(list1)
list_of_tokens.append(list2)
list_of_tokens.append(list3)
list_of_tokens.append(list4)
list_of_tokens.append(list5)
list_of_tokens.append(list6)
bigram_token_list=[]

stop_words=set(stopwords.words("english"))
list_stopwords= list(stop_words)

ps = PorterStemmer()


urls=['https://www.edx.org/course/data-science-machine-learning','https://en.wikipedia.org/wiki/Engineering','https://my.clevelandclinic.org/research','https://en.wikipedia.org/wiki/Data_mining','https://en.wikipedia.org/wiki/Data_mining#Data_mining','http://cis.csuohio.edu/~sschung/']
stemmed_words=[]

for index,url in enumerate(urls):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser').get_text()
    soup= soup.replace('\n',' ')

    text_file = open("doc"+str(index+1)+".txt", "w",encoding="utf-8")
    text_file.write(soup)

    #Remove special characters
    for char in '!\"#$%&()*+.-/:;<=>?@[\]^_`{|}~\n,':
        soup=soup.replace(char,' ')

    #convert all text to lower case
    soup = soup.lower()


    #generate tokens
    tokens = word_tokenize(soup)
    for token in tokens:
        list_of_tokens[index].append(token)

#remove stop words
for list in list_of_tokens:
    for token in list:
        if token in list_stopwords:
            while token in list:
                list.remove(token)
'''
#stemming- reduces words to their word root word or chops off the derivational affixes
for list in list_of_tokens:
        list[:] = [ps.stem(token) for token in list]
'''


#-------------count no of times word appears---------------------
# Initializing Dictionary
d = {}
# Count number of times each word from word queries comes up in list of words (in dictionary)
Word_queries=['research','data','mining','analytics']

researchlist=[]
datalist=[]
mininglist=[]
analyticslist=[]
researchlist.append("research")
datalist.append("data")
mininglist.append("mining")
analyticslist.append("analytics")
for list in list_of_tokens:
    d={}
    for token in list:
        if token in Word_queries:
            if token not in d:
                d[token] = 0
            d[token] += 1
    print(d)
    if "research" in d.keys():
        researchlist.append(d["research"])
    else:
        researchlist.append("0")
    if "data" in d.keys():
        datalist.append(d["data"])
    else:
        datalist.append("0")
    if "mining" in d.keys():
        mininglist.append(d["mining"])
    else:
        mininglist.append("0")
    if "analytics" in d.keys():
        analyticslist.append(d["analytics"])
    else:
        analyticslist.append("0")

print(researchlist)
print(datalist)
print(mininglist)
print(analyticslist)


datamininglist=[]
machinelearninglist=[]
deeplearninglist=[]
datamininglist.append("data mining")
machinelearninglist.append("machine learning")
deeplearninglist.append("deep learning")

for list in list_of_tokens:
    global b
    bgs = nltk.bigrams(list)
    fdist = nltk.FreqDist(bgs)
    b = Counter()
    datamininglist.append(fdist['data', 'mining'])
    machinelearninglist.append(fdist['machine','learning'])
    deeplearninglist.append(fdist['deep', 'learning'])

print(datamininglist)
print(machinelearninglist)
print(deeplearninglist)



#write to csv

listofdocs=['',"doc1","doc2","doc3","doc4","doc5","doc6"]
with open('documentvector.csv', 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(listofdocs)
    csvwriter.writerow(researchlist)
    csvwriter.writerow(datalist)
    csvwriter.writerow(mininglist)
    csvwriter.writerow(analyticslist)
    csvwriter.writerow(datamininglist)
    csvwriter.writerow(machinelearninglist)
    csvwriter.writerow(deeplearninglist)





















