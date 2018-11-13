import json
import os
from process_data import addDictToFile, combineTwoBlocks, getDictionary

# create inverted index
def createInvertedIndex(directory):
        numOfFiles = len(os.listdir(directory))
        firstfile = 'InvertedIndex.txt'
        iterateDir = iter(os.listdir(directory))
        while numOfFiles > 0:
                secondfile = next(iterateDir, None)
                dic1 = getDictionary(firstfile)
                dic2 = getDictionary(directory + '/' + secondfile)
                combinedBlock = combineTwoBlocks(dic1, dic2)
                addDictToFile(combinedBlock , firstfile)
                numOfFiles = numOfFiles-1


createInvertedIndex('DISK')