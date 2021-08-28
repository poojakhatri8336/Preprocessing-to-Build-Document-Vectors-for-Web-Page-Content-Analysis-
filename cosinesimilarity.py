from scipy import spatial
import pandas as pd
import csv

vector1=[]
vector2=[]
vector3=[]
vector4=[]
vector5=[]
vector6=[]
col_list = ["doc1","doc2","doc3","doc4","doc5","doc6"]
df = pd.read_csv("documentvector.csv", usecols=col_list)
vector1.append(df["doc1"].values)
vector2.append(df["doc2"].values)
vector3.append(df["doc3"].values)
vector4.append(df["doc4"].values)
vector5.append(df["doc5"].values)
vector6.append(df["doc6"].values)

vectorlist=[]

vectorlist.append(vector1)
vectorlist.append(vector2)
vectorlist.append(vector3)
vectorlist.append(vector4)
vectorlist.append(vector5)
vectorlist.append(vector6)
with open('cosinesimilarity.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['',"doc1","doc2","doc3","doc4","doc5","doc6"])
    for i in range(0,6):
        cosinelist = []
        cosinelist.append("doc"+str(i+1))
        for j in range(0,6):
            result = 1 - spatial.distance.cosine(vectorlist[i], vectorlist[j])
            cosinelist.append(result)
        csvwriter.writerow(cosinelist)
