import util
import constant

def getTagInfo(filename):
    """
    Getting the tag information from the data file
    :param filename: The name of the data file
    :return: the list of object, where each object would be dict representing tag and word
    """
    return util.getTaggedWords(filename)

if __name__ == '__main__':
    tag_info = getTagInfo(constant.DEV_TAGGED_DATA)

