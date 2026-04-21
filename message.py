# Student Answer Evaluation System
# Regex Cleaning + Stopword Removal + Lemmatization + BoW Similarity

import re
import nltk
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# --------------------------------------------------
# Initialize Tools
# --------------------------------------------------
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# --------------------------------------------------
# Text Preprocessing Function
# --------------------------------------------------
def preprocess_text(text):
    text = text.lower()                          # lowercase
    text = re.sub(r'[^a-zA-Z\s]', '', text)     # remove punctuation/numbers
    words = text.split()                        # tokenize
    
    # remove stopwords + lemmatization
    words = [lemmatizer.lemmatize(word) for word in words
             if word not in stop_words]
    
    return " ".join(words)

# --------------------------------------------------
# Model Answer and Student Answer
# --------------------------------------------------
model_answer = """
Python is a high level programming language used for web development,
data science, machine learning, and automation.
"""

student_answer = """
Python is an easy programming language used in machine learning,
web applications, data analysis and automation.
"""

# --------------------------------------------------
# Preprocess Both Answers
# --------------------------------------------------
clean_model = preprocess_text(model_answer)
clean_student = preprocess_text(student_answer)

print("Model Answer Cleaned:")
print(clean_model)

print("\nStudent Answer Cleaned:")
print(clean_student)

# --------------------------------------------------
# Bag of Words Vectorization
# --------------------------------------------------
vectorizer = CountVectorizer()

vectors = vectorizer.fit_transform([clean_model, clean_student])

# --------------------------------------------------
# Cosine Similarity
# --------------------------------------------------
similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

# --------------------------------------------------
# Score Calculation
# --------------------------------------------------
score = round(similarity * 10, 2)   # out of 10

print("\nSimilarity Score:", round(similarity * 100, 2), "%")
print("Marks Awarded:", score, "/10")