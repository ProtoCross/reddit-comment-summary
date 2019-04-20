# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 20:18:16 2019

@author: Josh
"""

import praw
from info import ID, SECRET

reddit = praw.Reddit(client_id=ID,
                     client_secret=SECRET,
                     user_agent='web_mining')
submission = reddit.submission(id='3g1jfi')

for top_level_comment in submission.comments:
    print(top_level_comment.body)