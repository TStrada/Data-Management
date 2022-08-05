#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import re
import os
import requests
from bs4 import BeautifulSoup


# In[2]:


## List songs available
URL = "https://www.songsterr.com/a/wa/all?r=sort&lyrics=any&tuning=any&diff=any&inst=gtr&sort=p&vocals=any"

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find("div", class_="listOuterWrapper")

songs = results.find_all("a", class_="tab-link")

song_links = []
for song in songs:    
    song_links.append(song['href'])
song_links
len(song_links)


# In[3]:


## Build the official link 'https://www.songsterr.com/' + song_path
for path in song_links:

    # find the index of path
    i = song_links.index(path)
  
    # replace path with 'https://www.songsterr.com/' + path
    song_links = song_links[:i]+['https://www.songsterr.com' + str(path)]+song_links[i+1:]

song_links


# In[4]:


## Search every link and extract informations
band = []
song = []
player = []
technique = []
difficulty = []
difficulty_score = []

n_errors = []



for link in song_links:
        
        print('-------------------------------------------------------------')
        print('Link: {}'.format(link))
        
    
    ##  Open link page
        URL = str(link)
        page = requests.get(URL)

    ##  Parse it with BeautifulSoup
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="header")

    ##  Find and add informations about the band and title song
        try:    
            Band_Song = results.find("h1", class_="C612su")
            print(Band_Song.text)
        except:
            print('\u0332'.join('Band and Song not found'))
            n_errors += 1
            continue

        try: 
            band_song = (Band_Song.text).split('\xa0-\xa0')
            print(band_song)
        except:
            print('\u0332'.join('Band and Song split error'))
            n_errors += 1
            break
            
        try:
            band.append(band_song[0])
        except:
            band.append(np.nan)
            n_errors += 1
            print('\u0332'.join('Band not found'))
        try:
            song.append(band_song[1].replace(' Tab', ''))
        except:
            song.append(np.nan)
            n_errors += 1
            print('\u0332'.join('Song not found'))
            

        ##  Find and add informations about the player and the technique
        try:
            Player_style = results.find("h2", class_="C61a4")
            print(Player_style.text)
        except:
            n_errors += 1
            print('\u0332'.join('Player and Style not found'))
            continue

        try:
            player_list = (Player_style.text).replace('Difficulty (Rhythm):', '').replace('\xa0-\xa0', ' - ').split(' - ')
            print(player_list)

        except:
            n_errors += 1
            print('\u0332'.join('Player and Style split error'))
            break
        
        try:
            if 'pachelbel' in link:
                player.append(np.nan)
                technique.append(player_list)
            else:
                player.append(player_list[0].replace('Track: ', ''))
        except:
            player.append(np.nan)
            n_errors += 1
            print('\u0332'.join('Player not found'))
        
        if 'pachelbel' not in link:
            try:
                style = player_list[1:]
                technique.append(style)
            except:
                technique.append(np.nan)
                n_errors += 1
                print('\u0332'.join('Technique not found'))
            
            
        ##  Find and add informations about the track difficulty
        try:
            track_difficulty = soup.find(id="track-difficulty")
            print(track_difficulty)
            try:
                diff = re.findall('(\w+)', str(track_difficulty))
                index_pre_diff = diff.index('title')
                print(diff)
                print(index_pre_diff)

                if diff[index_pre_diff + 1] == 'Beginner':
                    difficulty_score.append(diff[index_pre_diff + 3] + '/' + '8')
                    print('Success')

                if diff[index_pre_diff + 1] == 'Intermediate':
                    difficulty_score.append(str(int(diff[index_pre_diff + 3]) + 2) + '/' + '8')
                    print('Success')

                if diff[index_pre_diff + 1] == 'Advanced':
                    difficulty_score.append(str(int(diff[index_pre_diff + 3]) + 5) + '/' + '8')
                    print('Success')


                difficulty.append(diff[index_pre_diff + 1])
            except:
                n_errors += 1
                difficulty.append(np.nan)
                print('Re operation findall error')
                continue

        except:
            print('\u0332'.join('Diffulty not found'))
            difficulty.append(np.nan)
            difficulty_score.append(np.nan)
#             n_errors += 1
            continue

        
            
print(n_errors)


# In[5]:


dataset = {'Band': band, 'Song': song, 
           'Player': player, 'Technique': technique,
           'Difficulty': difficulty,
           'Score': difficulty_score}
for key in dataset:
    print(len(dataset[key]))


a = pd.DataFrame(dataset)
a.to_csv('Dataset_Song_1.csv')

