
import pandas  as  pd
from  bs4  import BeautifulSoup
import urllib
import codecs
import os,glob
import json

#Web Scrapper to fetch the list of TED Talks in Hindi

def List_Talks(path,list):
    
    r = urllib.urlopen(path).read()
    soup = BeautifulSoup(r)
    talks= soup.find_all("a",class_='')
    #print(talks)
    for i in talks:
        if i.attrs['href'].find('/talks/')==0 :
            talkname = i.attrs['href'].split('?')[0]
            list.append(talkname)

    return list

#Fetch the English Transcript

def EnglishTranscript(url):

    url = url + "language=en"
    print url
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    #print data
    for key, value in data.items():
        print value

#Fetch the Hindi Transcript

def HindiTranscript(url):

    url = url + "language=hi"
    print url
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    #print data
    for key, value in data.items():
        print value

all_talk_names= []

for i in xrange(1,12):
    path='https://www.ted.com/talks?language=hi&page=%d'%(i)
    list_of_talks=List_Talks(path,all_talk_names)

list_of_talks = list(set(list_of_talks))

#all_talk_names contains the list of TED Talks in Hindi Language

#Go through the list one by one and get the transcripts

for x in list_of_talks:
    url="https://www.ted.com/"+x+"/transcript.json?"
    EnglishTranscript(url)
    HindiTranscript(url)



url = "https://www.ted.com//talks/marina_abramovic_an_art_made_of_trust_vulnerability_and_connection/transcript.json?language=en"
response = urllib.urlopen(url)
data = json.loads(response.read())
for key, value in data.items():
    print value








