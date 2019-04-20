# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 19:48:29 2019

@author: Josh
"""

import praw
import nltk
import pickle
import numpy

def scrape_comments():
    return




def cluster_score(cluster):
    sig_words = len(cluster)
    total_words = cluster[-1] - cluster[0] + 1
    return sig_words ** 2 / total_words

def score_sentences(sentences, important_words, CLUSTER_THRESH=5):
    nltk.download('punkt')
    scores = []
    
    for sent in map(nltk.tokenize.word_tokenize, sentences):
        word_idx = []
        # Find the positions of all the important words in the
        # sentence
        for word in important_words:
            if word in sent:
                word_idx.append(sent.index(word))
        word_idx.sort()
        # Build the clusters based on the cluster threshold
        if len(word_idx) > 0:
            clusters = []
            current_cluster = [word_idx[0]]
            for idx in word_idx[1:]:
                # check to see if the current index is close
                # enough to the previous index
                if idx - word_idx[-1] < CLUSTER_THRESH:
                    current_cluster.append(idx)
                else:
                    # if it's not, start a new cluster
                    clusters.append(current_cluster)
                    current_cluster = [idx]
            clusters.append(current_cluster)
            
            # Score clusters, keep track of the largest cluster score
            # for the sentence
            scores.append(max(map(cluster_score, clusters)))
        else: # a sentence with no important words has a score of 0
            scores.append(0)
    return scores
 
def summarize(sentences, important_words, CTHRESH=5, TOP_SENTENCES=5):
    scores = score_sentences(sentences, important_words, CTHRESH)
    avg = numpy.mean(scores)
    std_dev = numpy.std(scores)
    score_threshold = avg + 0.5 * std_dev
    mean_scored = [t[0] for t in enumerate(scores) if t[1] > score_threshold]
    
    sorted_scores = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:TOP_SENTENCES]
    sorted_indexes = sorted([s[0] for s in sorted_scores])
    
    return {'top-n': ' '.join([sentences[i] for i in sorted_indexes]),
            'mean-score': ' '.join([sentences[i] for i in mean_scored])}
    