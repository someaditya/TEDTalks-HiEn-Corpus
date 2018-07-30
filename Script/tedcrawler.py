
import pandas  as  pd
from  bs4  import BeautifulSoup
import urllib
import codecs
import os,glob

def enlist_talk_names(path,dict_):
    r = urllib.urlopen(path).read()
    soup = BeautifulSoup(r)
    talks= soup.find_all("a",class_='')
    for i in talks:
        print i 
        if i.attrs['href'].find('/talks/')==0 and dict_.get(i.attrs['href'])!=1:
            dict_[i.attrs['href']]=1    
    return dict_

all_talk_names={}
for i in xrange(1,61):
    path='https://www.ted.com/talks?language=hi&page=%d'%(i)
    all_talk_names=enlist_talk_names(path,all_talk_names)
    #print all_talk_names

def extract_talk(path,talk_name):
    r=urllib.urlopen(path).read()
    soup=BeautifulSoup(r)
    df=pd.DataFrame()
    #print path
    for i in soup.findAll('link'):
        if i.get('href')!=None and i.attrs['href'].find('?language=')!=-1:
            #print i.attrs['href']
            lang=i.attrs['hreflang']
            path=i.attrs['href']
            r1=urllib.urlopen(path).read()
            soup1=BeautifulSoup(r1)
            time_frame=[]
            text_talk=[]
            for i in soup1.findAll('span',class_='talk-transcript__fragment'):
                time_frame.append(i.attrs['data-time'])
                text_talk.append(i.text.replace('\n',' '))
            #print len(time_frame),len(text_talk)
            df1=pd.DataFrame()
            df1[lang]=text_talk
            df1[lang+'_time_frame']=time_frame
            df=pd.concat([df,df1],axis=1)
    df.to_csv(talk_name+'.csv',sep='\t',encoding='utf-8')

for i in all_talk_names:
    #print('https://www.ted.com'+i+'/transcript',i[7:])
    #print i
    extract_talk('https://www.ted.com'+i+'/transcript',i[7:])

path='/Users/someaditya/Desktop/TedCrawler/'
os.chdir(path)
pieces=[]
for file in glob.glob('*.csv'):
    print file
    frame=pd.read_csv(path+file,sep='\t',encoding='utf-8')
    pieces.append(frame)
df= pd.concat(pieces, ignore_index=True)

df.to_csv('All_TED_TALKS_DATA_1.csv',sep='\t',encoding='utf-8')

