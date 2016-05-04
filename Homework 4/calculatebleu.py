import sys
import ngrams
import math

class ComputeBLEU(object):
    '''
    This class would compute the BLEU score. To initiate the class, you need to pass
    two arguments /path/to/candidate /path/to/reference to read the candidate and reference files
    '''
    def __init__(self):
        self.nRange = range(1,5)
        if len(sys.argv) < 3:
            sys.exit('Usage: %s /path/to/candidate /path/to/reference' % sys.argv[0])
        self.candidata_file = sys.argv[1]
        self.reference_file = sys.argv[2]

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
        ngram = ngrams.NGrams(n, self.reference_file).getNGrams()

        self.reference_ngrams = ngram

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

        if candidate_word_count <= reference_word_count:
            ratio = reference_word_count / candidate_word_count
            BP = math.exp( 1 - ratio )
        else:
            BP = 1

        BLEU_Score = 0
        for result_item in result:
            p_n = math.log(result_item)
            w_n = (1.00/len(result))
            BLEU_Score += (p_n * w_n)

        BLEU_Score = math.exp(BLEU_Score)
        BLEU_Score *= BP
        print BLEU_Score

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