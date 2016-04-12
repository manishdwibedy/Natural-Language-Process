import util
import constant
import datetime
import pickle
import sys

def getTagInfo(filename):
    """
    Getting the tag information from the data file
    :param filename: The name of the data file
    :return: the list of object, where each object would be dict representing tag and word
    """
    return util.getTaggedWords(filename)

def getStartingTagCount(tag_info):
    """
    Getting the count of the starting tag count
    :param tag_info: the tag information list
    :return: a dict containing the count of starting TAG
    """
    starting_prob = {}
    index = 0
    for sentence in tag_info:
        startingTagInfo = sentence[0]

        tag = startingTagInfo['tag']

        # Raise an exception, if the length of the tag is not 2
        if len(tag) != 2:
            raise ValueError('The length of the tag is not 2')

        if tag in starting_prob:
            starting_prob[tag] += 1
        else:
            starting_prob[tag] = 1
        index += 1
    return starting_prob

def isStartProbCorrect(tag_info, start_prob):
    """
    Checking if any starting probability is missed or added extra
    :param tag_info: the tag info list
    :param start_prob: the dict representing the tag with count
    :return:
    """
    sentence_count = len(tag_info)
    tag_count = 0
    for tag, count in start_prob.iteritems():
        tag_count += count

    if sentence_count < tag_count:
        # Missing starting probability
        return False
    elif tag_count > sentence_count:
        # Missed tag information
        return False
    else:
        return True

def getStartProb(start_prob, totalCount):
    """
    Computing the starting probability
    :param start_prob: the dict representing the tag with the count
    :param totalCount: the total number of sentences in the data file
    :return: a dict representing the tag with their probability
    """
    starting_prob = {}

    totalCount = float(totalCount)

    for tag, count in start_prob.iteritems():
        starting_prob[tag] = count/totalCount
    return starting_prob

def getPOSTransitionCount(tag_info):
    """
    Compute the transition probability
    :param tag_info: the tag information
    :return: a dictionary with key as 'curr' and the value is an dict as prev and count
    """

    transitionProb = {}

    count = 0
    # For every set of tags for a sentence
    for tags in tag_info:

        # print 'Reading sentence : ' + str(count)
        count += 1

        # Initialize the previous and current tag to empty string
        prev = ''
        curr = ''

        for tag in tags:
            # Store the tag to the current tag
            curr = tag['tag']

            # Would cover the first tag
            if prev != '':
                # Already seen the current tag
                if curr in transitionProb:
                    # Get the transitions to the curr tag
                    transition_array = transitionProb[curr]

                    # Loop over the transitions

                    index = getPreviousTagIndex(prev, transition_array)
                    if index > -1:
                        prevTagInfo = transition_array[index]
                        prevTagInfo['count'] += 1
                    else:
                        transition = {
                            'previous': prev,
                            'count': 1
                        }
                        transition_array.append(transition)
                        transitionProb[curr] = transition_array
                else:
                    transition = {
                        'previous': prev,
                        'count': 1
                    }
                    transition_array = [transition]
                    transitionProb[curr] = transition_array
                # Store the current to the previous
                prev = curr
                continue
            else:
                # Store the current to the previous
                prev = curr
                # Clear the current
                curr = ''

    return transitionProb

def getPreviousTagIndex(previous, transition_array):
    """
    Find the index in the transition array. If the previous tag is not present, returning -1
    :param previous: the previous tag, being searched
    :param transition_array: the transition array
    :return: the index in the transition array
    """
    index = 0

    for previousTagInfo in transition_array:
        if previousTagInfo['previous'] == previous:
            return index
        index += 1
    return -1

def getTotalWordCount(tag_info):
    """
    Count the words in the data file
    :param tag_info: the tag information
    :return: number of words in the data file
    """
    count = 0
    for sentence in tag_info:
        count += len(sentence)
        pass
    return count

def getTransitionCount(transition_count):
    """
    Counting the number of transtion in the transition_count
    :param transition_count: the transition dictionary
    :return: number of transitions
    """
    count = 0
    for curr, previousInfoList in transition_count.iteritems():
        for previousObj in previousInfoList:
            count += previousObj['count']
    return count


def getTagCount(transition_count):
    """
    Calculate the number of times a particular tag occurs
    :param transition_count: the transition from 'a tag' to 'another tag'
    :return: a dict representing the nubmer of times a 'tag' occurred in the data
    """
    tag_count = {}
    for tag in transition_count:
        count = 0
        for previousTag in transition_count[tag]:
            count += previousTag['count']
        tag_count[tag] = count

    return tag_count

def getTransitionProb(transition_count, tagcount):
    """
    Get the transition probability from a tag to another tag
    :param transition_count: the transition counts from 'a tag' to 'another tag'
    :param tagcount: the total number of times tag occur
    :return: a dict representing the prob that 'a tag' goes to 'another tag'
    """
    transition_prob = {}
    for tag in transition_count:
        next_tag_prob = []
        for previousTag in transition_count[tag]:
            probability = previousTag['count'] / float(tagcount[tag])
            tag_prob = {
                'previous': previousTag['previous'],
                'prob': probability
            }
            next_tag_prob.append(tag_prob)
        transition_prob[tag] = next_tag_prob
    return transition_prob

def getWordCount(tag_info):
    """
    Calculating the number of times a word occurs in the data file
    :param tag_info: the tag information in the data file
    :return: the dict representing the number of times a word occurs
    """
    word_count = {}
    for sentence in tag_info:
        for word in sentence:
            if word['word'] in word_count:
                word_count[word['word']] += 1
            else:
                word_count[word['word']] = 1

    return word_count


def getEmissionCount(tag_info):
    """
    Computing the emission probability
    :param tag_info: the tag information in the data file
    :return: currently nothing
    """
    word_count = getWordCount(tag_info)


    # {word : [{tag1: count1}, {tag2: count2}]...}
    word_tags = {}

    for sentence in tag_info:
        for wordtag in sentence:
            word = wordtag['word']
            tag = wordtag['tag']

            # If the word has not been seen ever
            if word not in word_tags:
                tag_count = {
                    'tag': tag,
                    'count': 1
                }
                word_tags[word] = [tag_count]
            # else, already seen the word
            else:
                tags_count = word_tags[word]

                # If I have also seen the tag already for the word in consideration
                for tag_count in tags_count:
                    if tag_count['tag'] == tag:
                        tag_count['count'] += 1
                        break
                # If I could not find the tag for the word
                else:
                    tag_count = {
                        'tag': tag,
                        'count': 1
                    }
                    tags_count.append(tag_count)

    return word_tags

def getTotalEmissionCount(emission_count):
    """
    Calculating the sum of all the emissions
    :param emission_count: The emission of the tags
    :return: the sum of all the emissions
    """
    count = 0
    for word, tags in emission_count.iteritems():
        for tag in tags:
            count += tag['count']
    return count


def getEmissionTagCount(emission_tag):
    """
    Getting the number of tags the word has
    :param emission_tag: the emission list for the word
    :return: the total number of tag
    """
    count = 0
    for tag in emission_tag:
        count += tag['count']
    return count

def getEmissionProb(emission_count):
    """
    Calculating the emission probabilities for each of the word
    :param emission_count: the emission list for the word
    :return: the emission probability of each word
    """
    emission_prob = {}
    for word, word_emissions in emission_count.iteritems():
        emission_list = []
        total = float(getEmissionTagCount(word_emissions))
        for word_emission in word_emissions:
            prob = {
                'tag': word_emission['tag'],
                'prob':word_emission['count'] / total
            }
            emission_list.append(prob)
        emission_prob[word] = emission_list

    return emission_prob


if __name__ == '__main__':

    num_of_args = len(sys.argv)

    if num_of_args == 2:
        filename = sys.argv[1]
    start = datetime.datetime.now()

    # Tag Information
    tag_info = getTagInfo(filename)

    # First Tag Count
    starting_tag_count = getStartingTagCount(tag_info)

    # If we found the correct number of starting tag
    if isStartProbCorrect(tag_info, starting_tag_count):

        # Starting Probability
        starting_prob = getStartProb(starting_tag_count, len(tag_info))

        # Transition Count
        POS_transition_count = getPOSTransitionCount(tag_info)

        # Total number of words
        word_count = getTotalWordCount(tag_info)

        # Total number of transitions
        transition_count = getTransitionCount(POS_transition_count)

        # Expected number of transitions
        expected_transition = word_count - len(tag_info)

        # If missed any transitions!
        if expected_transition == transition_count:
            # Total number of tags in the data
            tag_count = getTagCount(POS_transition_count)

            # Computing the transition probability
            transition_prob = getTransitionProb(POS_transition_count, tag_count)

            # Emission count for every tag
            emission_count = getEmissionCount(tag_info)

            # Total number of emissions
            total_emmission_count = getTotalEmissionCount(emission_count)

            if word_count == total_emmission_count:
                emission_prob = getEmissionProb(emission_count)
                with open('hmm_model.txt', 'w') as file:
                    pickle.dump([starting_prob, transition_prob, emission_prob], file)
            else:
                raise ValueError('Error in calculation of emmission probilities')
        else:
            raise ValueError('Error in calculation of the transitions probabilities')
    else:
        raise ValueError('Error in calculation of starting probabilities')

    end = datetime.datetime.now()
    print 'Took ' + str(end-start) + ' time.'

