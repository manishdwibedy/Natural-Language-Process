import codecs

class NGrams(object):
    def __init__(self, filename):
        self.filename = filename

    def readFile(self):
        lines = []

        with codecs.open(self.filename,'r',encoding='utf8') as f:
            self.lines = f.readlines()
            pass

    def computeNGrams(self):
        self.readFile()
        for line in self.lines:
            print line

if __name__ == '__main__':
    file_location = 'data/candidate-1.txt'
    NGrams(file_location).computeNGrams()