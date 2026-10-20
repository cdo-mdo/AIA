from collections import Counter

def laplace_smoothing(ngrams, vocab_size):
    ngrams_counts = Counter(ngrams)
    smoothed_ngrams = {ngram: (count + 1) / (len(ngrams) + vocab_size) for ngram, count in ngrams_counts.items()}

    return smoothed_ngrams

ngrams = [('Geeks', 'for'), ('for', 'Geeks'), ('Geeks', 'Community')]
vocab_size = 5

smoothed_ngrams = laplace_smoothing(ngrams, vocab_size)
print("Smoothed N-grams:", smoothed_ngrams)

