from Utils.import_packages import *

# Apply preprocessing to datasets
def clean_text(text):
    if isinstance(text, str):
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and punctuation
        text = re.sub(r"[^\w\s]", "", text)
        # Remove extra spaces
        text = re.sub(r"\s+", " ", text).strip()
    else:
        text = ""
    return text

def preprocess_dataset(df):
    df['title'] = df['title'].apply(clean_text)
    df['sentiment_label'] = df['sentiment_label'].astype(int)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # Shuffle dataset
    return df