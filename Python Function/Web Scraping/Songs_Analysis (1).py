#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import re
import os
from ast import literal_eval


# In[2]:


df = pd.read_csv('Dataset_Songs_Features.csv', index_col = 'Unnamed: 0')
## Read Technque rows as list
df.Technique = df.Technique.apply(literal_eval)
df.tail(50)
## There are many errors splitting 'PLayer' and 'Technique'.
## Many rows have cyrillic characters
## Some rows have invalid Player or/and Band or/and Song.
## Some rows don't have Difficulty level


# Some analysis:
# - Check duplicates
# - Check repetitions in each columns
# - Check Difficulty and Score columns

# In[3]:


## Shape df
print('Original Dataset: {} rows | {} columns'.format(len(df), len(df.columns)))
print(' ')

## Check duplicated
dup = df.loc[df.duplicated(subset=['Band', 'Song', 'Player']) == True]
print('N° duplicates: {}'.format(len(dup)))
df.drop_duplicates(subset=['Band', 'Song', 'Player'], inplace = True)
print('No duplicates Dataset: {} rows | {} columns'.format(len(df), len(df.columns)))


# In[4]:


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


# In[5]:


dt = pd.DataFrame(df.apply(lambda x: repetition_col(x), axis = 1).to_list(), columns = ['Errors', 'Ok'])
print('Len dataset: {}'.format(len(df)))
print('N° right divisions: ', dt.groupby('Errors').sum().values[0][0])
print('N° wrong divisions: ', dt.groupby('Ok').sum().values[0][0])
## There aren't repetitions


# Check how many rows don't have player elements or take mistakes 

# In[6]:


## Make uniform styles
## Divide for instruments
basic_instruments = ['Guitar', 'Bass', 'Drums', 'Piano']
re_basic_instruments = [re.compile('({})'.format(instrument[1:])) for instrument in basic_instruments]
guitar = []
bass = [] 
drums = [] 
piano = []

def instrumental_division(x):
    
    if re_basic_instruments[0].findall(x):
        guitar.append(x)
    if re_basic_instruments[1].findall(x):
        bass.append(x)
    if re_basic_instruments[2].findall(x):
        drums.append(x)
    if re_basic_instruments[3].findall(x):
        piano.append(x)
       
    return(guitar, bass, drums, piano)
    
    

df['Player'].astype(str).apply(lambda x: instrumental_division(x))  


# In[7]:


print('Guitar mistakes: {}'.format(len(guitar)), 
     'Bass mistakes: {}'.format(len(bass)), 
     'Drums mistakes: {}'.format(len(drums)), 
     'Piano mistakes: {}'.format(len(piano)))

##
df['Player'] = df['Player'].astype(str).apply(lambda x: x.strip('[').strip(']'))
df.reset_index(inplace = True)

instruments = drums + guitar + bass + piano
## Find rows with errors
index_err = []
for rows in df['Player'].values:
    if rows in instruments:
        print(df[df['Player'] == rows][['Band', 'Song', 'Player', 'index']])
        index_err.append(df[df['Player'] == rows])


# In[8]:


## Build a new dataset with all mistakes
db = index_err[0]
for el in index_err[1:]:
    db = pd.concat([db, el], ignore_index = True)

db.drop_duplicates(['Band', 'Song'], inplace= True)
db = db.reset_index().drop('level_0', axis = 1)
db.head()


# In[9]:


## Move 'Player' to 'Technique'
for x in range(len(db)):    
    db['Technique'][x].append(db['Player'][x])

db.drop('Player', axis = 1, inplace = True)
db['Player'] = ''
db


# In[10]:


df_clean = pd.merge(df, db, on = ['index', 'Band', 'Song', 'Difficulty', 'Score'], how = 'left')
player = []
tech = []
for x in range(len(df_clean)):
    if df_clean['Player_y'][x] == '':
        player.append(np.nan)
    else:
        player.append(df_clean['Player_x'][x])
    
        
df_clean['Player'] = player
df_clean.drop(['Player_x', 'Player_y'], axis = 1, inplace = True)
df_clean['Player'] = df_clean['Player'].replace('nan', np.nan)
df_clean.drop('Technique_y', axis = 1, inplace = True)
df_clean.rename(columns={'Technique_x': 'Technique'}, inplace = True)
df_clean['Technique'] = df_clean['Technique'].apply(lambda x: pd.Series(x).unique().tolist())
## Order columns
df_clean = df_clean.reindex(columns=['index','Band','Song','Player','Technique','Difficulty', 'Score'])


# In[11]:


## Clean Technique from excessive characters such as 'Track: '
def clean(x):
    
    x = x.replace('Track: ', '')
    
    return(x)
    
df_clean['Technique'] = df_clean['Technique'].apply(lambda x: list(map(clean, x)))


# In[12]:


print(len(df_clean), len(df))
type(df_clean['Technique'][0])
df_clean


# In[13]:


# ## Check not english caracter
not_english = []
def eng_character(x):
    eng = re.compile('[a-zA-Z0-9]')
       
    if eng.findall(x):
        print('English: {}'.format(x))
    else:
        print('Not english: {}'.format(x))
        not_english.append(x)
#         not_english_index.append(x.index)
        
    return()


df_clean['Song'].apply(lambda x: eng_character(x))
df_clean['Band'].apply(lambda x: eng_character(x))



## Plot


# In[14]:


## Drop cyrillic rows
print(len(df_clean))
for el in not_english:
    i = df_clean[df_clean['Song'] == el].index
    l = df_clean[df_clean['Band'] == el].index

    df_clean.drop(i, inplace = True)
    try:
        df_clean.drop(l, inplace = True)
    except:
        continue

print(len(df_clean))


# Drop empty Difficulty rows

# In[15]:


i2 = df_clean[df_clean['Difficulty'].isnull()].index
print(len(i2))
df_clean.drop(i2, inplace=True)
df_clean.drop('index', inplace=True, axis = 1)
df_clean.reset_index(inplace=True)
print(len(df_clean))
df_clean


# Check there are some wrong splits between Player and Technique.
# Controlla il contenuto di ogni lista, estrai il contenuto, dividilo in tipi di strumenti, guarda cosa rimane fuori e a quale riga corrisponde

# In[16]:


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


df_clean['Technique'].apply(lambda x: unique_el(x))


# In[17]:


len_ls = df_clean['Technique'].apply(lambda x: len(x))
len(len_ls[len_ls == 0]) + 6646

print('Tot techniques used: {} |'.format(len(technique)), 
      'N° empty list: {} |'.format(len(len_ls[len_ls == 0])),
      ## Supponiamo che le liste vuote abbiano il proprio unico elemento in 'Player'
      'Possible elements: {} |'.format(len(technique) + len(len_ls[len_ls == 0])),
      'Max n° technique for song: {} |'.format(len_ls.unique().max()),
      'Lenght Dataset: {}'.format(len(df_clean)))


# In[18]:


## Technique
style = pd.Series(technique).unique()
print('N° Technique: {}'.format(len(style)))
style
## There are many techniques with transcriptive mistakes. Others actually are players.


# In[19]:


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


# In[20]:


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

print('Guitar: {} |'.format(len(guitar)),
      'Piano: {} |'.format(len(piano)),
      'Drums: {} |'.format(len(drums)),
      'Bass: {} |'.format(len(bass)),
      'Others clean: {}'.format(len(others)), 
      'Togheter: {} |'.format(togheter_clean),
      'All: {} |'.format(len(style)), 
      'All - Togheter: {}'.format(len(style) - togheter_clean))


mismatch = set(style1) - set(guitar) - set(drums) - set(piano) - set(bass) - set(others)
print('N° mismatch instruments: {}'.format(len(mismatch)))
## Inside guitar and bass there still are some players


# In[21]:


## Divide another time guitar and bass elements into more classes
## Guitar
player_outside_brackets = re.compile('(uitar)[()]')
playerorstyle_inside_brackets = re.compile('[()](\w+)')
player_outside_brackets_ls = []
playerorstyle_inside_brackets_ls = []
for el in guitar:
    if player_outside_brackets.findall(el):
        player_outside_brackets_ls.append(el)
#         print('guitar inside brackets', el)
    if playerorstyle_inside_brackets.findall(el):
        playerorstyle_inside_brackets_ls.append(el)
#         print('player inside brackets', el)
    
# print(len(playerorstyle_inside_brackets_ls), len(player_outside_brackets_ls))
playerorstyle_inside_brackets_ls = set(playerorstyle_inside_brackets_ls) - set(player_outside_brackets_ls)
playerorstyle_inside_brackets_ls


# In[22]:


print('Mismatch/Dataset: ' + str(round(len(mismatch)/len(df_clean)*100, 2)) + '%')


# Find rows with mismatch in Technique. Look at 'Player' columns

# In[23]:


def find_mismatch(x):
    if x in mismatch:
        print(x)
    return()

df_clean['Technique'].apply(lambda x: list(map(find_mismatch, x)))


# In[24]:


print(df_clean['Player'].isnull().sum())
print(df_clean.head())

df_clean.drop('index', axis = 1, inplace = True)
df_clean.to_csv('Dataset_Song_Features_clean.csv')
## Bisogna fare scraping per aver info sui Player


# In[25]:


# dt = pd.read_csv('Dataset_Song_Features_clean.csv')

# def index_mismatch(x):
#     for el in mismatch:
#         if el in x:
#             return(x.index)
    

# dt.apply(lambda x: map(index_mismatch, x))

