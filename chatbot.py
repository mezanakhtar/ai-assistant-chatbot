import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())       # Tokenize & lowercase
    tokens = [lemmatizer.lemmatize(t) for t in tokens]  # Lemmatize
    return " ".join(tokens)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json, random

# Load intents
with open("intents.json") as f:
    data = json.load(f)

# Flatten all patterns + track which intent each belongs to
patterns, tags = [], []
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        patterns.append(preprocess(pattern))
        tags.append(intent["tag"])

# Build TF-IDF matrix
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(patterns)

def get_response(user_input):
    processed = preprocess(user_input)
    user_vec = vectorizer.transform([processed])
    similarities = cosine_similarity(user_vec, tfidf_matrix)
    best_match = similarities.argmax()
    
    if similarities[0][best_match] < 0.6:   # Confidence threshold
        return "Sorry, I didn't understand that. Can you rephrase?"
    
    matched_tag = tags[best_match]
    for intent in data["intents"]:
        if intent["tag"] == matched_tag:
            return random.choice(intent["responses"])