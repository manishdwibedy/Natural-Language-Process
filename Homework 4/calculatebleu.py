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

    def computeBLUE(self):
        '''

        Computation of the BLEU score
        '''

        result = []
        for n in self.nRange:
            self.computeNgrams(n)

            ngram_BLEU_Score = 0
            for lineNumber, line in enumerate(self.candidate_ngrams):
                line_BLEU_score = 0
                for candidate_ngram, candidate_count in line.iteritems():
                    reference_line = self.reference_ngrams[lineNumber]
                    # the ngram is present in the reference line, as well
                    if candidate_ngram in reference_line:
                        count = min(candidate_count, self.reference_ngrams[lineNumber][candidate_ngram])
                        line_BLEU_score += float(count)
                ngram_BLEU_Score += line_BLEU_score
            part_result = ngram_BLEU_Score / self.getWords(self.candidate_ngrams)
            result.append({
                'result': part_result,
                'candidateLength': self.getWords(self.candidate_ngrams),
                'referenceLength': self.getWords(self.reference_ngrams),
            })
            # result.append(part_result)

        BLEU_Score = 0
        for result_item in result:
            reference_length = result_item['referenceLength']
            candidate_length = result_item['candidateLength']
            if candidate_length <= reference_length:
                ratio = reference_length / candidate_length
                BP = math.exp( 1 - ratio )
            else:
                BP = 1
            BLEU_Score += BP * math.log(result_item['result']+1)

        BLEU_Score /= len(result)
        print BLEU_Score

    def getWords(self, ngram):
        word_count = 0
        symbols = '!$%^&*()_+|~-=`{}[]:";<>?,./'

        symbol_list = []
        for symbol in symbols:
            symbol_list.append(symbol)
        for ngam_line in ngram:
            for ngram_token, count in ngam_line.iteritems():
                if ngram_token not in symbol_list:
                    word_count += count
        return word_count
if __name__ == '__main__':
    blue = ComputeBLEU()
    blue.computeBLUE()
    pass