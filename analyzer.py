import string
from collections import Counter

def analyze_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Split into words
    words = text.split()
    
    # Word count
    word_count = len(words)
    
    # Sentence count (simple approximation)
    sentence_count = text.count('.') + text.count('!') + text.count('?')
    
    # Word frequency
    word_freq = Counter(words)
    most_common = word_freq.most_common(5)
    
    # Results
    print("Total words:", word_count)
    print("Total sentences:", sentence_count)
    print("Most common words:")
    for word, count in most_common:
        print(f"{word}: {count}")

# Example usage
text = input("Enter your text:\n")
analyze_text(text)