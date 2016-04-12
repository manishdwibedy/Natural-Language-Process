import pickle
import util
import constant

def getHMMModel(filename):
    """
    Get the HMM model from the file
    :param filename: the file's path
    :return: the starting, transmission and emission probabilities
    """
    with open(filename) as file:
        starting_prob, transition_prob, emission_prob = pickle.load(file)
    return starting_prob, transition_prob, emission_prob

def tagData(starting_prob, transition_prob, emission_prob, file_contents):

    currentTag = ''
    # previousTag = ''
    tagged_info = []


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
                print ''
        tagged_sentences.append(tagged_sentence)
    return tagged_sentences

if __name__ == '__main__':
    starting_prob, transition_prob, emission_prob = getHMMModel('hmm_model.txt')

    file_contents = util.getUntaggedWords(constant.RAW_DATA)
    tagged_sentences = tagData(starting_prob, transition_prob, emission_prob, file_contents)

    true_value = util.getTaggedWords(constant.DEV_TAGGED_DATA)
    pass