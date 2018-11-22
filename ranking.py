from afinn import Afinn


def sentimentVal(document):
    """
    ""  document in a string of the page content
    """
    afinn = Afinn()
    return afinn.score(document)


def rankingOrder(query):
    """ 
    "" checks if sentimental ranking should be ascending or descending
    """
    if (sentimentalVal(query) < 0): # overall negative sentiment value
        return 'asc'
    else: 
        return 'desc'


def sentimentRankDocs(documents): 
    """ rank each document,
    "" documents are in an array of (id, content) tuples
    "" return an array of id<>sentimentScores values
    """
    sentimentScores = []
    for doc in documents:
        sentimentScores[doc['id']] = sentimentVal(doc['content'])
    
    return sentimentScores

