#!/usr/bin/env python
# coding: utf-8

## Import libraries
from selenium import webdriver
import pandas as pd
import numpy as np
import re
import os
from selenium.common.exceptions import (NoSuchElementException,ElementClickInterceptedException,ElementNotInteractableException)


import requests
from bs4 import BeautifulSoup

URL = "https://www.songsterr.com"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="header")
# print(results.prettify())

Band_Song = results.find_all("div", class_="C612su")
# for job_element in job_elements:
#     print(job_element.text, end="\n"*2)
    
player_style = results.find_all("div", class_="C61a4")
# # for job_element in job_elements:
# #     print(job_element.text, end="\n"*2)

track_difficulty = soup.find(id="track-difficulty")
track_difficulty
# difficulty = track_difficulty.find_all('div', class_ = 'C61331')
# # for job_element in difficulty:
# #     print(job_element.text, end="\n"*2)
# difficulty

