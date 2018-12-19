
import pandas  as  pd
import numpy as np
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

if os.path.exists("hindi.csv"): os.remove("hindi.csv")
if os.path.exists("english.csv"): os.remove("english.csv")
if os.path.exists("output.csv"): os.remove("output.csv")

#Web Scrapper to fetch the list of TED Talks in Hindi

def List_Talks(path,list):

    time.sleep(30)
    
    req = requests.get(path)
    
    print req.status_code
   
    if req.status_code == 200:
        r = urllib.urlopen(path).read()
        soup = BeautifulSoup(r)
        talks= soup.find_all("a",class_='')
        for i in talks:
            if i.attrs['href'].find('/talks/')==0 :
                talkname = i.attrs['href'].split('?')[0]
                list.append(talkname)
    else:
        time.sleep(60)
        r = urllib.urlopen(path).read()
        soup = BeautifulSoup(r)
        talks= soup.find_all("a",class_='')
        for i in talks:
            if i.attrs['href'].find('/talks/')==0 :
                talkname = i.attrs['href'].split('?')[0]
                list.append(talkname)

    return list

#Method to read the Online JSON from TED Talks Transcript URLs

def readjson(data,lang):
    
    df = pd.DataFrame()
    hi_text_data=[]
    hi_time_frame=[]
    en_text_data=[]
    en_time_frame=[]

    if "paragraphs" not in data: # check if paragraphs node exits
        return
    for cues in data['paragraphs']: #iterate through paragraphs node
        for d in cues['cues']: #iterate through cues
            #print d['text']
            #To get rid of the next line error
            oldsent =  d['text'].encode('utf-8') 
            timex =  str(d['time']).encode('utf-8') 
            sentence = oldsent.replace("\n", " ") 
            print(str(sentence).encode('utf-8'))
           
            if(lang == "hi"):      
              
                hi_text_data.append(sentence)
                hi_time_frame.append(timex)

                df1=pd.DataFrame()
                df1[0] = hi_time_frame
                df1[1] = hi_text_data
   
                df1.to_csv('hindi.csv',mode='w',index=False, header=False,sep='\t',encoding='utf-8')
                
            else:
                en_text_data.append(sentence)
                en_time_frame.append(timex)
            
                df2=pd.DataFrame()
                df2[0] = en_time_frame
                df2[1] = en_text_data
    
                #df = pd.concat([df,df1],axis=1)
                df2.to_csv('english.csv',mode='w', index=False, header=False,sep='\t',encoding='utf-8')
               
   
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
    else:
        print("Scraping too much.. Cooldown")
        time.sleep(60) 
        data = requests.get(url)
        data = data.json()
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
    else:
        print("Scraping too much.. Cooldown")
        time.sleep(60) 
        data = requests.get(url)
        data = data.json()
        print("Writing Hindi Transcript")
        readjson(data,"hi")

all_talk_names= []
list_of_talks=[]

for i in xrange(1,14):
    path='https://www.ted.com/talks?language=hi&page=%d'%(i)
    list_of_talks=List_Talks(path,all_talk_names)


list_of_talks = list(set(list_of_talks))
print("Total no of talks",len(list_of_talks))
time.sleep(10)

#list_of_talks contains the list of TED Talks in Hindi Language

#Go through the list one by one and get the transcripts

for x in list_of_talks:
    url="https://www.ted.com"+x+"/transcript.json?"
    count = count + 1
    print("Talk no: "+str(count)+" Talk name: "+"https://www.ted.com"+x)
    EnglishTranscript(url)
    HindiTranscript(url)

    a = pd.read_csv("hindi.csv",sep='\t', header=None)
    a.columns = ["time", "text"]
    b = pd.read_csv("english.csv",sep='\t', header=None)
    b.columns = ["time", "text"]

    output = pd.merge(a,b, on='time')
    output.to_csv('output.csv', mode='a',index=False, header=False,sep='\t',encoding='utf-8')

    
    print("Finished talkno "+str(count))
    print("Sleeping for 2 seconds before htting next Talk URL")

    #Sleep 15/60/120/300 seconds to avoid Status Code 429 (Too Many Requests)
    time.sleep(2) 

    import gc
    gc.collect()
