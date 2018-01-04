# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 17:29:52 2017

@author: rajar
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 16:35:49 2017

@author: rajar
"""

import collections
from collections import Counter
import operator
import numpy
import math
import re
import nltk
from nltk.corpus import stopwords

posdocs = 0
negdocs = 0
priorposprob = 0
priornegprob = 0
totalposwords = 0
totalnegwords = 0
totalwords = 0
allposwords = []
allnegwords = []
vocabulary = []
counterposwords = []
counternegwords = []
counterposwordsdict = {}
counternegwordsdict = {}
likelihoods = {}

poskey = ""
negkey = ""
posoccur = 0
negoccur = 0

finalposprob = 1
finalnegprob = 1

classifier = ""

inputfile = open("testdata.txt",'r').readlines()
outputfile = open("testdataoutput2.txt","w")

posfile = open("hotelPosT-train.txt",'r',encoding="utf8").readlines()

for line in posfile:
    if (line[:2] == "ID"):
        posdocs += 1
        t = line[7:]
        s = t.strip().split(" ")
        for i in range (1,len(s)):
            abc = re.sub('[^A-Za-z0-9]+', '', s[i]) 
            allposwords.append(abc)

negfile = open("hotelNegT-train.txt",'r',encoding="utf8").readlines()

for line in negfile:
    if (line[:2] == "ID"):
        negdocs += 1
        t = line[7:]
        s = t.strip().split(" ")
        for i in range (1,len(s)):
            bcd = re.sub('[^A-Za-z0-9]+', '', s[i])
            allnegwords.append(bcd)

priorposprob = posdocs/(posdocs + negdocs)
priornegprob = negdocs/(posdocs + negdocs)

stoplist = stopwords.words('english')

for i in stoplist:
    for j in allposwords:
        if (i == j):
            #print(j)
            allposwords.remove(j)
    for k in allnegwords:
        if (i == k):
            #print(k)
            allnegwords.remove(k)
    
counterposwords = Counter(allposwords)
counternegwords = Counter(allnegwords)

vocabulary = sorted(set(allposwords + allnegwords))

for i in counterposwords:
    counterposwordsdict[i] = counterposwords[i]
    
for j in counternegwords:
    counternegwordsdict[j] = counternegwords[j]

totalposwords = len(allposwords)
totalnegwords = len(allnegwords)

totalwords = totalposwords + totalnegwords

#------------------------------------------------------------------------
#-----------------------End of all calculations--------------------------
#------------------------------------------------------------------------

#------------------------------------------------------------------------
#-----------------------Sentence classifier function---------------------
#------------------------------------------------------------------------

def sentenceclassifier(r):
    for i in r:
        poskey = i + "," + "pos"
        negkey = i + "," + "neg"
        if i in counterposwordsdict:
            posoccur = counterposwordsdict[i]
        else:
            posoccur = 0
        if i in counternegwordsdict:
            negoccur = counternegwordsdict[i]
        else:
            negoccur = 0
        likelihoods[poskey] = (posoccur + 1)/(totalposwords + len(vocabulary))
        likelihoods[negkey] = (negoccur + 1)/(totalnegwords + len(vocabulary))
    
    posprob = 0
    negprob = 0
    for j in r:
        if j in vocabulary:
            poskey = j + "," + "pos"
            negkey = j + "," + "neg"
            posprob += math.log(likelihoods[poskey])
            negprob += math.log(likelihoods[negkey])
        else:
            continue

    
    finalposprob = math.log(priorposprob) + posprob
    finalnegprob = math.log(priornegprob) + negprob
    if finalposprob > finalnegprob:
        classifier = "POS"
    else:
        classifier = "NEG"
    #print(classifier)
    return classifier

#------------------------------------------------------------------------
#--------------------Populating the output files-------------------------
#------------------------------------------------------------------------

nopuncArray=[]
st2 = []
for k in inputfile:
    q = k[7:]
    r = q.strip('\t').strip('\n')
    st = r.split(" ")
    #st2 = st.strip('\t').strip('\n')
    #print(st)
    for i in range (1,len(st)):
        cde = re.sub('[^A-Za-z0-9]+', '', st[i])
        #print(cde)
        st2.append(cde)
    print(st2)
    outputfile.write(k[:7] + " " + sentenceclassifier(st) + "\n")
    st2 = []
