#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import numpy as np
import re
import os
import requests
from bs4 import BeautifulSoup
# import wikipedia as wkp ## Non funziona


# In[26]:


dt = pd.read_csv('Dataset_Analysis/Dataset_Song_Features_clean.csv') 
df = dt[dt['Player'].isnull()]


# In[28]:


song_band = []
def song_plus_band(col1, col2):
    
    ## Example: So_Far_Away_(Dire_Straits)
    band = col1.replace(' ', '_').replace('-', '_')
#     print(band)
    song = col2.replace(' ', '_')
#     print(song)
    band_plus_song = song + '_' + '({})'.format(band)
    print(band_plus_song)
    song_band.append(band_plus_song)
    return()

df.apply(lambda x: song_plus_band(x['Band'], x['Song']), axis = 1)


# In[88]:


# url_ita = 'https://it.wikipedia.org/wiki/{}'.format(song_band[14])
# url_en = 'https://it.wikipedia.org/wiki/{}'.format(song_band[14])
# url_ita = 'https://it.wikipedia.org/wiki/{}'.format('Dear_God_(Avenged_Sevenfold)')
chitarra_solista = []
chitarra = []
basso = []
piano = []
batteria = []
altro = []

def wkp_ita(x):
    
    url_ita = 'https://it.wikipedia.org/wiki/{}'.format(x)
    
    try:
        page = requests.get(url_ita)

        soup = BeautifulSoup(page.content, "html.parser")
        # print(soup)
        results = soup.find("ul")
        a = re.split(r'\n', results.text)

        chitarra_solista_re = re.compile('chitarra solista')
        chitarra_re = re.compile('chitarra')
        basso_re = re.compile('basso')
        piano_re = re.compile('piano')
        batteria_re = re.compile('batteria')

        for el in a:
            if chitarra_solista_re.search(el):
                chitarra_solista.append(el)
            if chitarra_re.search(el):
                chitarra.append(el)
            if basso_re.search(el):
                basso.append(el)
            if piano_re.search(el):
                piano.append(el)
            if batteria_re.search(el):
                batteria.append(el)
            else:
                altro.append(el)
    except:       
        print('Not found {}'.format(x))

    return()


# In[ ]:


for x in song_band:
    wkp_ita(x)


# In[71]:


a[0]

