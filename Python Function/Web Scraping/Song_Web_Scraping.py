#!/usr/bin/env python
# coding: utf-8

## Import libraries
from selenium import webdriver
import pandas as pd
import numpy as np
import re
import os
from selenium.common.exceptions import (NoSuchElementException,ElementClickInterceptedException,ElementNotInteractableException)


## Set Chrome driver and open it at 'songsterr.com'
Path = 'C:\Program Files (x86)\chromedriver.exe'

driver = webdriver.Chrome(Path)
driver.get('https://www.songsterr.com')

## Avoid coockies istance
try:    
    driver.find_element_by_xpath('//*[@id="accept"]').click()
except :#(ElementClickInterceptedException,ElementNotInteractableException):
    print("element not interactable or Click intercepted")

