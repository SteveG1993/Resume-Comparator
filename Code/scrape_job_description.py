# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 16:29:00 2019

@author: Steven.Gregoire
"""

import requests


url = 'https://www.amazon.jobs/en/jobs/746354/research-science-manager-nlu-analytics'
r = requests.get(url)
html = r.text

from bs4 import BeautifulSoup


# Create a BeautifulSoup object from the HTML
soup = BeautifulSoup(html, "html5lib")


text = soup.find_all('p')

print(text)
#text = [s.extract() for s in soup('p')]



import requests


url = 'https://www.amazon.jobs/en/jobs/746354/research-science-manager-nlu-analytics'
r = requests.get(url)
html = r.text

from bs4 import BeautifulSoup


# Create a BeautifulSoup object from the HTML
soup = BeautifulSoup(html, "html5lib")


text = soup.find_all('p')

words = 

