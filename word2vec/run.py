import pandas as pd
import gensim
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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

def train_word2vec_model(texts, min_count=5):
    sentences = [preprocess(text) for text in texts]
    model = gensim.models.Word2Vec(sentences, min_count=min_count)
    return model

def get_word_similarities(model, target_word, tokens):
    word_similarities = {}
    for word in tokens:
        if word in model.wv.key_to_index:  # Checking if word exists in the vocabulary
            similarity = model.wv.similarity(target_word, word)
            word_similarities[word] = similarity
    return word_similarities

def generate_word_cloud(word_similarities):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_similarities)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def main(input_csv, target_word):
    nltk.download('punkt')
    nltk.download('stopwords')

    # Read CSV file
    df = pd.read_csv(input_csv)

    # Train Word2Vec model
    model = train_word2vec_model(df['text'])

    for index, row in df.iterrows():
        # Preprocess text data
        tokens = preprocess(row['text'])
        tokens = remove_stopwords(tokens)
        tokens = remove_punctuations(tokens)

        # Get word similarities
        word_similarities = get_word_similarities(model, target_word, tokens)
        print(word_similarities)

        # Generate word cloud
        generate_word_cloud(word_similarities)


if __name__ == "__main__":
    input_csv = 'word2vec/keyword.csv'  # Replace with your input CSV file path
    target_word = 'NU'  # Replace with your target word
    main(input_csv, target_word)
