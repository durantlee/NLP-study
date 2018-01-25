import numpy as np
import sys
import argparse
import os
import json
import string
import csv

'''
Load supported file
'''
#fp_path = '/u/cs401/Wordlists/First-person'
dev_fp_path = '../Wordlists/First-person'
fp_file = open(dev_fp_path)
fp = fp_file.readlines()
fp = [i.replace("\n","") for i in fp]
#sp_path = '/u/cs401/Wordlists/Second-person'
dev_sp_path = '../Wordlists/Second-person'
sp_file = open(dev_sp_path)
sp = sp_file.readlines()
sp = [i.replace("\n","") for i in sp]
#tp_path = '/u/cs401/Wordlists/Third-person'
dev_tp_path = '../Wordlists/Third-person'
tp_file = open(dev_tp_path)
tp = tp_file.readlines()
tp = [i.replace("\n","") for i in tp]
#slang_path = '/u/cs401/Wordlists/Slang'
dev_slang_path = '../Wordlists/Slang'
slang_file = open(dev_slang_path)
slang = slang_file.readlines()
slang = [i.replace("\n","") for i in slang]
#slang_path = '/u/cs401/Wordlists/Slang'
dev_slang_path = '../Wordlists/Slang'
slang_file = open(dev_slang_path)
slang = slang_file.readlines()
slang = [i.replace("\n","") for i in slang]
#BNG_path = '/u/cs401/Wordlists/BristolNorms+GilhoolyLogie.csv'
dev_BNG_path = '../Wordlists/BristolNorms+GilhoolyLogie.csv'
BNG_file = csv.reader(open(dev_slang_path))
BNG = np.array([row for row in BNG_file][1:])
#RW_path = '/u/cs401/Wordlists/Ratings_Warriner_et_al.csv'
dev_RW_path = '../Wordlists/Ratings_Warriner_et_al.csv'
RW_file = csv.reader(open(dev_RW_path))
RW = np.array([row for row in RW_file][1:])



#some helpful tags for future regex
common_nouns = ['NN', 'NNS']
proper_nouns = ['NNP', 'NNPS']
adverbs = ['RB', 'RBR', 'RBS']
wh = ['WDT', 'WP', 'WP$', 'WRB']



def extract1( comment ):
    ''' This function extracts features from a single comment

    Parameters:
        comment : string, the body of a comment (after preprocessing)

    Returns:
        feats : numpy Array, a 173-length vector of floating point features
    '''

    feats = np.zeros(173)
    comment = comment.split(" ")
    len_comment = 0.0
    no_of_token = 0.0
    no_of_sen = 0.0
    AoA = []


    for i in comment:
        #some feature need to calculate regardless of words
        len_comment += len(i)
        no_of_token +=1
        if '.\n' in i:
            no_of_sen += 1
            continue

        #need to think a better way but should be enough for now
        if any(j +'/PRP' in i for j in fp) \
                or any(k +'/PRP$' in i for k in fp):
            feats[0] +=1
            continue
        if any(j + '/PRP' in i for j in sp) \
                or any(k + '/PRP$' in i for k in sp):
            feats[1] +=1
            continue
        if any(j + '/PRP' in i for j in tp) \
                or any(k + '/PRP$' in i for k in tp):
            feats[2] +=1
            continue
        if '/CC' in i:
            feats[3] +=1
            continue
        if '/VBD' in i:
            feats[4] +=1
            continue
        if '/VBG' in i:
            feats[5] +=1
            continue
        if i == ',/,':
            feats[6] +=1
            continue
        if i[0] in string.punctuation and i[1] in string.punctuation:
            feats[7] +=1
            continue
        if any(n in i for n in common_nouns):
            feats[8] +=1
        if any(pn in i for pn in proper_nouns):
            feats[9] +=1
        if any(ad in i for ad in adverbs):
            feats[10] +=1
        if any(w in i for w in wh):
            feats[11] +=1
        if any(sl in i for sl in slang):
            feats[12] +=1
        if len(i.split('/')[0])>=3 and i.split('/')[0].isupper():
            feats[13] +=1

    #average length of sentence,tokens
    feats[14] = no_of_token/(no_of_sen if no_of_sen != 0 else 1)
    feats[15] = len_comment/(no_of_token if no_of_token != 0 else 1)
    feats[16] = no_of_sen

    #norm: average, sd





    return feats



def main( args ):

    data = json.load(open(args.input))
    feats = np.zeros( (len(data), 173+1))

    # TODO: your code here
    np.savez_compressed( args.output, feats)

    
if __name__ == "__main__": 

    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument("-o", "--output", help="Directs the output to a filename of your choice", required=True)
    parser.add_argument("-i", "--input", help="The input JSON file, preprocessed as in Task 1", required=True)
    args = parser.parse_args()
                 

    main(args)

