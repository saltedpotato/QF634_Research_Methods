import pandas as pd
import time
import sys, os
from newscatcher import Newscatcher, urls
import gensim.downloader
import numpy as np
import re
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import random

model_glove_twitter = gensim.downloader.load('glove-twitter-25')

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
    return news

# topics supported: 'tech', 'news', 'business', 'science', 'finance', 'food', 'politics', 'economics', 'travel', 'entertainment', 'music', 'sport', 'world'
import random
def clean_newscatcher_news(t, n = "All"):
    supported_urls = urls(topic = t, language = 'en') 
    if n != "All":
        if n <= len(supported_urls):
            supported_urls = random.sample(supported_urls, n)  # Select 3 random items            

    
    print(f"No. of URLs: {len(supported_urls)}")
    print(supported_urls)

    dates = []
    titles = []
    sources = []
    unsupported_urls = []
    for url in supported_urls:
        nc = Newscatcher(website = url, topic = t)
        results = nc.get_news()
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

def get_topic(phrase):
    topics = ['tech', 'news', 'business', 'science', 'finance', 'politics', 'economics', 'travel', 'entertainment', 'music', 'world']
    ret_topics = Counter() 

    for i in range(5):
        p = re.sub(r'[^a-zA-Z]+', '', phrase.sample(1).item().split(" ")[0].lower())
        similarity = 0
        topic = ''
        try:
            vec2 = model_glove_twitter[p]
            for t in topics:
                vec1 = model_glove_twitter[t]
                curr_similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
                if curr_similarity > similarity:
                    topic = t
                    similarity = curr_similarity
        except:
            continue

        ret_topics.update([topic])
    if len(ret_topics) == 0:
        return ''
    else:
        largest_value = max(ret_topics, key=ret_topics.get)
        return largest_value

def remove_similar_news(df, col, threshold=0.8):
    df = df.reset_index(drop=True)
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(df[col])

    cos_sim = cosine_similarity(vectors)

    to_remove = []

    for r in range(len(cos_sim)):
        if r in to_remove:
            continue

        for c in range(len(cos_sim)-r):
            if r == c:
                continue
            similarity = cos_sim[r,c]
            if similarity > threshold:
                to_remove += [c]
                
    df = df.drop(df.index[to_remove])
    df = df.reset_index(drop=True)
    return df

def remove_irrelevant_news(df, col, threshold=0.1, threshold_size = 0.1):
    df = df.reset_index(drop=True)
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(df[col])

    cos_sim = cosine_similarity(vectors)

    to_remove = []

    for r in range(len(cos_sim)):
        # considered irrelevant if the article is too different from the rest
        perc_unsimilar = len(cos_sim[r][cos_sim[r] <= threshold])/len(cos_sim[r])
        
        if perc_unsimilar >= threshold_size:
            to_remove += [r]
        
                
    df = df.drop(df.index[to_remove])
    df = df.reset_index(drop=True)
    return df            
