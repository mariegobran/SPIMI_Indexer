import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import ast
import re
from nltk.stem.porter import PorterStemmer
from nltk.tokenize.regexp import RegexpTokenizer

stopwords = stopwords.words('english')

def is_number(value):
    try:
        number = ast.literal_eval(value)
        if isinstance(number, int) or isinstance(number, float):
            return True
        else:
            return False
    except:
        return False

def tokenizeArticle(article):
    # wordTokens = word_tokenize(article)
    tokenizer = RegexpTokenizer(r'\w+')
    wordTokens = tokenizer.tokenize(article)
    #strings with no letters
    pattern = re.compile("^[\W\s_0-9]+$")
    filteredTokens = [token for token in wordTokens if not pattern.match(token)]
    #remove punctuation
    filteredTokens =  [token for token in filteredTokens if not token in string.punctuation]
    #remove empty strings
    filteredTokens =  [token for token in filteredTokens if not token == "''" and not token == '``']
    #remove numbers
    filteredTokens = [token for token in filteredTokens if not is_number(token)]
    #remove stopwords 30
    filteredTokens = [token for token in filteredTokens if not token in stopwords]
    #remove stopwords 150
    # filteredTokens = [token for token in filteredTokens if not token in stopwords[30:151]]

    #case folding
    filteredTokens = [token.lower() for token in filteredTokens]
    #stemming
    # Stemming = PorterStemmer()
    # filteredTokens = [Stemming.stem(token) for token in filteredTokens]

    #remove digits
    filteredTokens = [token for token in filteredTokens if not token.isdigit()]
    return filteredTokens



# ******* TESTING ********

# testarticle = '''President Reagan, fighting to regain
# public confidence in the wake of the Iran arms scandal,
# admitted tonight that the clandestine operation wound up as an
# arms-for-hostages deal and, "It was a mistake."
#     "When it came to managing the NSC (National Security
# Council) staff, let's face it, 34 my style didn't match its
# previous track record," Reagan said in a television address to
# the American people. --check
#     "I have already begun correcting this," he added in his
# prepared remarks.
#     Reagan's speech, widely regarded as critical to his hopes
# of repairing his presidency, was his first detailed response to
# last week's scorching Tower commission report on the secret
# sale of arms to Iran and diversion of profits to U.S.-backed
# contra rebels in Nicaragua.'''
# print(str(tokenizeArticle(testarticle)))

art = 'Repeat and repeat again'
# print(str(tokenizeArticle(art)))