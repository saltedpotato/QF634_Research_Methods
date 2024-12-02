import pandas as pd
import time

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
        sources +=[entry['source']['href']]
        time.sleep(0.25)

    news = pd.DataFrame()
    news["date"] = dates
    news["title"] = titles
    news["source"] = sources
    print(news.shape)
    return news