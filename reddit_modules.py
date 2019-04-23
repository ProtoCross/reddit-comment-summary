# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 19:48:29 2019

@author: Josh
"""

import nltk
import numpy
from nltk.tokenize import sent_tokenize
from praw.models import MoreComments
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def scrape_comments(reddit, submission):
    sentences = []

    #Need to ignore MoreComments error for results to display
    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        sentences.extend(sent_tokenize(top_level_comment.body))
    return sentences

def process_comments(sentences):
    words = list()
    #Tokenize all of the words present
    for sent in sentences:
        words.extend(map(lambda x: x.lower(), nltk.tokenize.word_tokenize(sent)))
    
    #Set stopwords to find end of sentences
    stopwords = set(nltk.corpus.stopwords.words('english'))
    for punct in ",.'?:;’“”":
        stopwords.add(punct)
    freqDist = nltk.FreqDist(words)
    
    N = 12
    
    sorted_terms = sorted(freqDist.items(), key=lambda x: x[1], reverse=True)
    
    #Find the 12 most common words
    n_most_common = [word[0] for word in sorted_terms if word[0] not in stopwords][:N]
    
    summaries = summarize(sentences, n_most_common, 5, 8)
    
    #put 'mean-score' or 'top-n'
    return summaries['mean-score']

#Cluster score based on number of significant words ^2 and total words
def cluster_score(cluster):
    sig_words = len(cluster)
    total_words = cluster[-1] - cluster[0] + 1
    return sig_words ** 2 / total_words

def score_sentences(sentences, important_words, CLUSTER_THRESH=5):
    nltk.download('punkt')
    scores = []
    
    for sent in map(nltk.tokenize.word_tokenize, sentences):
        word_idx = []
        
        #Find the positions of all the important words in a sentence
        for word in important_words:
            if word in sent:
                word_idx.append(sent.index(word))
        word_idx.sort()
        
        #Build clusters based on threshold
        if len(word_idx) > 0:
            clusters = []
            current_cluster = [word_idx[0]]
            for idx in word_idx[1:]:
                #Check to see if the current index is close to previous index
                if idx - word_idx[-1] < CLUSTER_THRESH:
                    current_cluster.append(idx)
                    
                #If it's not, start a new cluster
                else:
                    clusters.append(current_cluster)
                    current_cluster = [idx]
            clusters.append(current_cluster)
            
            #Score clusters, keep track of the largest cluster score
            scores.append(max(map(cluster_score, clusters)))
        #If no important words are present, score 0
        else:
            scores.append(0)
    return scores
 
def summarize(sentences, important_words, CTHRESH=5, TOP_SENTENCES=5):
    #Number of sentences wanted
    N = 5
    
    #Get score threshold based on average and standard deviation
    scores = score_sentences(sentences, important_words, CTHRESH)
    avg = numpy.mean(scores)
    std_dev = numpy.std(scores)
    score_threshold = avg + 0.5 * std_dev
    mean_scored = [t[0] for t in enumerate(scores) if t[1] > score_threshold][:N]
    
    sorted_scores = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:TOP_SENTENCES]
    sorted_indexes = sorted([s[0] for s in sorted_scores])
    
    #Return dictionary of summaries
    return {'top-n': ' '.join([sentences[i] for i in sorted_indexes]),
            'mean-score': ' '.join([sentences[i] for i in mean_scored])}
    
def generate_cloud(summary):
    #Pass summary to wordcloud for generation
    wordcloud = WordCloud(max_font_size = 40).generate(summary)
    plt.figure()
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis('off')
    plt.show()
    return wordcloud