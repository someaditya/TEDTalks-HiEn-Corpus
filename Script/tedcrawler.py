
import pandas  as  pd
from  bs4  import BeautifulSoup
import urllib
import codecs
import os,glob
import json
import requests
import time

import sys

reload(sys)
sys.setdefaultencoding('utf8')

oldsent = ' '
sentence = ' '

count = 0

if os.path.exists("hindi.txt"): os.remove("hindi.txt")
if os.path.exists("english.txt"): os.remove("english.txt")
    
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

#Method to read the Online JSON from TED Talks Transcript URLs

def readjson(data,lang):
    if "paragraphs" not in data: # check if paragraphs node exits
        return
    for cues in data['paragraphs']: #iterate through paragraphs node
        for d in cues['cues']: #iterate through cues
            #print d['text']
            #To get rid of the next line error
            oldsent =  d['text']
            sentence = oldsent.replace("\n", " ") 
            print(str(sentence).encode('utf-8'))
            if(lang == "hi"):      
                file = open("hindi.txt","a")
                file.write(str(sentence).encode('utf-8')+"\n") 
            else:
                file = open("english.txt","a")
                file.write(str(sentence).encode('utf-8')+"\n")


#Fetch the English Transcript

def EnglishTranscript(url):

    url = url + "language=en"
    print url
    data = requests.get(url)
    print data.status_code
    if data.status_code == 200:
        print("Good Response")
        data = data.json()
        #print data
        print("Writing English Transcript")
        readjson(data,"eng")

#Fetch the Hindi Transcript

def HindiTranscript(url):

    url = url + "language=hi"
    print url
    response = requests.get(url)
    data = requests.get(url)
    print data.status_code
    if data.status_code == 200:
        print("Good Response")
        data = data.json()
        #print data
        print("Writing Hindi Transcript")
        readjson(data,"hi")

all_talk_names= []

for i in xrange(1,13):
    path='https://www.ted.com/talks?language=hi&page=%d'%(i)
    list_of_talks=List_Talks(path,all_talk_names)

list_of_talks = list(set(list_of_talks))

#list_of_talks contains the list of TED Talks in Hindi Language

#Go through the list one by one and get the transcripts

for x in list_of_talks:
    url="https://www.ted.com"+x+"/transcript.json?"
    count = count + 1
    print("Talk no: "+str(count)+" Talk name: "+"https://www.ted.com"+x)
    EnglishTranscript(url)
    HindiTranscript(url)
    
    print("Finished talkno "+str(count))
    print("Sleeping for 60 seconds before htting next URL")

    #Sleep 15/60/120/300 seconds to avoid Status Code 429 (Too Many Requests)
    time.sleep(60) 














