import pickle
import util
import constant
import datetime
import sys

def getHMMModel(filename):
    """
    Get the HMM model from the file
    :param filename: the file's path
    :return: the starting, transmission and emission probabilities
    """
    with open(filename) as file:
        starting_prob, transition_prob, emission_prob = pickle.load(file)
    return starting_prob, transition_prob, emission_prob

def getMostProbableTag(transition_prob):
    most_likely_tag = {}
    for tag, tag_prob in transition_prob.iteritems():
        max_prob = 0
        max_tag = ''
        for nextTag in tag_prob:
            if nextTag['prob'] > max_prob:
                max_prob = nextTag['prob']
                max_tag = nextTag['previous']
        most_likely_tag[tag] = max_tag
    return most_likely_tag


def tagData(starting_prob, transition_prob, emission_prob, file_contents):

    currentTag = ''
    # previousTag = ''
    tagged_info = []

    most_probable_tag = getMostProbableTag(transition_prob)

    tagged_sentences = []
    for sentence in file_contents:
        tagged_sentence = []

        for word in sentence:
            # The word has already been seen in the training data
            if word in emission_prob:

                # First word in the sentence
                if currentTag == '':
                    maxProb = 0
                    bestTag = ''


                    for emission_tag in emission_prob[word]:
                        tag = emission_tag['tag']
                        prob = emission_tag['prob']

                        if tag in starting_prob:
                            prob *= starting_prob[tag]

                        # If found a more probable tag
                        if prob > maxProb:
                            maxProb = prob
                            bestTag = tag
                    # Found the most probable tag
                    tagging = {
                        'word': word,
                        'tag': bestTag
                    }
                    # Change the tag
                    currentTag = bestTag
                    tagged_sentence.append(tagging)


                # The word has a previous word/tag data
                else:
                    maxProb = 0
                    bestTag = ''

                    for emission_tag in emission_prob[word]:
                        tag = emission_tag['tag']
                        prob = emission_tag['prob']


                        # Found the transition prob from 'last' POS to emitted tag
                        for possibleTag in transition_prob[tag]:
                            if currentTag == possibleTag['previous']:
                                prob *= possibleTag['prob']
                                break

                        # If found a more probable tag
                        if prob > maxProb:
                            maxProb = prob
                            bestTag = tag
                    # Found the most probable tag
                    tagging = {
                        'word': word,
                        'tag': bestTag
                    }
                    # Change the tag and
                    currentTag = bestTag
                    tagged_sentence.append(tagging)
            else:
                # By default, assuming that the unknown word is NC
                tagging = {
                    'word': word,
                    'tag': most_probable_tag[currentTag]
                }
                # Change the tag to NC
                tagged_sentence.append(tagging)
                currentTag = most_probable_tag[currentTag]
        tagged_sentences.append(tagged_sentence)
    return tagged_sentences

def getDiff(tagged_sentences, true_value):

    correctTag = 0
    wrongTag = 0
    sentenceIndex = 0
    for sentence in true_value:
        wordIndex = 0
        for word in sentence:

            true_tag = word['tag']
            tag_assigned = tagged_sentences[sentenceIndex][wordIndex]['tag']

            if true_tag == tag_assigned:
                correctTag += 1
            else:
                wrongTag += 1
            wordIndex += 1
        sentenceIndex += 1
    accuracy = float(correctTag) / (correctTag + wrongTag)
    print 'Accuracy : ' + str(accuracy * 100)
    pass

def writeOutput(tagged_sentences):

    sentences = []

    # Preparing the data to be written in the file
    for sentence in tagged_sentences:
        sentence_file = ''
        for tagged_word in sentence:
            sentence_file += tagged_word['word'] + '/' + tagged_word['tag'] + ' '
        sentence_file = sentence_file.strip()
        sentence_file += '\n'
        sentences.append(sentence_file)

    output = open('hmmoutput.txt', 'w')
    for sentence in sentences:
        output.write(sentence)
    output.close()
    pass
if __name__ == '__main__':
    start = datetime.datetime.now()

    num_of_args = len(sys.argv)

    if num_of_args == 2:
        filename = sys.argv[1]

    starting_prob, transition_prob, emission_prob = getHMMModel('hmm_model.txt')

    file_contents = util.getUntaggedWords(filename, True)
    tagged_sentences = tagData(starting_prob, transition_prob, emission_prob, file_contents)

    # If True, would compute the accurary of the tagger
    if constant.COMPUTE_ACCURACY:
        true_value = util.getTaggedWords(constant.DEV_TAGGED_DATA)
        getDiff(tagged_sentences, true_value)

    writeOutput(tagged_sentences)

    end = datetime.datetime.now()
    print 'Took ' + str(end-start) + ' time.'

    pass