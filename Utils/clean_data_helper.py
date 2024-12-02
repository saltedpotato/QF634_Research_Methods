import pandas as pd
import time
import sys, os
from newscatcher import Newscatcher, urls

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def clean_scraped_data(s):
    s2 = s.reset_index(drop=True)
    s2.columns = s2.columns.droplevel(1)
    s2["date"] = s.index.tolist()
    s2 = s2[["date"] + s2.columns.tolist()[:-1]]
    return s2

def clean_goog_news(entries):
    dates = []
    titles = []
    sources = []

    for entry in entries:
        dates += [entry["published"]]
        titles += [entry["title"]]
        sources +=[entry['link']]
        time.sleep(0.25)

    news = pd.DataFrame()
    news["date"] = dates
    news["title"] = titles
    news["source"] = sources
    print(news.shape)
    return news

# topics supported: 'tech', 'news', 'business', 'science', 'finance', 'food', 'politics', 'economics', 'travel', 'entertainment', 'music', 'sport', 'world'
def clean_newscatcher_news(t):
    supported_urls = urls(topic = t, language = 'en') 
    print(f"No. of URLs: {len(supported_urls)}")
    print(supported_urls)

    dates = []
    titles = []
    sources = []
    unsupported_urls = []
    for url in supported_urls:
        blockPrint()
        nc = Newscatcher(website = url, topic = t)
        results = nc.get_news()
        enablePrint()
        try:
            articles = results['articles']
        
            for article in articles:
                dates += [article["published"]]
                titles += [article["title"]]
                sources +=[article['link']]
        except:
            unsupported_urls += [url]
            continue
    
    news = pd.DataFrame()
    news["date"] = dates
    news["title"] = titles
    news["source"] = sources
    news["topic"] = t
    print(news.shape)
    print(f"Unsupported URL count: {len(unsupported_urls)}")
    return news



