import os

def changeToPresentDirectory():
    '''
    Changing to the current directory.
    :return:
    '''
    os.path.abspath(os.curdir)


def getCurrentPath():
    return os.getcwd()

if __name__ == '__main__':
    changeToPresentDirectory()
    print getCurrentPath()
