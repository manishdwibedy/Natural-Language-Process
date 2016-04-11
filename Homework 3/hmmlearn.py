import util
import constant
import datetime

def getTagInfo(filename):
    """
    Getting the tag information from the data file
    :param filename: The name of the data file
    :return: the list of object, where each object would be dict representing tag and word
    """
    return util.getTaggedWords(filename)

def getStartingTagCount(tag_info):
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

if __name__ == '__main__':
    start = datetime.datetime.now()

    tag_info = getTagInfo(constant.DEV_TAGGED_DATA)
    starting_prob = getStartingTagCount(tag_info)
    if isStartProbCorrect(tag_info, starting_prob):
        pass

    end = datetime.datetime.now()
    print 'Took ' + str(end-start) + ' time.'

