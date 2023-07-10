import pandas as pd
from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter


ex=URLExtract()
def fetch(selecteduser,df):
    if selecteduser!='Overall':
        df=df[df['User']==selecteduser]

    total = df.shape[0]

    words=[]
    for i in df['Message']:
        words.extend(i.split())

    #media
    media_count = (df['Message'] == '<Media omitted>').sum()

    #link
    links = []
    for i in df['Message']:
        links.extend(ex.find_urls(i))

    return total, len(words),media_count,len(links)


def busyusers(df):
    X = df['User'].value_counts().head()
    newdf=round((df['User'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','count':'percent'})
    return X,newdf

def wordcl(selecteduser,df):
    if selecteduser!='Overall':
        df=df[df['User']==selecteduser]

    wc = WordCloud(width=500,height=500,background_color='black')
    temp = df[df['Message'] != '<Media omitted>']
    dfwc=wc.generate(temp['Message'].str.cat(sep=" "))
    return dfwc

import emoji

def extract_emojis(selecteduser, df):
    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    emojis = []
    for message in df['Message']:
        for c in message:
            if emoji.is_emoji(c):
                emojis.append(c)

    emojidf=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emojidf

def timeline(selecteduser, df):
    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    timelin= df.groupby(['year','month']).count()['Message'].reset_index()
    time=[]
    for i in range(timelin.shape[0]):
        time.append(timelin['month'][i] + "-" + str(timelin['year'][i]))

    timelin['time']=time
    return timelin

def dailytimeline(selecteduser, df):
    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    daily = df.groupby('dayname').count()['Message']
    daily = daily.reindex(day_order)
    return daily

def busyhours(selecteduser, df):
    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    pivotdf=df.pivot_table(index='dayname', columns='hour', values='Message',aggfunc='count').fillna(0)

    return pivotdf
def mostbusymonth(selecteduser, df):
    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]
    busymonth = df.groupby('month').count()['Message']


    return busymonth









