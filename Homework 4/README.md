 **Implementing BLEU evaluation metric for multiple languages**

 
 We implemented a program that calculates the BLEU evaluation metric, as defined in Papineni, Roukos, Ward and Zhu (2002): Bleu: a Method for Automatic Evaluation of Machine Translation, ACL 2002. 
 
 We ran the program on sets of candidate and reference translations, and calculated the BLEU score for each candidate. 
 
 Further we calculated how closely our calculated BLEU score matches the true BLEU score.
 
 We used the data in the following languages:
 1. German
 2. Greek
 3. Portuguese
 4. English
 
 The data file for the above languages and the true BLEU score is as follows:
 
 	        Candidate	        Reference	        BLEU score
German	    candidate-1.txt	    reference-1.txt	    0.151184476557
Greek	    candidate-2.txt	    reference-2.txt	    0.0976570839819
Portuguese	candidate-3.txt	    reference-3.txt	    0.227803041867
English	    candidate-4.txt     reference-4a.txt    0.227894952018
                                reference-4b.txt

