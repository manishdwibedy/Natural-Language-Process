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

if __name__ == '__main__':
    start = datetime.datetime.now()
    tag_info = getTagInfo(constant.DEV_TAGGED_DATA)
    end = datetime.datetime.now()
    print 'Took ' + str(end-start) + ' time.'

