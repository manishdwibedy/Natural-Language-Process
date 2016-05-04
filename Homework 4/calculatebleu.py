import sys
import ngrams

class ComputeBLEU(object):
    '''
    This class would compute the BLEU score. To initiate the class, you need to pass
    two arguments /path/to/candidate /path/to/reference to read the candidate and reference files
    '''
    def __init__(self, n):
        self.n = n
        if len(sys.argv) < 3:
            sys.exit('Usage: %s /path/to/candidate /path/to/reference' % sys.argv[0])
        self.candidata_file = sys.argv[1]
        self.reference_file = sys.argv[2]

    def getCandidateNGrams(self):
        '''
        Computation of the N-grams of the candidate file
        '''
        ngram = ngrams.NGrams(self.n, self.candidata_file).getNGrams()

        self.candidate_ngrams = ngram

    def getReferenceNGrams(self):
        '''
        Computation of the N-grams of the reference file
        '''
        ngram = ngrams.NGrams(self.n, self.reference_file).getNGrams()

        self.reference_ngrams = ngram

    def computeNgrams(self):
        '''
        Computation of the N-grams of the both the reference and candidate files
        '''

        self.getCandidateNGrams()
        self.getReferenceNGrams()

    def computeBLUE(self):
        '''

        Computation of the BLEU score
        '''
        self.computeNgrams()

        BLEU_Score = 0
        for lineNumber, line in enumerate(self.candidate_ngrams):
            line_BLEU_score = 0
            for candidate_ngram, candidate_count in line.iteritems():
                reference_line = self.reference_ngrams[lineNumber]
                # the ngram is present in the reference line, as well
                if candidate_ngram in reference_line:
                    count = min(candidate_count, self.reference_ngrams[lineNumber][candidate_ngram])
                    num_of_words = self.getWords(line)
                    line_BLEU_score += float(count) / num_of_words
            print 'Line - ' + str(lineNumber)
            print line_BLEU_score
            # print line_BLEU_score
            BLEU_Score += line_BLEU_score
        print BLEU_Score / len(self.candidate_ngrams)

    def getWords(self, ngram):
        word_count = 0
        for ngram_token, count in ngram.iteritems():
            word_count += count
        return word_count
if __name__ == '__main__':
    n = 2
    blue = ComputeBLEU(n)
    blue.computeBLUE()
    pass