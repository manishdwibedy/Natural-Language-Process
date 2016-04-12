import pickle

def getHMMModel(filename):
    """
    Get the HMM model from the file
    :param filename: the file's path
    :return: the starting, transmission and emission probabilities
    """
    with open(filename) as file:
        starting_prob, transition_prob, emission_prob = pickle.load(file)
    return starting_prob, transition_prob, emission_prob

if __name__ == '__main__':
    starting_prob, transition_prob, emission_prob = getHMMModel('hmm_model.txt')
