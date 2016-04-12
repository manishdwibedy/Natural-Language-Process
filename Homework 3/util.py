import os
import constant

def changeToPresentDirectory():
    """
    Changing to the current directory.
    :return:
    """
    os.path.abspath(os.curdir)


def getCurrentPath():
    """
    Returning the current directory
    :return: The current directory
    """
    return os.getcwd()

def getDataDirectory():
    """
    Getting the data directory
    :return: Returns the data directory's absolute path
    """
    return os.path.join(getCurrentPath(), constant.DATA_DIR)

def readData(filename):
    """
    Readging the data file, specified by the filename
    :param filename: The filename to be read
    :return: A list containing every line in the file
    """

    # File Content list
    fileContents = []

    # Generating the file's absolute path
    path = os.path.join(getDataDirectory(), filename)

    with open(path) as file:
        for line in file:
            fileContents.append(line.strip())

    return fileContents

def getTaggedWords(filename):
    """
    Getting all the tagged information for the data file
    :param filename: Name of the data file
    :return: the tag information
    """
    tag_info_list = []

    # Getting all the content of the file
    fileContents = readData(filename)

    # For every sentence in the file
    for sentance in fileContents:

        tag_info_sentence = []
        # Split using space as a delimiter, as per the homework doc
        # A file with tagged training data in the word/TAG format,
        # with words separated by 'spaces' and each sentence on a new line.
        tagged_words = sentance.split(' ')

        for tagged_word in tagged_words:
            # Extracting the word and te tag using the '/' character
            word = tagged_word[:tagged_word.rfind('/')]
            tag = tagged_word[tagged_word.rfind('/')+1:]

            if len(tag) == 2:
                tag_info = {
                    'word': word,
                    'tag': tag
                }
                tag_info_sentence.append(tag_info)
            else:
                print 'Error : Getting wrong tag'

        tag_info_list.append(tag_info_sentence)
    return tag_info_list


if __name__ == '__main__':
    # changeToPresentDirectory()
    # print getCurrentPath()
    tag_info = getTaggedWords(constant.DEV_TAGGED_DATA)
    pass
