
import pandas  as  pd
from  bs4  import BeautifulSoup
import urllib
import codecs
import os,glob
import json

def enlist_talk_names(path,list):
    r = urllib.urlopen(path).read()
    soup = BeautifulSoup(r)
    talks= soup.find_all("a",class_='')
    #print(talks)
    for i in talks:
        if i.attrs['href'].find('/talks/')==0 :

            talkname = i.attrs['href'].split('?')[0]
            list.append(talkname)

    return list

all_talk_names= []

for i in xrange(1,2):
    path='https://www.ted.com/talks?language=hi&page=%d'%(i)
    all_talk_names=enlist_talk_names(path,all_talk_names)


#print all_talk_names


url = "https://www.ted.com/talks/will_marshall_the_mission_to_create_a_searchable_database_of_earth_s_surface/transcript.json?language=en"
response = urllib.urlopen(url)
data = json.loads(response.read())
#print data

for key, value in data.items():
    print value








