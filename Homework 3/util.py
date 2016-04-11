import os

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

if __name__ == '__main__':
    changeToPresentDirectory()
    print getCurrentPath()
