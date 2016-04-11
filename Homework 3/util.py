import os
import constant

def changeToPresentDirectory():
    '''
    Changing to the current directory.
    :return:
    '''
    os.path.abspath(os.curdir)


def getCurrentPath():
    '''
    Returning the current directory
    :return: The current directory
    '''
    return os.getcwd()

def getDataDirectory():
    '''
    Getting the data directory
    :return: Returns the data directory's absolute path
    '''
    return os.path.join(getCurrentPath(), constant.DATA_DIR)

def readData(filename):
    '''
    Readging the data file, specified by the filename
    :param filename: The filename to be read
    :return: A list containing every line in the file
    '''

    # File Content list
    fileContents = []

    # Generating the file's absolute path
    path = os.path.join(getDataDirectory(), filename)

    with open(path) as file:
        for line in file:
            fileContents.append(line)

    return fileContents


if __name__ == '__main__':
    # changeToPresentDirectory()
    # print getCurrentPath()
    print readData('catalan_corpus_dev_tagged.txt')
