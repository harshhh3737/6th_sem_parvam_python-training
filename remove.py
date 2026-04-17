import re

def tokenize_and_clean(sentence):
    # Convert to lowercase (optional but common in NLP)
    sentence = sentence.lower()
    
    # Remove punctuation using regex and keep only words
    tokens = re.findall(r'\b\w+\b', sentence)
    
    return tokens


# Example usage
text = "Hello Harshala! Welcome to NLP. Let's build AI models."
tokens = tokenize_and_clean(text)

print(tokens)