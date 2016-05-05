import sys
import ngrams
import math
import os

class ComputeBLEU(object):
    '''
    This class would compute the BLEU score. To initiate the class, you need to pass
    two arguments /path/to/candidate /path/to/reference to read the candidate and reference files
    '''
    def __init__(self):
        self.nRange = range(1,5)
        curretDirectory = os.path.dirname(os.path.abspath(__file__))
        if len(sys.argv) < 3:
            sys.exit('Usage: %s /path/to/candidate /path/to/reference' % sys.argv[0])
        self.candidata_file = os.path.join(curretDirectory, sys.argv[1])
        self.reference_file = os.path.join(curretDirectory, sys.argv[2])

        if os.path.isdir(self.reference_file):
            self.multipleReferences = True
        else:
            self.multipleReferences = False



    def getCandidateNGrams(self, n):
        '''
        Computation of the N-grams of the candidate file
        '''
        ngram = ngrams.NGrams(n, self.candidata_file).getNGrams()

        self.candidate_ngrams = ngram

    def getReferenceNGrams(self, n):
        '''
        Computation of the N-grams of the reference file
        '''

        # Dealing with a single reference file
        if not self.multipleReferences:
            ngram = ngrams.NGrams(n, self.reference_file).getNGrams()
            self.reference_ngrams = ngram
        else:
            for root, dirs, files in os.walk(self.reference_file, topdown=False):
                for name in files:
                    print(os.path.join(root, name))

    def computeNgrams(self, n):
        '''
        Computation of the N-grams of the both the reference and candidate files
        '''

        self.getCandidateNGrams(n)
        self.getReferenceNGrams(n)

    def compute_blue_ngrams(self):
        candidate_word_count = 0
        reference_word_count = 0

        result = []

        for n in self.nRange:
            self.computeNgrams(n)

            if n == 1:
                reference_word_count = self.getWordCountFile(self.reference_ngrams)
                candidate_word_count = self.getWordCountFile(self.candidate_ngrams)

            ngram_BLEU_Score = 0
            for candidate_line_index, candidate_line in enumerate(self.candidate_ngrams):
                line_BLEU_score = 0
                reference_line = self.reference_ngrams[candidate_line_index]

                for candidate_ngram, candidate_count in candidate_line.iteritems():
                    # the ngram is present in the reference line, as well
                    if candidate_ngram in reference_line:
                        count = min(candidate_count, self.reference_ngrams[candidate_line_index][candidate_ngram])
                        line_BLEU_score += float(count)
                ngram_BLEU_Score += line_BLEU_score
            part_result = ngram_BLEU_Score / self.getWordCountFile(self.candidate_ngrams)
            result.append(part_result)
        return candidate_word_count, reference_word_count, result
    def computeBLUE(self):
        '''

        Computation of the BLEU score
        '''

        candidate_word_count, reference_word_count, result = self.compute_blue_ngrams()

        BLEU_Score = 0
        for result_item in result:
            p_n = math.log(result_item)
            w_n = (1.00/len(result))
            BLEU_Score += (p_n * w_n)

        BLEU_Score = math.exp(BLEU_Score)
        BLEU_Score *= self.computeBP(candidate_word_count, reference_word_count)
        print BLEU_Score

    def computeBP(self, candidate_word_count, reference_word_count):
        if candidate_word_count <= reference_word_count:
            ratio = reference_word_count / candidate_word_count
            bp = math.exp( 1 - ratio )
        else:
            bp = 1
        return bp

    def getWordCountLine(self, ngram):
        word_count = 0
        # for ngam_line in ngram:
        for ngram_token, count in ngram.iteritems():
            word_count += count
        return word_count

    def getWordCountFile(self, ngram):
        word_count = 0
        for ngram_line in ngram:
            for ngram_token, count in ngram_line.iteritems():
                word_count += count
        return word_count
if __name__ == '__main__':
    blue = ComputeBLEU()
    blue.computeBLUE()
    pass