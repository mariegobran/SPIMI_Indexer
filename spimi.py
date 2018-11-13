import json
import os
import re
from bs4 import BeautifulSoup
from process_data import getText, nextOutputFile, getDocuments, addDictToFile, getDictionary
from tokenizing import tokenizeArticle

if not os.path.exists( 'DISK' ):
    os.makedirs( 'DISK' )

dictionary = {}
articlesInBlock = 0
outputfile = nextOutputFile()

def addIdToTerm(term, id, dictionary ):
    # check if each term is in the dictionary
    #   a- if yes: append article id to dictionary[newid] (check if the article newid is already in the list)
    #   b- if no : add the term as key to dictionary and give it a value of {article's newid}
    # global dictionary
    if term in dictionary:
        if id not in dictionary[term]:
            if dictionary[term][-1] != id:
                dictionary[term].append(id)
    else:
        dictionary[term] = [id]
    return dictionary


### Loop through the Reuters articles 
documents = getDocuments(22)

for newid in documents:
    if articlesInBlock < 500:
        for term in documents.get(newid):
            dictionary = addIdToTerm(term, newid, dictionary)
        articlesInBlock = articlesInBlock + 1
    else:
        # 1- sort dictionary #####
        # 2- copy current dictionary to new block
        # 2- dictionary = {}
        # 3- add terms to dictionary
        addDictToFile(dictionary, outputfile.name)
        dictionary = {}
        for term in documents.get(newid):
            dictionary = addIdToTerm(term, newid, dictionary)
        outputfile = nextOutputFile()
        articlesInBlock = 1

### Add last dictionary
addDictToFile(dictionary, outputfile.name)
