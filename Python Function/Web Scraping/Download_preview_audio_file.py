#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
import re
import requests


# ## Define a function:
# - Input = artist name, song name, url preview
# - Output = Database(columns = 'Artist name', 'Song name', 'song.mp3'

# In[3]:


def dowloader(song, url):
    
    mp3_song = song + '.mp3'
    sample = requests.get(url)
    
    open(mp3_song, 'wb').write(sample.content)
    
    return(mp3_song)
    
url_1 = 'https://p.scdn.co/mp3-preview/0f3af5cc81ffa0d41685dd697b6a193cedd7057a?cid=a91ed9edffbc4349b0ae66ad2680900a'
song = 'Example'
dowloader(song, url_1)

