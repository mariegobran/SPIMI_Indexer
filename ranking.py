from afinn import Afinn


def sentimentVal(document):
    """
    ""  document in a string of the page content
    """
    afinn = Afinn()
    return afinn.score(document)


def sentimentRankDocs(documents): 
    """ rank each document,
    "" documents are in an array of (id, content) tuples
    "" return an array of id<>sentimentScores values
    """
    sentimentScores = {}
    for doc in documents:
        sentimentScores[doc['id']] = sentimentVal(doc['content'])
    
    return sentimentScores

def orderdRanks(query, scores):
    """ order sentiment ranks in ascending or descending order base on a given query
    """
    if (sentimentVal(query) < 0): # overall negative sentiment value
        orderedScores = sorted(scores.items(), key=lambda x: x[1])
    else: 
        orderedScores = sorted(scores.items(), reverse=True, key=lambda x: x[1])
    return orderedScores
