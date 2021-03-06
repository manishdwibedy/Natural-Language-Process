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
        self.curretDirectory = os.path.dirname(os.path.abspath(__file__))
        if len(sys.argv) < 3:
            sys.exit('Usage: %s /path/to/candidate /path/to/reference' % sys.argv[0])
        self.candidata_file = os.path.join(self.curretDirectory, sys.argv[1])
        self.reference_file = os.path.join(self.curretDirectory, sys.argv[2])

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
            reference_files = []
            for root, dirs, files in os.walk(self.reference_file, topdown=False):
                for name in files:
                    reference_files.append(os.path.join(root, name))

            ngrams_list = []
            for reference_file in reference_files:
                ngrams_list.append(ngrams.NGrams(n, reference_file).getNGrams())
            self.reference_ngrams = ngrams_list

    def computeNgrams(self, n):
        '''
        Computation of the N-grams of the both the reference and candidate files
        '''

        self.getCandidateNGrams(n)
        self.getReferenceNGrams(n)

    def compute_bleu_ngrams(self):
        if not self.multipleReferences:
            return self.compute_bleu_reference_file()
        else:
            return self.compute_bleu_reference_directory()

    def compute_bleu_reference_file(self):
        result = []
        for n in self.nRange:
            self.computeNgrams(n)

            if n == 1:
                reference_word_count = self.getWordCountFile(self.reference_ngrams)
                candidate_word_count = self.getWordCountFile(self.candidate_ngrams)

            ngram_BLEU_Score = 0
            for candidate_line_index, candidate_line in enumerate(self.candidate_ngrams):
                line_BLEU_score = 0.0
                reference_line = self.reference_ngrams[candidate_line_index]

                for candidate_ngram, candidate_count in candidate_line.iteritems():
                    # the ngram is present in the reference line, as well
                    if candidate_ngram in reference_line:
                        count = min(candidate_count, reference_line[candidate_ngram])
                        line_BLEU_score += count
                ngram_BLEU_Score += line_BLEU_score
            part_result = ngram_BLEU_Score / self.getWordCountFile(self.candidate_ngrams)
            result.append(part_result)
        return candidate_word_count, reference_word_count, result

    def compute_bleu_reference_directory(self):
        result = []
        reference_word_count = 0
        for n in self.nRange:
            self.computeNgrams(n)
            if n == 1:
                candidate_word_count = self.getWordCountFile(self.candidate_ngrams)

                reference_word_count = 0
                for lineIndex in range(len(self.candidate_ngrams)):
                    words_list = []
                    for reference in self.reference_ngrams:
                        words_count = self.getWordCountLine(reference[lineIndex])
                        words_list.append(words_count)
                    reference_word_count += min(words_list)

            ngram_BLEU_Score = 0
            for candidate_line_index, candidate_line in enumerate(self.candidate_ngrams):
                line_BLEU_score = 0
                for candidate_ngram, candidate_count in candidate_line.iteritems():

                    maxCount = -1
                    for reference in self.reference_ngrams:
                        reference_line = reference[candidate_line_index]

                        # the ngram is present in the reference line, as well
                        if candidate_ngram in reference_line:
                            count = min(candidate_count, reference[candidate_line_index][candidate_ngram])
                            if count > maxCount:
                                maxCount = count
                    else:
                        if maxCount > 0:
                            line_BLEU_score += float(maxCount)
                ngram_BLEU_Score += line_BLEU_score
            part_result = ngram_BLEU_Score / self.getWordCountFile(self.candidate_ngrams)
            result.append(part_result)
        return candidate_word_count, reference_word_count, result

    def computeBLEU(self):
        '''

        Computation of the BLEU score
        '''

        candidate_word_count, reference_word_count, result = self.compute_bleu_ngrams()

        BLEU_Score = 0
        for result_item in result:
            p_n = math.log(result_item)
            w_n = (1.00/len(result))
            BLEU_Score += (p_n * w_n)

        BLEU_Score = math.exp(BLEU_Score)
        BLEU_Score *= self.computeBP(candidate_word_count, reference_word_count)
        self.writeOutput(BLEU_Score)
        print BLEU_Score

    def computeBP(self, candidate_word_count, reference_word_count):
        if candidate_word_count <= reference_word_count:
            ratio = float(reference_word_count) / candidate_word_count
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

    def writeOutput(self, bleu_score):
        file_name = 'bleu_out.txt'
        file_location = os.path.join(self.curretDirectory, file_name)
        target = open(file_location, 'w')

        target.write(str(bleu_score))
if __name__ == '__main__':
    blue = ComputeBLEU()
    blue.computeBLEU()
    pass