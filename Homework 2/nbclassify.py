import NButil
from NButil import *
import re
import sys
# import nblearn

changeToPresentDirectory()

debug = True


# Returns the probability of each word, we have trained
# Also, the probability of word given each of the 4 classes is returned
def wordProb():
    # probability of each words would be stored classwise
    # an Instance would look like:
    # {'word1' : {'class1': prob1, 'class2': prob2, ...}}
    wordProbability = {}
    with open('nbmodel.txt') as modelInfo:
        # Read all the word information
        wordsInfo = modelInfo.readlines()

        # For each word information
        for wordInfo in wordsInfo:
            # Split the line using the delimiter
            info = wordInfo.split(';;')
            if len(info) != 3:
                continue
            word = info[0]
            NBclass = info[1]
            probability = info[2][:-1]

            # seen the word already
            if word in wordProbability:
                wordProbability[word][NBclass] = probability
            # seeing the word for the first time
            else:
                wordProbability[word] = {NBclass: probability}

    return wordProbability


stopWords = addStopWords()
# print stopWords

wordProb = wordProb()
# print len(wordProb)

tuning = open('tuning.txt', 'w')
# structure of the map would be
# {word: {class: prob, ..}}
tuningMap = {}
# which classes to target
tunningTargetClasses = NBclasses

def classifyReview(fileLocation):
    reviewClass = None

    with open(fileLocation) as testData:
        # Read all the word information by spliting the words
        review = re.split(r"[,;!#^&*()\.\- ]+", testData.read())
        reviewWords = []

        # Remove all the stop words in the review
        for reviewWord in review:
            if reviewWord not in stopWords:
                reviewWord = replaceWords(reviewWord)
                if lowerAllWords or not reviewWord.isupper():
                    reviewWord = reviewWord.lower()
                reviewWords.append(reviewWord)
                if reviewWord in wordProb:
                    pass
                    # print reviewWord + str(wordProb[reviewWord])
        # print reviewWords


        probabilityMap = {}

        # Calculate the most likely class1
        for NBclass in NBclasses:
            tuning.write(NBclass + '\n\n')
            # print NBclass + '\n\n'
            if normalProbability:
                # reset the probability to 1, for each class
                probability = 1
            else:
                # reset the probability to 0, for each class
                probability = 0

            # print probability

            for word in reviewWords:
                # If the word has been seen in the training data
                if word in wordProb:
                    probWord = wordProb[word]

                    # print 'word is ' + word
                    # print 'prob is ' + str(probWord)

                    # if the word has been seen for the class in the training data
                    if NBclass in probWord:
                        if not normalProbability:
                            # Using the log of the probability
                            probability += float(probWord[NBclass])
                            addToTuningList(tuningMap, word, probWord[NBclass], NBclass, tunningTargetClasses)
                        else:
                            # Using the probability as such
                            probability *= float(probWord[NBclass])
                    else:
                        probWord = wordProb['--']
                        if not normalProbability:
                            # Using the log of the probability
                            probability += float(probWord[NBclass])
                            addToTuningList(tuningMap, word, probWord[NBclass], NBclass, tunningTargetClasses)
                        else:
                            # Using the probability as such
                            probability *= float(probWord[NBclass])

                # If the word was never seen in the training data
                else:
                    probWord = wordProb['--']
                    if not normalProbability:
                        # Using the log of the probability
                        probability += float(probWord[NBclass])
                        addToTuningList(tuningMap, word, probWord[NBclass], NBclass, tunningTargetClasses)
                    else:
                        # Using the probability as such
                        probability *= float(probWord[NBclass])

            print probability
            # print NBclass + str(probability)
            probabilityMap[NBclass] = probability
            tuning.write('\n\n')

        # Let the maximum of the probability be of class 'NT'
        reviewClass = 'NT'
        max = probabilityMap['NT']

        # print probabilityMap
        # print max
        # Calculate the most probable class
        for NBclass, probability in probabilityMap.iteritems():
            # print probability
            if probability > max:
                max = probability
                reviewClass = NBclass
    return reviewClass

performance = {'C': 0, 'W': 0}
polarityPerformance = {'C': 0, 'W': 0}
truthyPerformance = {'C': 0, 'W': 0}

# Testing some values in the tesing data
# for index in range(1,10):
#     print classifyReview('op_spam_train/negative_polarity/deceptive_from_MTurk/fold4/d_homewood_%d.txt' % index)


# print len(tuningMap)
# for word, probList in tuningMap.iteritems():
#     if len(probList) != len(tunningTargetClasses):
#         tuning.write(word + str(probList) + '\n\n')


if len(sys.argv) != 2:
    print "Missing the location of the test data"
else:
    rootFolder = sys.argv[1]

    # Get all the reviews in the Root Folder
    reviews = getAllReviews(rootFolder)

    output = open('nboutput.txt', 'w')
    # For each review, learn from it
    for review in reviews:
        classDetermined = classifyReview(review)

        output.write(getOutput(review, classDetermined) + '\n')

        NBclass = getClass(review)


        if NBclass == classDetermined:
            performance['C'] += 1
        else:
            # print fileLocation
            # print classIdentifier + ' - ' + reviewClassification[file]
            performance['W'] += 1


        if NBclass[0:1] == classDetermined[0:1]:
            polarityPerformance['C'] += 1
        else:
            # print fileLocation
            # print classIdentifier + ' - ' + reviewClassification[file]
            polarityPerformance['W'] += 1
        if NBclass[1:2] == classDetermined[1:2]:
            truthyPerformance['C'] += 1
        else:
            # print fileLocation
            # print classIdentifier + ' - ' + reviewClassification[file]
            truthyPerformance['W'] += 1
    output.close()
#
#
# for polarity in polarities:
#     for truthy in truthies:
#         folderName = truthy
#         if truthy.startswith(truthful) and polarity.startswith('neg'):
#             folderName += truthSource[0] + '/'
#         elif truthy.startswith(truthful):
#             folderName += truthSource[1] + '/'
#
#         words = {}
#         wordCount = 0
#
#         # Read the test folder
#         foldIndex = testFoldNumber
#
#         # The class identifier is the first character of the folder name
#         classIdentifier = polarity[0:1] + truthy[0:1]
#         classIdentifier = classIdentifier.upper()
#
#
#         for file in os.listdir(dataRoot + polarity + folderName + 'fold' + str(foldIndex)):
#             if file.endswith(".txt"):
#                 # the path to the review file
#                 fileLocation = dataRoot + polarity + folderName + 'fold' + str(foldIndex) + "/" + file
#                 classDetermined = classifyReview(fileLocation)
#
#                 if classIdentifier == classDetermined:
#                     performance['C'] += 1
#                 else:
#                     # print fileLocation
#                     # print classIdentifier + ' - ' + reviewClassification[file]
#                     performance['W'] += 1
#
#
#                 if classIdentifier[0:1] == classDetermined[0:1]:
#                     polarityPerformance['C'] += 1
#                 else:
#                     # print fileLocation
#                     # print classIdentifier + ' - ' + reviewClassification[file]
#                     polarityPerformance['W'] += 1
#                 if classIdentifier[1:2] == classDetermined[1:2]:
#                     truthyPerformance['C'] += 1
#                 else:
#                     # print fileLocation
#                     # print classIdentifier + ' - ' + reviewClassification[file]
#                     truthyPerformance['W'] += 1
# print float(polarityPerformance['C']) / (polarityPerformance['C'] + polarityPerformance['W'])
# print float(truthyPerformance['C']) / (truthyPerformance['C'] + truthyPerformance['W'])
# print float(performance['C']) / (performance['C'] + performance['W'])
