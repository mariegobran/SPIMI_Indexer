import os
import json
import re
import ast
from bs4 import BeautifulSoup
from collections import OrderedDict
from tokenizing import tokenizeArticle

if not os.path.exists( 'DISK' ):
    os.makedirs( 'DISK' )

blocknum = 1
blockIndex = []

# getText function - extracts title and body text from a reuters article
def getText(article):
    text = ''
    if not article.title is None:
        text = text + (article.title.text + ' ')
    if not article.body is None:
        text = text + (article.body.text)
    return text

# nextOutputFile function
def nextOutputFile():
    global blocknum
    file = open('DISK/Block'+str(blocknum).zfill(3)+'.txt', 'w+')
    blocknum = blocknum+1
    return file

# extract the documents from the reuters files 
# numfiles is the number of reuters files to extract (22 being the maximum)
def getDocuments(numfiles):
    documents = {}
    if numfiles > 22:
        numfiles = 22
    for i in range(numfiles):
        inputfile = open('reuters/reut2-'+str(i).zfill(3)+'.sgm', 'r')
        data = inputfile.read()
        soup = BeautifulSoup(data,'html.parser')

        for el in soup.find_all('reuters'):
            documents[el['newid']] = tokenizeArticle(getText(el))
            if(documents[el['newid']] is None):
                documents[el['newid']] = []

    return documents



def addDictToFile(dict, filepath):
    outputfile = open(filepath, 'w+')
    dict = OrderedDict(sorted(dict.items()))
    for term in dict:
        outputfile.write(term + ": " + str(dict.get(term))+ '\n')

def getDictionary(filepath):
    dictionary = {}
    inputfile = open(filepath , 'r')
    for line in inputfile:
        term = line[: line.index(':')]
        postings = line[(line.index(':')+2) : ]
        dictionary[term] = ast.literal_eval(postings)
    return dictionary

def combineTwoBlocks(dict1, dict2):
    newBlock = {}
    firstIterator = iter(dict1)
    secondIterator = iter(dict2)
    firstDictKey = next(firstIterator, None)
    secondDictKey = next(secondIterator, None)

    #check first key in both:
    #   1- if both keys are equal, combine their postings numbers list and add it to the new block
    #   2- if not equal
    #       a- if dict1 key is smaller add it to the new block
    #           a1- add it to the new block
    #           a2- check the next key in dict1 then go to 1
    #       b- if dict2 key is smaller repeat a (replace dict1 with dict2) 

    while (firstDictKey is not None) and (secondDictKey is not None):
        if(firstDictKey == secondDictKey):
            newBlock[firstDictKey] = (dict1[firstDictKey] + dict2[secondDictKey])
            firstDictKey = next(firstIterator, None)
            secondDictKey = next(secondIterator, None)
        elif(firstDictKey < secondDictKey):
            newBlock[firstDictKey] = dict1[firstDictKey]
            firstDictKey = next(firstIterator, None)
        else:
            newBlock[secondDictKey] = dict2[secondDictKey]
            secondDictKey = next(secondIterator, None)

    #after reaching the end of one dictionary
    if(firstDictKey is None):
        while(secondDictKey is not None):
            newBlock[secondDictKey] = dict2[secondDictKey]
            secondDictKey = next(secondIterator, None)
    else: 
        while(firstDictKey is not None):
            newBlock[firstDictKey] = dict1[firstDictKey]
            firstDictKey = next(firstIterator, None)
    return newBlock


def getNumber(str):
    if str != None:
        return int(str)
    else: 
        return 0

def combinePostings(list1, list2):
    newList = []
    list2Iter = iter(list2)
    key2 = getNumber(next(list2Iter, None))
    for newid in list1:
        key1 = int(newid)
        if key1 == key2:
            key2 = getNumber(next(list2Iter, None))
        else:
            while (key2 != 0) and (key1 > key2) :
                newList.append(str(key2))
                key2 = getNumber(next(list2Iter, None))
                continue
        newList.append(str(key1))
    while(key2 != 0):
        newList.append(str(key2))
        key2 = getNumber(next(list2Iter, None))

    return newList
