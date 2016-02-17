#!/usr/bin/env python
import NButil
from NButil import *
import os
from os import path
import sys
import re
import math
import collections

# Map to store the training words in the format:
# Class : Map of words (word: count)
# For eg.   ND - negative deceptive, NT - negative truthful
#           PD - positive deceptive, PT - positive truthful
# Instance would be like : ND : {'word1': 1, 'word2': 2}
vocabulary = {}

# Count the number of unique words in our vocabulary
vocabularyCount = set()

# NBClass words encountered for every class
# Class : count
# {ND : 5, NT: 10, ....}
NBWordCount = {}

# Would be storing the number of words in an NB class
# An Instance would be like:
# {class1: 5, class2: 10}
# wordCount = {}

# Would store the word seen in an NB class
# An Instance would be like:
# {class1: [{word1: 5, word2: 10}], class2: {word3: 15, word4: 20}}
# words = {}

# word - count
frequentWords = {}

def addToFrequencyList(word):
    if word in frequentWords:
        frequentWords[word] += 1
    else:
        frequentWords[word] = 1

# Would increment the vocabulary count of the class
def incrementNBVocabCount(NBclass):
    if NBclass in NBWordCount:
        NBWordCount[NBclass] += 1
    else:
        NBWordCount[NBclass] = 1

# Would be adding the word to the list of words found for the specified class
def addWordToList(word, NBclass):
    if NBclass in vocabulary:
        wordList = vocabulary[NBclass]
        if word in wordList:
            wordList[word] += 1
        else:
            wordList[word] = 1
    else:
        vocabulary[NBclass] = {word: 1}

# Would be learning by a specified training review
def learn(fileLocation):
    # opening the review file
    fileObj = open(fileLocation)

    NBclass = getClass(fileLocation)
    # split the review by space
    review = re.split(r"[,;!#^&*()\.\- ]+", fileObj.read())
    # review = fileObj.read().split()

    # read every word
    for reviewWord in review:
        # if the word is not a stop word
        reviewWord = replaceWords(reviewWord)

        # print reviewWord
        if lowerAllWords or not reviewWord.isupper():
            reviewWord = reviewWord.lower()
            # print reviewWord

        if reviewWord not in stopWords and reviewWord != '':
            # Adding to frequentWords List
            addToFrequencyList(reviewWord)

            # Incrementing the word count
            incrementNBVocabCount(NBclass)

            # Adding the word to the set of unique vocabulary
            vocabularyCount.add(reviewWord)

            # Need to test the suffix list
            # reviewWord = removeSuffix(reviewWord)

            # Would be counting the word found
            addWordToList(reviewWord, NBclass)

def writeToFile():

    # writing the vocabulary to nbmodel to be used for nbclassify
    # Format of the file
    # Word ;; Class ;; log(probability)
    output = open('nbmodel.txt', "w")

    # Number of unique words found in our training data
    uniqueWordCount = len(vocabularyCount)

    if normalProbability:
        print 'Taking normalProbability'
    else:
        print 'Taking log of the probability'

    # print uniqueWordCount


    for NBclass, NBwordList in vocabulary.iteritems():
        # print len(NBwordList)
        for word, count in NBwordList.iteritems():
            probability = float(count + 1) / (NBWordCount[NBclass] + uniqueWordCount)

            if normalProbability:
                # Taking the probability as such
                # print(word + ';;' + NBclass + ';;' + str(probability) + '\n')
                output.write(word + ';;' + NBclass + ';;' + str(probability) + '\n')
            else:
                # Taking the log of the probability
                output.write(word + ';;' + NBclass + ';;' + str(math.log(probability)) + '\n')
        else:
            probability = float(1) / (NBWordCount[NBclass] + uniqueWordCount)

            if normalProbability:
                # Taking the probability as such
                # print('--;;' + NBclass + ';;' + str(probability) + '\n')
                output.write('--;;' + NBclass + ';;' + str(probability) + '\n')
            else:
                # Taking the log of the probability
                # print('--;;' + NBclass + ';;' + str(probability) + '\n')
                output.write('--;;' + NBclass + ';;' + str(math.log(probability)) + '\n')

        # Adding the probability for word that are not seen in the classIdentifier

    output.close()



changeToPresentDirectory()

stopWords = addStopWords()

if len(sys.argv) != 2:
    print "Missing the location of the training data"
else:
    rootFolder = sys.argv[1]

    # Get all the reviews in the Root Folder
    reviews = getAllReviews(rootFolder)

    # For each review, learn from it
    for review in reviews:
        learn(review)

    # Write the output to a file
    writeToFile()

topFrequestWords = sorted(frequentWords, key=frequentWords.get, reverse=True)

for index in range(10):
    print topFrequestWords[index]


# ---------------------
#        TESTING
# ---------------------
# Finding the common words that are in every class 50 times or more
commonWordList = []
commonWords = {}
for NBclass, NBwordList in vocabulary.iteritems():
    # print len(NBwordList)
    count = []
    for word, count in NBwordList.iteritems():
        if count > 50:
            if word in commonWords:
                commonWords[word] += 1
            else:
                commonWords[word] = 1
for word, count in commonWords.iteritems():
    if count == 4:
        # print word
        commonWordList.append(word)
