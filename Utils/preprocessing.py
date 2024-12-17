from Utils.import_packages import *

from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import string

# Download NLTK data
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
# nltk.download('punkt_tab')
# nltk.download('averaged_perceptron_tagger_eng')

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')

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

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
    
# Preprocessing function
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    # Tokenize text
    tokens = word_tokenize(text.lower(), language='english')
    
    # Get POS tags
    pos_tags = pos_tag(tokens)

    # Remove punctuation and stopwords, and lemmatize
    tokens = [lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for word, tag in pos_tags 
              if word not in stop_words and word not in string.punctuation]
    return ' '.join(tokens)

def text_to_vector(df, vectorise_columns, numerical_columns = []):
    vectorizer = CountVectorizer()
    ret_df = pd.DataFrame()
    all_col = vectorise_columns + numerical_columns
    for col in all_col:
        if col in vectorise_columns:
            vectorized = vectorizer.fit_transform(df[col])
            ret_df = pd.concat([ret_df, pd.DataFrame(vectorized.toarray())], axis=1)
        else:
            ret_df[col] = df[col]
    return ret_df
