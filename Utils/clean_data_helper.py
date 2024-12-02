import pandas as pd

def clean_scraped_data(s):
    s2 = s.reset_index(drop=True)
    s2.columns = s2.columns.droplevel(1)
    s2["Date"] = s.index.tolist()
    s2 = s2[["Date"] + s2.columns.tolist()[:-1]]
    return s2