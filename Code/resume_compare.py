#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 09:50:24 2019

@author: steve
"""
import nltk
#nltk.download('averaged_perceptron_tagger')


from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
import codecs
from nltk.stem.wordnet import WordNetLemmatizer
lem = WordNetLemmatizer()

# NLTK's default english stopwords
default_stopwords = stopwords.words('english')

#File Locations

document_folder = '../data/'
resume_file = document_folder + 'resume.txt'
job_description_file = document_folder + 'job_description.txt'
custom_stopwords_file = document_folder + 'custom_stopwords.txt'

custom_stopwords = codecs.open(custom_stopwords_file, 'r', 'utf-8').read().splitlines()
all_stopwords = list(map(str.lower,set(default_stopwords + custom_stopwords)))
all_stopwords = [lem.lemmatize(w) for w in all_stopwords]

                        
minimum_word_length = 2

desired_parts_of_speach = set(['NN'
                   ,'NNP'
                   ,'NNS'
                   ,'NNPS']
                 )



def process_text(text,stopwords,pos=None,lemmatizer=None):
    tokens = word_tokenize(text)
    tags = pos_tag(tokens)
    lem = lemmatizer

    if pos is not None:
        words = [w for w,pos in tags if pos in pos]
        
    words = [t for t in tokens if t.isalpha()]
    words = [w for w in words if len(w)>=minimum_word_length]
    words = [w for w in words if not w.isnumeric()]
    words = [w.lower() for w in words]
    words = [w for w in words if w not in all_stopwords]

    
    if lemmatizer is not None:
        words = [lem.lemmatize(w) for w in words]
#     words = [nouns_only(w) for w in words]
#     words = map(nouns_only, words)

    return words

def pos_inspection(text,pos=None):
    tokens = word_tokenize(text)
    tags = pos_tag(tokens)
    return tags
    



f_resume=open(resume_file,'r',)
f_desc = open(job_description_file,'r')

raw_resume =f_resume.read()
raw_desc = f_desc.read()


pos_tags = pos_inspection(raw_desc)


resume_words = process_text(raw_resume,all_stopwords,desired_parts_of_speach,lem)
job_words = process_text(raw_desc,all_stopwords,desired_parts_of_speach,lem)

resume_set = set(resume_words)
job_set = set(job_words)



matching_words = resume_set.intersection(job_set)
missing_words = job_set-resume_set


print ('You resume matches at ',"{0:.0%}".format(len(matching_words)/len(job_words)))


print('Your resume is missing the following words (naive): ',missing_words)



import requests


url = 'https://www.amazon.jobs/en/jobs/746354/research-science-manager-nlu-analytics'
r = requests.get(url)
html = r.text

from bs4 import BeautifulSoup


# Create a BeautifulSoup object from the HTML
soup = BeautifulSoup(html, "html5lib")

textlist = []

for node in soup.findAll('p'):
    for text in node.findAll(text=True):
        textlist.append(text)

raw_text = ''.join(textlist)

print(raw_text)


