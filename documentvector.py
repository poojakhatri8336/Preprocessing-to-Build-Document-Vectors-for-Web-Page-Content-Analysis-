import spatial as spatial
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
import csv
import pandas as pd

#nltk.download()
from scipy.spatial.distance import cdist

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


urls=['https://en.wikipedia.org/wiki/Machine_learning','https://en.wikipedia.org/wiki/Engineering','https://my.clevelandclinic.org/research','https://en.wikipedia.org/wiki/Data_mining','https://en.wikipedia.org/wiki/Data_mining#Data_mining','http://cis.csuohio.edu/~sschung/']
stemmed_words=[]

for index,url in enumerate(urls):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser').get_text()
    soup= soup.replace('\n',' ')

    #remove digits from text
    text = ''.join([i for i in soup if not i.isdigit()])

    #remove unicode characters

    encoded_string = text.encode("ascii", "ignore")
    text = encoded_string.decode()


    text_file = open("doc"+str(index+1)+".txt", "w",encoding="utf-8")
    text_file.write(text)

    #Remove special symbols
    for char in '!\"#$%&()*+.-/:;<=>?@[\]^_`{|}~\n,':
        text=text.replace(char,' ')

    #convert all text to lower case
    text = text.lower()

    #generate tokens
    tokens = word_tokenize(text)
    for token in tokens:
        list_of_tokens[index].append(token)



#remove stop words
for list in list_of_tokens:
    for token in list:
        if token in list_stopwords:
            while token in list:
                list.remove(token)

#remove ' single quote
for list in list_of_tokens:
    for token in list:
        if "'" in token:
            list.remove(token)


for list in list_of_tokens:
    print(list)

#stemming- reduces words to their word root word or chops off the derivational affixes
for list in list_of_tokens:
        list[:] = [ps.stem(token) for token in list]



#-------------count no of times word appears---------------------
# Initializing Dictionary
d = {}
# Count number of times each word from word queries comes up in list of words (in dictionary)
Word_queries=['research','data','mine','analyt']
i=1
df=pd.DataFrame([])
for list in list_of_tokens:
    d={}
    for token in list:
            if token not in d:
                d[token] = 0
            d[token] += 1
    #print(d)
    for key,value in d.items():
        df = df.append({"term": key, "doc": i , "frequency" : value},ignore_index=True)
    i += 1

df.sort_values(by=['term'],inplace=True)
df.to_csv (r'TFIDF.csv', index = False, header=True)


researchlist=[]
datalist=[]
mininglist=[]
analyticslist=[]
researchlist.append("research")
datalist.append("data")
mininglist.append("mining")
analyticslist.append("analytics")

#checks in dataframe for all 6 doc ids for given single words. If it exists, fetches the count and store in list, if it doesnt keep 0
resultlist=[]
for i in range(1,7):
    result = df['frequency'].where((df['term'] == "research") & (df['doc'] == i)).dropna()
    if (len(result) == 0):
        researchlist.append("0")
    else:
        listToStr = ' '.join([str(elem) for elem in result.tolist()])
        researchlist.append(listToStr)
    result = df['frequency'].where((df['term'] == "data") & (df['doc'] == i)).dropna()
    if (len(result) == 0):
        datalist.append("0")
    else:
        listToStr = ' '.join([str(elem) for elem in result.tolist()])
        datalist.append(listToStr)
    result = df['frequency'].where((df['term'] == "mine") & (df['doc'] == i)).dropna()
    if (len(result) == 0):
        mininglist.append("0")
    else:
        listToStr = ' '.join([str(elem) for elem in result.tolist()])
        mininglist.append(listToStr)
    result = df['frequency'].where((df['term'] == "analyt") & (df['doc'] == i)).dropna()
    if (len(result) == 0):
        analyticslist.append("0")
    else:
        listToStr = ' '.join([str(elem) for elem in result.tolist()])
        analyticslist.append(listToStr)

print(researchlist)
print(datalist)
print(mininglist)
print(analyticslist)


#generate bigrams with frequency distributions and look for given bigrams in generated list

datamininglist=[]
machinelearninglist=[]
deeplearninglist=[]
datamininglist.append("data mining")
machinelearninglist.append("machine learning")
deeplearninglist.append("deep learning")

for list in list_of_tokens:
    bgs = nltk.bigrams(list)
    fdist = nltk.FreqDist(bgs)
    datamininglist.append(fdist['data', 'mine'])
    machinelearninglist.append(fdist['machin', 'learn'])
    deeplearninglist.append(fdist['deep', 'learn'])

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


#cosine similarity

for i in range(len(researchlist)):
    vector1 = [researchlist[1],datalist[1],mininglist[1],analyticslist[1],datamininglist[1],machinelearninglist[1],deeplearninglist[1]]
    vector2 = [researchlist[2],datalist[2],mininglist[2],analyticslist[2],datamininglist[2],machinelearninglist[2],deeplearninglist[2]]
    vector3 = [researchlist[3],datalist[3],mininglist[3],analyticslist[3],datamininglist[3],machinelearninglist[3],deeplearninglist[3]]
    vector4 = [researchlist[4],datalist[4],mininglist[4],analyticslist[4],datamininglist[4],machinelearninglist[4],deeplearninglist[4]]
    vector5= [researchlist[5],datalist[5],mininglist[5],analyticslist[5],datamininglist[5],machinelearninglist[5],deeplearninglist[5]]
    vector6 = [researchlist[6],datalist[6],mininglist[6],analyticslist[6],datamininglist[6],machinelearninglist[6],deeplearninglist[6]]

print(vector1)
print(vector2)
print(vector3)
print(vector4)
print(vector5)
print(vector6)
vectorlist=[]

vectorlist.append(vector1)
vectorlist.append(vector2)
vectorlist.append(vector3)
vectorlist.append(vector4)
vectorlist.append(vector5)
vectorlist.append(vector6)

'''
for i in range(3,6):
    for j in range(3,6):
        result = 1 - spatial.distance.cosine(vector1, vector2)
        print(result)
'''






























