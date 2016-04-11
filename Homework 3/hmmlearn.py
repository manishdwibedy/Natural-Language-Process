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

def getStartingProb(tag_info):
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

if __name__ == '__main__':
    start = datetime.datetime.now()

    tag_info = getTagInfo(constant.DEV_TAGGED_DATA)
    starting_prob = getStartingProb(tag_info)

    end = datetime.datetime.now()
    print 'Took ' + str(end-start) + ' time.'

