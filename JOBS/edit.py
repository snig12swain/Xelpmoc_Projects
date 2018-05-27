import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from subprocess import check_output
from sklearn import datasets
from scipy import stats

df1=pd.read_csv('jobs_cleaned.csv')
df1.head(1000)
df1.shape
df_cleaned=df1.iloc[:,:5]
df_cleaned.shape
df_cleaned.head(100)

df_cleaned.columns = ["A", "B", "C", "D", "E"]

df_cleaned.head(20)

df_cleaned.iloc[0,0]
df_cleaned.iloc[4500,0]

df_cleaned['A'].value_counts()
print (df_cleaned.head(100))



count = dict(df_cleaned['A'].value_counts())

A = list(df_cleaned.iloc[:, [0]].values[:, 0])
req = []
for i in range(len(A)):
    if count[A[i]] != 1:
        req.append(df_cleaned.iloc[[i]].values)

print(req)

counter = 0
l1=[]
l2=[]
for keys in count:
    if counter <9:
        l1.append(count[keys])
        l2.append(keys)
        counter +=1
    else:
        break       
