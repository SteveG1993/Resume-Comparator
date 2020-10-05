#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 20:43:38 2020

@author: steve
"""

from bs4 import BeautifulSoup
import requests

from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
import codecs
from nltk.stem.wordnet import WordNetLemmatizer

lem = WordNetLemmatizer()
# NLTK's default english stopwords

minimum_word_length = 2
desired_parts_of_speech = set(['NN'] )

def get_document_folder():
    return '../data/'


def get_stopwords():
    default_stopwords = stopwords.words('english')
    custom_stopwords_file = get_document_folder() + 'custom_stopwords.txt'
    custom_stopwords = codecs.open(custom_stopwords_file, 'r', 'utf-8').read().splitlines()
    all_stopwords = list(map(str.lower,set(default_stopwords + custom_stopwords)))
    #all_stopwords = [lem.lemmatize(w) for w in all_stopwords]
    return all_stopwords


def Pull_Job_Description(url):
    r = requests.get(url)
    html = r.text
    # Create a BeautifulSoup object from the HTML
    soup = BeautifulSoup(html, "html5lib")  
    textlist = []
    for node in soup.findAll('p'):
        for text in node.findAll(text=True):
            textlist.append(text)  
    raw_text = ''.join(textlist)  
    return raw_text

def process_text(text):
    tokens = word_tokenize(text)
    # tags = pos_tag(tokens)
    stopwords = get_stopwords()

    # if pos is not None:
    #     words = [w for w,pos in tags if pos in pos]
        
    words = [t for t in tokens if t.isalpha()]
    words = [w for w in words if len(w)>=minimum_word_length]
    words = [w for w in words if not w.isnumeric()]
    words = [w.lower() for w in words]
    words = [w for w in words if w not in stopwords]
    words = [lem.lemmatize(w) for w in words]

    return words

def open_resume(filename):
    f_resume=open(get_document_folder() + filename,'r',)
    raw_resume =f_resume.read()
    return raw_resume
 
    
def compare(job_wordlist,resume_wordlist,verbose=True):
    resume_set = set(resume_wordlist)
    job_set = set(job_wordlist)
    matching_words = resume_set.intersection(job_set)
    missing_words = job_set-resume_set
    
    print ('You resume matches at ',"{0:.0%}".format(len(matching_words)/len(job_set)))
    
    if verbose:    
        print('Your resume is missing the following words (naive): ',missing_words)

if __name__ == '__main__':
    url = input('Enter URL to job description:')
    resume_filename = input('Enter file name of your resume:')
    #print('You entered:')
    #print(url)
    job_desc = Pull_Job_Description(url=url)
    resume_text = open_resume(resume_filename)
    
    if job_desc is not None and resume_text is not None:
        desc_words = process_text(job_desc, stopwords)
        resume_words = process_text(resume_text,stopwords)
        compare(desc_words,resume_words)
    else:
        print('Missing resume or job description')
    
    
    
    
    