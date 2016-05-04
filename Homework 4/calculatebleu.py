import sys
import ngrams

class ComputeBLEU(object):
    def __init__(self):
        if len(sys.argv) < 3:
            sys.exit('Usage: %s /path/to/candidate /path/to/reference' % sys.argv[0])
        self.candidata_file = sys.argv[1]
        self.reference_file = sys.argv[2]

    def getCandidateNGrams(self):
        ngram = ngrams.NGrams(self.candidata_file).getNGrams()

        self.candidate_ngrams = ngram

    def getReferenceNGrams(self):
        ngram = ngrams.NGrams(self.reference_file).getNGrams()

        self.reference_ngrams = ngram

    def computeNgrams(self):
        self.getCandidateNGrams()
        self.getReferenceNGrams()

if __name__ == '__main__':
    blue = ComputeBLEU()
    blue.computeNgrams()
    pass