#read inverted index
from tokenizing import tokenizeArticle
from process_data import getDictionary, combinePostings

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
    
print('1- single word query')
print('2- multiple words (AND)')
print('3- multiple words (OR)')

queryType = input('Enter your query choice: ')

def queryProcess(queryType):
    query = input('Enter your query: ')
    queryTokens = tokenizeArticle(query)
    invertedIndex = getDictionary('Index/InvertedIndex.txt')
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

queryProcess(queryType)