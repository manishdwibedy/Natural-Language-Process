import codecs

class NGrams(object):
    def __init__(self, n, filename):
        self.filename = filename
        self.n = n

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

        self.ngrams = []

        # For each of the lines
        for line in self.lines:
            line_ngrams = {}

            # computing the list of words
            words = line.strip().split(' ')

            # If the words are less than 4, only one N-gram is possible
            if len(words) < self.n:
                # The only n-gram
                ngram = ' '.join(words).strip()

                if ngram in line_ngrams:
                    line_ngrams[ngram] += 1
                else:
                    line_ngrams[ngram] = 1

            # Otherwise len(words) - 3 number of 4-grams are possible
            else:
                end_index = len(words) - self.n
                for index in range(0, end_index):
                    n_words = words[index:index+self.n]
                    ngram = ' '.join(n_words).strip()
                    if ngram in line_ngrams:
                        line_ngrams[ngram] += 1
                    else:
                        line_ngrams[ngram] = 1
            self.ngrams.append(line_ngrams)

    def getNGrams(self):
        '''
        Returing the n-grams as a dict
        :return: a dict of n-grams with their counts
        '''
        self.computeNGramsFile()

        return self.ngrams

if __name__ == '__main__':
    file_location = 'data/book_data/reference-1.txt'
    ngrams =  NGrams(1, file_location).getNGrams()
    print ngrams