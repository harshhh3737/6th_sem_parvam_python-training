def text_analyzer(text):
    stop_words = {
        "the", "is", "a", "an", "in", "it", "of", "and",
        "to", "for", "on", "at", "was", "be"
    }

    # Basic stats
    words = text.lower().split()
    sentences = [s for s in text.split(".") if s.strip()]

    # Clean words + remove stopwords
    clean_words = []
    for w in words:
        word = w.strip(".,!?;:")
        if word not in stop_words:
            clean_words.append(word)

    # Word frequency
    freq = {}
    for word in clean_words:
        freq[word] = freq.get(word, 0) + 1

    # Top 5 words
    top_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]

    # Output
    print(f"Total words     : {len(words)}")
    print(f"Unique words    : {len(set(words))}")
    print(f"Sentences       : {len(sentences)}")
    print(f"After stop words: {len(clean_words)} words remain")
    print(f"Top 5 words     : {top_words}")


# Sample input
sample_text = """Python is a great language. Python is used for AI and data science. 
Many developers love Python because it is simple and powerful."""

text_analyzer(sample_text)