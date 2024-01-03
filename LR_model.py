# logistic_regression_model.py
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import string
import numpy as np
from camel_tools.tokenizers.morphological import MorphologicalTokenizer
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tagger.default import DefaultTagger
from camel_tools.utils.normalize import normalize_unicode
from camel_tools.utils.dediac import dediac_ar
from nltk.stem.isri import ISRIStemmer
import nltk
import demoji
from sklearn.svm import SVC
import arabic_reshaper
from bidi.algorithm import get_display

# import subprocess

# # To install all datasets
# # subprocess.run(['camel_data', '-i', 'all'], check=True)

# # or just the datasets for morphology and MLE disambiguation only
# subprocess.run(['camel_data', '-i', 'light'], check=True)

# # or just the default datasets for each component
# subprocess.run(['camel_data', '-i', 'defaults'], check=True)
# Load your dataset
# nltk.download('punkt')

mle = MLEDisambiguator.pretrained()


def preprocess(tweet):
    sentence = processDocument(tweet)
    normal_sen = sentence.split()
    d1tok_tokenizer = MorphologicalTokenizer(disambiguator=mle, scheme='d1tok', split='True')
    Tok_sen = d1tok_tokenizer.tokenize(normal_sen)
    tagger = DefaultTagger(mle, 'pos')
    tags = tagger.tag(Tok_sen)
    sentence = ''

    for i in range(len(Tok_sen)):
        if tags[i] == "noun" or tags[i] == "adj" or tags[i] == "verb":
            sentence += " " + Tok_sen[i]

    Tok_sen = d1tok_tokenizer.tokenize(sentence.split())
    disambiguated = mle.disambiguate(Tok_sen)
    stem_word = ' '.join([d.analyses[0].analysis['lex'] for d in disambiguated])
    sentence = normalize_unicode(stem_word)
    sentence = dediac_ar(sentence)

    return sentence


#-------------
arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
english_punctuations = string.punctuation
punctuations_list = arabic_punctuations + english_punctuations
# nltk.download('stopwords')

def remove_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)

    return text.translate(translator)


#-------------
def normalize_arabic(text):
    text = re.sub("[إأآٱا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    return text
#-------------
def remove_repeating_char(text):
    return re.sub(r'(.)\1{2,}', r'\1', text)
#-------------
def processDocument(doc):

    #Replace @username with empty string
    doc = re.sub(r'@[^\s]+', ' ', doc)
    doc = re.sub(r'_', ' ', doc)
    doc = re.sub(r'\n', ' ', doc)
    doc = re.sub(r'[a-z,A-Z]', '', doc)
    doc = re.sub(r'\d', '', doc)
    #Convert www.* or https?://* to " "
    doc = re.sub('((www\.[^\s]+)|(https?://[^\s]+))',' ',doc)
    #Replace #word with word
    doc = re.sub(r'#([^\s]+)', r'\1', doc)
    # remove punctuations
    doc= remove_punctuations(doc)
    # # normalize the tweet
    #doc= normalize_arabic(doc)
    # remove repeated letters
    doc=remove_repeating_char(doc)
    doc = re.sub(r'\W', ' ', doc)
    # Remove emojis
    doc = demoji.replace(doc, repl="")

    # Remove remaining non-alphanumeric characters

    # Remove extra whitespaces
    doc = re.sub(r'\s+', ' ', doc).strip()



    return doc



def train_model(X_train, y_train):
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 3))
    X_train_tfidf = vectorizer.fit_transform(X_train)

    param_grid = {'C': [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]}
    grid_search = GridSearchCV(LogisticRegression(), param_grid, cv=5)
    grid_search.fit(X_train_tfidf, y_train)

    best_params = grid_search.best_params_
    print("Best Parameters:", best_params)

    best_model = grid_search.best_estimator_
    best_model.fit(X_train_tfidf, y_train)

    return best_model, vectorizer

def test_model(model, vectorizer, X_test, y_test):
    X_test_tfidf = vectorizer.transform(X_test)
    y_pred = model.predict(X_test_tfidf)

    accuracy = accuracy_score(y_test, y_pred)
    print(f'accuracy : {accuracy*100:.2f}')
    
    return y_pred

def analyze_user_tweets(userFile, vectorizer, model):
    # Preprocess the unlabeled tweets
    unlabeled_df = pd.read_csv(userFile)
    unlabeled_df["Tweets"] = unlabeled_df['Tweets'].apply(lambda x: preprocess(x))

    unlabeled_df = unlabeled_df.dropna(subset=['Tweets'])
    unlabeled_df = unlabeled_df[unlabeled_df['Tweets'].str.strip() != ""]
    print(unlabeled_df)
    # Vectorize the unlabeled tweets using the same vectorizer
    X_unlabeled_tfidf = vectorizer.transform(unlabeled_df['Tweets'])

    # Predict labels for the unlabeled tweets
    y_unlabeled_pred = model.predict(X_unlabeled_tfidf)

    # Add 'Prediction' column to the DataFrame
    unlabeled_df['Prediction'] = y_unlabeled_pred

    # Calculate Depression Percentage
    depression_percentage = (np.sum(y_unlabeled_pred == 1) / len(y_unlabeled_pred)) * 100

    # if depression_percentage >= 60:
    #     print(f"Depression Percentage: {depression_percentage:.2f}%")
    # else:
    #     print(f"Your Depression Percentage is low, its: {depression_percentage:.2f}%")

    # Identify the top signs of depression from the user's tweets
    feature_names = vectorizer.get_feature_names()
    coef_indices = model.coef_[0]
    
    # Get the top 10 most significant terms for depression
    if len(coef_indices)>=11:
        top_depression_terms = [feature_names[index] for index in np.argsort(coef_indices)[-10:]]
    else:
        top_depression_terms = [feature_names[index] for index in np.argsort(coef_indices)[-10:]]
        
    
    print("Top Signs of Depression:")
    print(", ".join(top_depression_terms))
    depressed_wordcloud_text = ' '.join(unlabeled_df['Tweets'][y_unlabeled_pred == 1])
    reshaped_text = arabic_reshaper.reshape(depressed_wordcloud_text)
    bidi_text = get_display(reshaped_text)
    

    # Display a few rows of the preprocessed data with predictions
    print("Preprocessed Data with Predictions:")
    for index, row in unlabeled_df[['Tweets', 'Prediction']].head().iterrows():
        classification = "Depressed" if row['Prediction'] == 1 else "Not Depressed"
        color = "\033[1;31m" if row['Prediction'] == 1 else "\033[1;32m"
        print(f"{color}{row['Tweets']} - {classification}\033[0m")

    # Generate Word Cloud
    if not depressed_wordcloud_text:
        print("No depressed tweets found in the unlabeled set.")
    else:
        wordcloud_depressed = WordCloud(
            width=800, height=400, background_color='#fbfbfb',
            font_path='NotoNaskhArabic-Medium.ttf',
            max_words=50,  # Adjust the number of max words
            collocations=False  # Disable collocations
        ).generate(bidi_text)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud_depressed, interpolation='bilinear')
        plt.title('Word Cloud for Depressed Tweets')
        plt.axis('off')
        # Save or display the Word Cloud
        plt.savefig('depression_wordcloud.png')
        plt.show()
    return depression_percentage

def main():
    # Load your dataset
    dataset_path = 'rr.csv'
    df = pd.read_csv(dataset_path)

    # Preprocess tweets
    df["Tweets"] = df['Tweets'].apply(lambda x: preprocess(x))

    X = df['Tweets']
    y = df['Label']
    

    # ... (your data splitting code)
    combined_tweets = [(tweet, label) for tweet, label in zip(X, y)]

    # Separate depressed and non-depressed tweets
    depressed_tweets = [(tweet, label) for tweet, label in combined_tweets if label == 1]
    non_depressed_tweets = [(tweet, label) for tweet, label in combined_tweets if label == 2]



    # Split the data into training and testing sets with an equal number of depressed and non-depressed tweets
    X_train_depressed, X_test_depressed, y_train_depressed, y_test_depressed = train_test_split(
        [tweet for tweet, _ in depressed_tweets], [label for _, label in depressed_tweets],
        test_size=0.2, random_state=42, stratify=[label for _, label in depressed_tweets]
    )

    X_train_non_depressed, X_test_non_depressed, y_train_non_depressed, y_test_non_depressed = train_test_split(
        [tweet for tweet, _ in non_depressed_tweets], [label for _, label in non_depressed_tweets],
        test_size=0.2, random_state=42, stratify=[label for _, label in non_depressed_tweets]
    )
    # Combine the depressed and non-depressed training sets
    X_train = X_train_depressed + X_train_non_depressed
    y_train = y_train_depressed + y_train_non_depressed

    # Combine the depressed and non-depressed testing sets
    X_test = X_test_depressed + X_test_non_depressed
    y_test = y_test_depressed + y_test_non_depressed



    # Training
    best_model, vectorizer = train_model(X_train, y_train)

    # Testing
    y_pred=  test_model(best_model, vectorizer, X_test, y_test)
    depression_percentage = (np.sum(y_pred == 1) / len(y_pred)) * 100
    depressed_text = ' '.join(arabic_reshaper.reshape(tweet) for tweet, _ in depressed_tweets)
    reshaped_text = arabic_reshaper.reshape(depressed_text)
    bidi_text = get_display(reshaped_text)
    if not depressed_text:
        print("No depressed tweets found in the training set.")
    else:
        wordcloud_depressed = WordCloud(
            width=800, height=400, background_color='#fbfbfb',
            font_path='NotoNaskhArabic-Medium.ttf',
            max_words=50,  # Adjust the number of max words
            collocations=False  # Disable collocations
        ).generate(bidi_text)      
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud_depressed, interpolation='bilinear')
        plt.title('Word Cloud for Depressed Tweets')
        plt.axis('off')
        plt.savefig('dataset_wordcloud.png')
        plt.show()
    return vectorizer,depression_percentage,best_model
        
    
    


vectorizer,depression_percentage,best_model= main()
joblib.dump(best_model,'LR_Model.pkl')
joblib.dump(depression_percentage,'Saudi_percentage.pkl')
joblib.dump(vectorizer,'vectorizer.pkl')
