# Import necessary libraries and modules
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import string
from camel_tools.tokenizers.morphological import MorphologicalTokenizer
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tagger.default import DefaultTagger
from camel_tools.utils.normalize import normalize_unicode
from camel_tools.utils.dediac import dediac_ar
import nltk
import demoji

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Define Arabic and English punctuations
arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
english_punctuations = string.punctuation
punctuations_list = arabic_punctuations + english_punctuations

# Load the Maximum Likelihood Estimation Disambiguator
mle = MLEDisambiguator.pretrained()


def preprocess(tweet):
    """
    Preprocesses an Arabic tweet.
    
    This function tokenizes, tags, disambiguates, normalizes, and dediacs the given tweet.

    Parameters:
    - tweet (str): The input Arabic tweet.

    Returns:
    - str: The preprocessed tweet.
    """
    sentence = processDocument(tweet)
    normal_sen = sentence.split()
    
    # Tokenize and tag the tweet
    d1tok_tokenizer = MorphologicalTokenizer(disambiguator=mle, scheme='d1tok', split='True')
    Tok_sen = d1tok_tokenizer.tokenize(normal_sen)
    tagger = DefaultTagger(mle, 'pos')
    tags = tagger.tag(Tok_sen)
    sentence = ''

    for i in range(len(Tok_sen)):
        if tags[i] == "noun" or tags[i] == "adj" or tags[i] == "verb":
            sentence += " " + Tok_sen[i]

    # Disambiguate the tokens
    Tok_sen = d1tok_tokenizer.tokenize(sentence.split())
    disambiguated = mle.disambiguate(Tok_sen)
    stem_word = ' '.join([d.analyses[0].analysis['lex'] for d in disambiguated])
    
    # Normalize and dediac the disambiguated tokens
    sentence = normalize_unicode(stem_word)
    sentence = dediac_ar(sentence)

    return sentence


# Function to remove punctuations from text
def remove_punctuations(text):
    """
    Removes punctuations from the given text.

    Parameters:
    - text (str): The input text.

    Returns:
    - str: The text with punctuations removed.
    """
    translator = str.maketrans('', '', punctuations_list)

    return text.translate(translator)


# Function to normalize Arabic text
def normalize_arabic(text):
    """
    Normalizes Arabic text.

    Parameters:
    - text (str): The input Arabic text.

    Returns:
    - str: The normalized Arabic text.
    """
    text = re.sub("[إأآٱا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    return text


# Function to remove repeating characters from text
def remove_repeating_char(text):
    """
    Removes repeating characters from the given text.

    Parameters:
    - text (str): The input text.

    Returns:
    - str: The text with repeating characters removed.
    """
    return re.sub(r'(.)\1{2,}', r'\1', text)


# Function to remove repeated words from text
def remove_repeated_words(text):
    """
    Removes repeated words from the given text.

    Parameters:
    - text (str): The input text.

    Returns:
    - str: The text with repeated words removed.
    """
    words = text.split()
    unique_words = list(set(words))
    return ' '.join(unique_words)


# Function to preprocess documents
def processDocument(doc):
    """
    Preprocesses a document by removing URLs, mentions, hashtags, punctuations, digits, emojis, etc.

    Parameters:
    - doc (str): The input document.

    Returns:
    - str: The preprocessed document.
    """
    # Replace @username with empty string
    doc = re.sub(r'@[^\s]+', ' ', doc)
    # Replace underscore (_) with space
    doc = re.sub(r'_', ' ', doc)
    # Replace newline characters with space
    doc = re.sub(r'\n', ' ', doc)
    # Remove lowercase and uppercase English letters
    doc = re.sub(r'[a-z,A-Z]', '', doc)
    # Remove digits
    doc = re.sub(r'\d', '', doc)
    # Convert www.* or https?://* to " "
    doc = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', ' ', doc)
    # Replace #word with word
    doc = re.sub(r'#([^\s]+)', r'\1', doc)
    # remove punctuations
    doc = remove_punctuations(doc)
    # # normalize the tweet
    doc = normalize_arabic(doc)
    # remove repeated letters
    doc = remove_repeating_char(doc)
    doc = re.sub(r'\W', ' ', doc)
    # Remove emojis
    doc = demoji.replace(doc, repl="")
    # Remove extra whitespaces
    doc = re.sub(r'\s+', ' ', doc).strip()

    return doc


def remove_stopwords(text):
    """
    Removes stopwords and unwanted words from the given text.

    Parameters:
    - text (str): The input text.

    Returns:
    - str: The text with stopwords and unwanted words removed.
    """
    # Define a list of unwanted words
    unwanted_words = ["انا", "انت", "هو", "هي", "نحن", "انتم", "هم",
                      "هن", 'الي', 'اني', 'ان', "علي", 'الا', 'لان', 'لكن', 'او',
                      "كنت", "كان", 'شاء', "مرة", "يوم", "بس", "قلت", "وقت", "وقف", "الله", "اللهم", "رب", "يارب"]
    
    # Define a regular expression pattern to remove 'و' at the beginning of words
    pattern = re.compile(r'\bو(\w+)\b', flags=re.UNICODE)

    # Use sub() to replace matches with an empty string
    cleaned_text = pattern.sub(r'\1', text)
    
    # Retrieve Arabic stopwords using NLTK
    stop_words = set(stopwords.words("arabic"))

    # Tokenize the cleaned text
    word_tokens = word_tokenize(cleaned_text)

    # Filter out stopwords, unwanted words, and words with length less than 2 characters
    text = ' '.join([word for word in word_tokens if word.strip() not in stop_words and word.strip() not in unwanted_words and len(word.strip()) > 2])

    return text

