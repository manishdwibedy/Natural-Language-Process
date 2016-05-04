import sys
import ngrams

class ComputeBLEU(object):
    def __init__(self):
        if len(sys.argv) < 2:
            sys.exit('Usage: %s /path/to/candidate_file' % sys.argv[0])
        self.candidata_file = sys.argv[1]

    def getCandidateNGrams(self):
        ngram = ngrams.NGrams(self.candidata_file).getNGrams()

        self.candidate_ngrams = ngram


if __name__ == '__main__':
    blue = ComputeBLEU()
    pass