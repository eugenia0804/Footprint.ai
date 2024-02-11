import pandas as pd
import gensim
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json

def preprocess(text):
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in words]
    return tokens

def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    return [word for word in tokens if word.lower() not in stop_words]

def remove_punctuations(tokens):
    return [word for word in tokens if word.isalnum()]

def train_word2vec_model(texts, min_count=2):
    sentences = [preprocess(text) for text in texts]
    model = gensim.models.Word2Vec(sentences, min_count=min_count)
    return model

def get_word_similarities(model, target_word, tokens):
    word_similarities = {}
    for word in tokens:
        if word in model.wv.key_to_index:
            similarity = model.wv.similarity(target_word, word)
            word_similarities[word] = similarity
    return word_similarities

def generate_word_cloud(word_similarities, title):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_similarities)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title)
    plt.axis('off')
    plt.show()

def main(input_csv, target_word):
    nltk.download('punkt')
    nltk.download('stopwords')

    # Read CSV file
    df = pd.read_csv(input_csv)

    # Train Word2Vec model
    model = train_word2vec_model(df['text'])

    all_word_similarities = {}

    for index, row in df.iterrows():
        # Preprocess text data
        tokens = preprocess(row['text'])
        tokens = remove_stopwords(tokens)
        tokens = remove_punctuations(tokens)

        # Get word similarities
        word_similarities = get_word_similarities(model, target_word, tokens)

        # Generate word cloud with time range as title
        start_timestamp = row['start_timestamp']
        end_timestamp = row['end_timestamp']
        title = f"{start_timestamp} - {end_timestamp}"
        generate_word_cloud(word_similarities, title)

        # Convert float32 values to regular floats
        word_similarities = {word: float(similarity) for word, similarity in word_similarities.items()}

        # Save word similarities to dictionary
        all_word_similarities[title] = word_similarities

    # Save all word similarities to a JSON file
    with open('word2vec/word_similarities.json', 'w') as f:
        json.dump(all_word_similarities, f)


if __name__ == "__main__":
    input_csv = 'word2vec/keyword.csv'  # Replace with your input CSV file path
    target_word = 'Northwestern'  # Replace with your target word
    main(input_csv, target_word)
