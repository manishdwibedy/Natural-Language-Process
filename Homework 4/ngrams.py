import codecs

class NGrams(object):
    def __init__(self, filename):
        self.filename = filename

    def readFile(self):
        '''
        Reading the file
        :return: Sets the value in the line parameter
        '''
        lines = []

        with codecs.open(self.filename,'r',encoding='utf8') as f:
            self.lines = f.readlines()

    def computeNGramsFile(self):
        # Reading the file
        self.readFile()

        # For each of the lines
        for line in self.lines:
            # computing the list of words
            print line

if __name__ == '__main__':
    file_location = 'data/candidate-1.txt'
    NGrams(file_location).computeNGramsFile()