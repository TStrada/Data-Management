#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
import numpy as np
import os
from random import random


# In[7]:


## Build fake dataset containing all attributes needed
# os.getcwd()
# os.chdir('..')
# os.getcwd()
songsterr = pd.read_csv('Dataset_Analysis/Dataset_Songs_Features.csv', index_col = 'Unnamed: 0')
print(songsterr.head(5))
fake = songsterr.copy()


# In[26]:


from random import seed
from random import choice
# # seed random number generator
# seed(1)
# # prepare a sequence
# sequence = [i for i in range(20)]
# print(sequence)
# # make choices from the sequence
# for _ in range(5):
# 	selection = choice(sequence)
# 	print(selection)
# for i in range(len(fake)):
#     print(round(random(), 2)) 


fake['Spotify danceability'] = [round(random(), 2) for i in range(len(fake))] 
fake['Spotify energy'] = [round(random(), 2) for i in range(len(fake))]
fake['Spotify loudness'] = [round(random(), 2) for i in range(len(fake))]
fake['Spotify valence'] = [round(random(), 2) for i in range(len(fake))]

level = ['Beginner', 'Intermediate', 'Advanced']
score = [n for n in range(1,9)]

fake['Guitar difficulty'] = fake['Difficulty']
fake['Guitar score'] = fake['Score']
fake['Guitar librosa 1'] = [round(random(), 2) for i in range(len(fake))]
fake['Guitar librosa 2'] = [round(random(), 2) for i in range(len(fake))]

fake['Bass difficulty'] = [choice(level) for i in range(len(fake))]
fake['Bass score'] = [str(choice(score)) + '/8' for i in range(len(fake))]
fake['Guitar librosa 1'] = [round(random(), 2) for i in range(len(fake))]
fake['Guitar librosa 2'] = [round(random(), 2) for i in range(len(fake))]

fake['Drums difficulty'] = [choice(level) for i in range(len(fake))]
fake['Drums score'] = [str(choice(score)) + '/8' for i in range(len(fake))]
fake['Guitar librosa 1'] = [round(random(), 2) for i in range(len(fake))]
fake['Guitar librosa 2'] = [round(random(), 2) for i in range(len(fake))]

fake['Piano difficulty'] = [choice(level) for i in range(len(fake))]
fake['Piano score'] = [str(choice(score)) + '/8' for i in range(len(fake))]
fake['Guitar librosa 1'] = [round(random(), 2) for i in range(len(fake))]
fake['Guitar librosa 2'] = [round(random(), 2) for i in range(len(fake))]


# In[28]:


fake.to_csv('Neo4j/fake_dataset.csv')


# Neo4j structure

# In[ ]:





# In[ ]:




