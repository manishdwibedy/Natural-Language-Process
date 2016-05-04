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
            lines = f.readlines()

        self.lines = lines

    def computeNGramsFile(self):
        # Reading the file
        self.readFile()

        self.ngrams = {}

        # For each of the lines
        for line in self.lines:
            # computing the list of words
            words = line.split(' ')

            # If the words are less than 4, only one N-gram is possible
            if len(words) < 4:
                # The only n-gram
                ngram = ' '.join(words).strip()

                if ngram in self.ngrams:
                    self.ngrams[ngram] += 1
                else:
                    self.ngrams[ngram] = 1
            # Otherwise len(words) - 3 number of 4-grams are possible
            else:
                end_index = len(words) - 4
                for index in range(0, end_index):
                    n_words = words[index:index+4]
                    ngram = ' '.join(n_words).strip()
                    if ngram in self.ngrams:
                        self.ngrams[ngram] += 1
                    else:
                        self.ngrams[ngram] = 1

    def getNGrams(self):
        '''
        Returing the n-grams as a dict
        :return: a dict of n-grams with their counts
        '''
        self.computeNGramsFile()

        return self.ngrams

if __name__ == '__main__':
    file_location = 'data/candidate-1.txt'
    print NGrams(file_location).getNGrams()