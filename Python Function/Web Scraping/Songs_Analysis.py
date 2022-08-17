#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import re
import os
from ast import literal_eval


# In[5]:


df = pd.read_csv('Dataset_Songs_Features.csv', index_col = 'Unnamed: 0')
## Read Technque rows as list
df.Technique = df.Technique.apply(literal_eval)
df.head(5)


# Some analysis:
# - Controlla duplicati
# - Controlla se ci sono ripetizioni di Band in Song, Song in Player, Player in Technique
# - Controlla Difficulty e Score

# In[8]:


## Shape df
print('Original Dataset: {} rows | {} columns'.format(len(df), len(df.columns)))
print(' ')

## Check duplicated
dup = df.loc[df.duplicated(subset=['Band', 'Song', 'Player']) == True]
print('N° duplicates: {}'.format(len(dup)))
df.drop_duplicates(subset=['Band', 'Song', 'Player'], inplace = True)
print('No duplicates Dataset: {} rows | {} columns'.format(len(df), len(df.columns)))


# In[10]:


## Control if there are repetition in consecutive columns
## Define function: object will be every rows

def repetition_col(x):
    
    columns=  df.columns
    band = [x[columns[0]]] 
    song = [x[columns[1]]]
    player = [x[columns[2]]]
    technique = x[columns[3]]
    
    errors = 0
    ok = 0
    
    if band in song or song in player or player in technique:
        errors += 1
        print('Repetition')
    else:
        ok += 1
    
    return(errors, ok)


# In[12]:


dt = pd.DataFrame(df.apply(lambda x: repetition_col(x), axis = 1).to_list(), columns = ['Errors', 'Ok'])
print('Len dataset: {}'.format(len(df)))
print('N° right divisions: ', dt.groupby('Errors').sum().values[0][0])
print('N° wrong divisions: ', dt.groupby('Ok').sum().values[0][0])
## There aren't repetitions


# In[116]:


## Check there are some wrong splits between Player and Technique
technique = []
# index = []
def unique_el(x):
    
    for el in x:
        technique.append(el)
#         print(x.index)
#         index.append(i)
#     print(technique)
    return(technique)


## Define function for empty list
na = 0
def empty_list(x):
    if len(x) == 0:
        na += 1
    return na 


df['Technique'].apply(lambda x: unique_el(x))


# In[74]:


len_ls = df['Technique'].apply(lambda x: len(x))
len(len_ls[len_ls == 0]) + 6646

print('Total element: {} |'.format(len(technique)), 
      'N° empty list: {} |'.format(len(len_ls[len_ls == 0])),
      'Possible elements: {} |'.format(len(technique) + len(len_ls[len_ls == 0])),
      'Max n° technique for song: {} |'.format(len_ls.unique().max()),
      'Lenght Dataset: {}'.format(len(df)))


# In[75]:


## Technique
style = pd.Series(technique).unique()
print('N° Technique: {}'.format(len(style)))
style
## There are many techniques with transcriptive mistakes. Others actually are players.


# In[76]:


## Make uniform styles
## Divide for instruments
basic_instruments = ['Guitar', 'Bass', 'Drums', 'Piano']
other_instruments = ['Accordion',
                     'Bag pipe', 
                     'Banjo', 
                     'Bugle', 
                     'Cello', 
                     'Clarinet', 
                     'Cymbals', 
                     'Bongo Drums', 
                     'French horn', 
                     'Harmonica', 
                     'Harp',
                     'Keyboard', 
                     'Maracas', 
                     'Organ',
                     'Pan Flute',
                     'Recorder', 
                     'Saxophone', 
                     'Sitar', 
                     'Tambourine',
                     'Triangle', 
                     'Trombone', 
                     'Trumpet',
                     'Tuba',
                     'Ukulele', 
                     'Violin', 
                     'Xylophone', 
                     'Bassoon',
                     'Castanets',
                     'Didgeridoo',
                     'Double', 
                     'Gong',
                     'Harpsichord',
                     'Lute',
                     'Mandolin',
                     'Oboe',
                     'Piccolo',
                     'Viola', 
                     'Distortion', 
                     'Sax', 
                     'Horn', 
                     'Fuzz', 
                     'Keys', 
                     'Lead',
                     'FX', 
                     'Pad', 
                     'Synth', 
                     'String',
                     'Rythm', 
                     'Riff',
                     'Solo', 
                     'Hand', 
                     'Vocal', 
                     'Voice' ,
                     'Drop'
]

re_basic_instruments = [re.compile('({})'.format(instrument[1:])) for instrument in basic_instruments]
re_basic_instruments

guitar = []
bass = [] 
drums = [] 
piano = []
others = []

def instrumental_division(x):
    
    if re_basic_instruments[0].findall(x):
        guitar.append(x)
    if re_basic_instruments[1].findall(x):
        bass.append(x)
    if re_basic_instruments[2].findall(x):
        drums.append(x)
    if re_basic_instruments[3].findall(x):
        piano.append(x)
    else:
        for instr in other_instruments:
            if re.findall('({})'.format(instr[1:]), x):
                others.append(x)
    
    return(guitar, bass, drums, piano, others)
    
    

pd.Series(style).apply(lambda x: instrumental_division(x))  


# In[77]:


## Check if instruments are in different list
togheter = len(guitar) + len(piano) + len(drums) + len(bass) + len(others)
print('Guitar: {} |'.format(len(guitar)),
      'Piano: {} |'.format(len(piano)),
      'Drums: {} |'.format(len(drums)),
      'Bass: {} |'.format(len(bass)),
      'Others: {} |'.format(len(others)),
      'Togheter: {} |'.format(togheter),
      'All: {} |'.format(len(style)), 
      'All - Togheter: {}'.format(len(style) - togheter))

all_instr = [guitar, bass, piano, drums]
for n in range(len(all_instr)):
    print(basic_instruments[n])
    print(set(all_instr[n]).intersection(set(others)))

    
## Define other matches list
style1 = style.copy()
others = set(others) - set(guitar) - set(bass)
togheter_clean = len(guitar) + len(piano) + len(drums) + len(bass) + len(others)

print('Others clean: {}'.format(len(others)), 
      'Togheter: {} |'.format(togheter_clean),
      'All: {} |'.format(len(style)), 
      'All - Togheter: {}'.format(len(style) - togheter_clean))


mismatch = set(style1) - set(guitar) - set(drums) - set(piano) - set(bass) - set(others)
print('N° mismatch instrumentes: {}'.format(len(mismatch)))
# other


# In[78]:


for i, x in enumerate(df['Technique']):
    print(i, type(x))

