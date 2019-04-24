# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 20:18:16 2019

@author: Josh
"""

import praw
import reddit_modules
from info import ID, SECRET
import pickle

#Create reddit instance
reddit = praw.Reddit(client_id=ID,
                     client_secret=SECRET,
                     user_agent='web_mining')
submission = reddit.submission(id='bg6q6s')

#Pickle the submission for later use
#pickle.dump(submission, open('aww.pkl', 'wb'))

#Store content of comments
sentences = reddit_modules.scrape_comments(reddit, submission)
    
#for f in sentences:
   # print(f)
    
summary = reddit_modules.process_comments(sentences)
print(summary)
reddit_modules.generate_cloud(summary)