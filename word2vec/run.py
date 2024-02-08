import gensim
from gensim.parsing.preprocessing import remove_stopwords
import nltk
from nltk.tokenize import word_tokenize

# Load NLTK stopwords
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('english'))

# Read the text data
with open('corpus.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Remove stopwords and tokenize the text
text_without_stopwords = remove_stopwords(text)
tokens = word_tokenize(text_without_stopwords)

# Remove punctuations
tokens = [word for word in tokens if word.isalnum()]

# Save the tokenized data
with open('corpus2.txt', 'w', encoding='utf-8') as file:
    file.write(" ".join(tokens))

# Train the Word2Vec model
sentences = gensim.models.word2vec.Text8Corpus("corpus2.txt")
model = gensim.models.Word2Vec(sentences, min_count=2)  # Ensure words with count more than 1 are included

# Get word similarities
word_similarities = {}
for word in model.wv.index_to_key:
    if model.wv.get_vecattr(word, "count") > 1:
        similarity = model.wv.similarity('AI', word)
        word_similarities[word] = similarity

# Sort word similarities by similarity values in descending order
sorted_word_similarities = sorted(word_similarities.items(), key=lambda x: x[1], reverse=True)

# Print word similarities in ranked order
for word, similarity in sorted_word_similarities:
    print(f"The similarity between 'AI' and '{word}' is: {similarity}")
