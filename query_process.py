#read inverted index
from tokenizing import tokenizeArticle
from process_data import getDictionary, combinePostings
import math
from collections import OrderedDict
import ast
from operator import itemgetter

reutersDocs =getDictionary('reuters_docs.txt') # all the documents in the reuters collections
invertedIndex = getDictionary('Index/InvertedIndex.txt') # SPIMI inverted index

# print(reutersDocs)
## resultsList is a list of query tokens and their corresponding postings
def queryAND(resultsList): 
    newList = next(iter(resultsList.values()))

    for token in resultsList:
        tempList = []
        for posting in resultsList[token]:
            if posting in newList:
                tempList.append(posting)
        newList = tempList
    return newList

def queryOR(queryTokens):
    resultsList = {}
    for token in queryTokens:
        if token in invertedIndex:
            resultsList[token] = invertedIndex[token]
    queryResult  = []
    for tokenlist in resultsList:
        queryResult = combinePostings(queryResult, resultsList[tokenlist])
    
    return queryResult


# print('1- single word query')
# print('2- multiple words (AND)')
# print('3- multiple words (OR)')

# queryType = input('Enter your query choice: ')

# Runs a query with a single word, AND operator or OR operator
def queryProcess(queryType):
    query = input('Enter your query: ')
    queryTokens = tokenizeArticle(query)
    if queryType is '1':
        print(invertedIndex[queryTokens[0]])
    elif queryType is '2':
        resultsList = {}
        for token in queryTokens:
            resultsList[token] = invertedIndex[token]
        print(queryAND(resultsList))
    elif queryType is '3':
        resultsList = {}
        for token in queryTokens:
            if token in invertedIndex:
                resultsList[token] = invertedIndex[token]
        queryResult  = []
        for tokenlist in resultsList:
            queryResult = combinePostings(queryResult, resultsList[tokenlist])
        print(str(queryResult))
    else:
        print('invalid query type!')


# Calculate idf of a term
def get_idf(term):
    dft = len(invertedIndex[term])
    n = len(reutersDocs)
    return math.log10(n/dft)

# Get tf in a document
def get_tf(term, document):
    counter = 0
    for token in document:
        if token == term:
            counter = counter + 1
    return counter


# Calculate BM25
def calc_bm25(queryterms, resultSet):
    scores = OrderedDict()
    docLength_avr = sum(len(reutersDocs[doc_id]) for doc_id in reutersDocs) / len(reutersDocs)
    
    for doc_id in resultSet:
        for term in queryterms:
            idf = get_idf(term)
            weight = 1 + get_tf(term, reutersDocs[doc_id])
            if doc_id in scores:
                scores[doc_id] += (weight * idf)
            else:
                scores[doc_id] = weight * idf
    scores_sorted = [k for k in sorted(scores, key=scores.get)]
    return (scores_sorted)

def query_bm25(query):
    query_tokens = tokenizeArticle(query)
    results_set = queryOR(query_tokens)
    scores_sorted = calc_bm25(query_tokens, results_set)
    return scores_sorted



# ****** TESTING *******
# print('first document length = ' + str(len(reutersDocs['1'])))
# print('average document length ' + str(calc_bm25(1,2)))
# for doc_id in reutersDocs:
#     print(doc_id + ' length = ' + str(len(reutersDocs[doc_id])))
# print ("documents lenghts" + (str(len(document)) for documnet in reutersDocs))

# queryProcess(queryType)

newQuery = True
while newQuery:
    user_query = input('Enter your query for user:')
    print('your query results: ' + str(query_bm25(user_query)))

    newQuery = True if input('Do you have a new query? (y/n) ')=='y' else False
