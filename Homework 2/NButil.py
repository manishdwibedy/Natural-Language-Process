import os
from os import path

# Symbols Array
symbols = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
           '-', '_', '+', '=', '{', '}', '[', ']', ';', ':', '\'', '"',
           '<', '>', ',', '.', '/', '?']


# Taking the normal probability, not using the log of the probability
normalProbability = False

# The NB classes list
NBclasses = ['ND', 'NT', 'PD', 'PT']

# Lower all the words or leave the uppercase words
lowerAllWords = True

# Routine to change to the current directory
def changeToPresentDirectory():
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

changeToPresentDirectory()

# Ignoring the most common words as stop words
# don't matter in categorizing the reviews
def addStopWords():
    stopWords = []
    with open('stopWords.txt') as file:
        content = file.readlines()
        for word in content:
            # Ignoring the white space character at the end of the line
            stopWords.append(word[:-1])
    return stopWords

# Remove any symbol, if present in the word
def replaceWords(inputWord):
    for symbol in symbols:
        inputWord = inputWord.replace(symbol,'')
    return inputWord



# Routine to remove the suffix for the end of the words
# Input   : word
# Returns : if the word has the suffix, retruns the stripped word
#           else the word is returned
def removeSuffix(word):
    suffixList = ['acy','al','ance','ence','dom','er','or','ism','ist','ity','ty',
              'ment','ness','ship','sion','tion','ate','en','ify','fy','ize',
              'ise','able','ible','al','esque','ful','ic','ical','ious','ous',
              'ish','ive','less','y']

    # If the word ends with one of suffix
    if word.endswith(tuple(suffixList)):
        # Loop through every suffix
        for suffix in suffixList:
            # Find the suffix
            if word.endswith(suffix):
                # Remove the suffix and return the stripped word
                return word[:word.index(suffix)]
    # Else the word is returned as such
    else:
        return word

# Return the output in the expected format
def getOutput(review, NBclass):
    classFound = ''
    if NBclass == 'ND':
        classFound = 'deceptive negative'
    elif NBclass == 'NT':
        classFound = 'truthful negative'
    elif NBclass == 'PD':
        classFound = 'deceptive positive'
    else:
        classFound = 'truthful positive'

    return classFound + ' ' + review

# Get the NB class of the review from the directory structure
def getClass(fileLocation):
    NBclass = ''

    # Whether the review is positive or negative
    if 'positive' in fileLocation:
        NBclass += 'P'
    else:
        NBclass += 'N'

    # Whether the reciew is deceptive or truthful
    if 'deceptive' in fileLocation:
        NBclass += 'D'
    else:
        NBclass += 'T'

    return NBclass

# Read all the reviews for the root folder
def getAllReviews(rootFolder):
    reviews = []
    for root, dirs, files in os.walk(rootFolder, topdown=False):
        for name in files:
            if name.endswith(".txt") and not name.startswith('README'):
                reviews.append(os.path.join(root, name))
    return reviews

def addToTuningList(tuningMap, word, prob, NBclass, targetClasses):
    # print tuningMap
    if NBclass in targetClasses:
        if word in tuningMap:
            tuningMap[word][NBclass] = prob
        else:
            tuningMap[word] = {NBclass: prob}
