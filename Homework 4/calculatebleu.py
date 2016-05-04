import sys
import ngrams

class ComputeBLEU(object):
    '''
    This class would compute the BLEU score. To initiate the class, you need to pass
    two arguments /path/to/candidate /path/to/reference to read the candidate and reference files
    '''
    def __init__(self):
        if len(sys.argv) < 3:
            sys.exit('Usage: %s /path/to/candidate /path/to/reference' % sys.argv[0])
        self.candidata_file = sys.argv[1]
        self.reference_file = sys.argv[2]

    def getCandidateNGrams(self):
        '''
        Computation of the N-grams of the candidate file
        '''
        ngram = ngrams.NGrams(self.candidata_file).getNGrams()

        self.candidate_ngrams = ngram

    def getReferenceNGrams(self):
        '''
        Computation of the N-grams of the reference file
        '''
        ngram = ngrams.NGrams(self.reference_file).getNGrams()

        self.reference_ngrams = ngram

    def computeNgrams(self):
        '''
        Computation of the N-grams of the both the reference and candidate files
        '''

        self.getCandidateNGrams()
        self.getReferenceNGrams()


if __name__ == '__main__':
    blue = ComputeBLEU()
    blue.computeNgrams()
    pass