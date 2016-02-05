import sys

# get the possible permutations of a given parameter, word
def getWords(word):
    # Base case : if the word is a single alphabet, the only possible
    # permutations is the alphabet itself, return the word itself.
    if len(word) == 1:
        return [word]

    # Storing the word in a dictionary to avoid store duplicate keys
    words = {}

    # Would loop through the characters of the word
    for char in word:
        # Delete the first occurance of the alphabet in consideration
        remaining_word = word.replace(char, '',1);

        # Calculate the permutations of the remaining word
        permutations = getWords(remaining_word)

        # The permutations of the words now is the character along with every
        # possible permutations of the remaining word
        for permutation in permutations:
            # Inserting the permutation(char + permutation) into the
            # dictionary to avoid duplicates
            words[char + permutation] = 1
    # returning the set of keys i.e. the permutations of the word
    return words.keys()

if len(sys.argv) != 2:
    print "Missing the word as a parameter"
else:
    word = sys.argv[1]
    words = getWords(word)

    print "Found " + str(len(words)) + " possible permutations.\n"
    words.sort()
    output = open('anagram_out.txt', 'w')

    for word in words:
        output.write(word + '\n')
