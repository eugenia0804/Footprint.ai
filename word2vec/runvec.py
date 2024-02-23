import pandas as pd
import gensim
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json
import os
from matplotlib.animation import FuncAnimation

def preprocess(text):
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in words]
    return tokens

def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    return [word.lower() for word in tokens if word.lower() not in stop_words]

def remove_punctuations(tokens):
    return [word.lower() for word in tokens if word.isalnum()]

def custom_token_generation(tokens):
    custom_tokens = []
    i = 0
    while i < len(tokens):
        if i < len(tokens) - 1 and tokens[i].lower() == 'pat' and tokens[i+1].lower() == 'fitzgerald':
            custom_tokens.append('Pat Fitzgerald')
            i += 2
        elif tokens[i].lower() in ['nu', 'northwestern']:
            custom_tokens.append('Northwestern')
            i += 1
        elif tokens[i].lower() in ['football', 'Football']:
            custom_tokens.append('football')
            i += 1
        else:
            custom_tokens.append(tokens[i])
            i += 1
    return custom_tokens

def train_word2vec_model(texts, min_count=3):
    sentences = [preprocess(text) for text in texts]
    model = gensim.models.Word2Vec(sentences, min_count=min_count)
    return model

def get_word_similarities(model, target_word, tokens):
    word_similarities = {}
    try:
        for word in tokens:
            if word in model.wv.key_to_index:
                similarity = model.wv.similarity(target_word, word)
                word_similarities[word] = similarity
    except KeyError as e:
        print(f"Word '{e.args[0]}' not present in the Word2Vec model.")
    return word_similarities


def generate_word_cloud(word_similarities, title, save_dir, index):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, f"wordcloud_{index}.png")
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_similarities)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title)
    plt.axis('off')
    plt.savefig(save_path)
    #plt.show
    plt.close()


def main(input_csv, target_word):
    nltk.download('punkt')
    nltk.download('stopwords')

    # Read CSV file
    df = pd.read_csv(input_csv)

    all_word_similarities = {}

    save_dir = 'word2vec/images/new_keyword-tweets'
    for index, row in df.iterrows():
        # Preprocess text data
        tokens = preprocess(row['text'])
        tokens = remove_stopwords(tokens)
        tokens = remove_punctuations(tokens)
        tokens = custom_token_generation(tokens)

        # Train Word2Vec model
        model = train_word2vec_model([' '.join(tokens)])  # Join tokens into a single string

        # Check if target word is in the model's vocabulary
        if target_word in model.wv.key_to_index:
            # Get word similarities
            word_similarities = get_word_similarities(model, target_word, tokens)

            # Generate word cloud with time range as title
            start_timestamp = row['start_timestamp']
            end_timestamp = row['end_timestamp']
            title = f"{start_timestamp} - {end_timestamp}"
            generate_word_cloud(word_similarities, title, save_dir, index)

            # Convert float32 values to regular floats
            word_similarities = {word: float(similarity) for word, similarity in word_similarities.items()}

            # Save word similarities to dictionary
            all_word_similarities[title] = word_similarities
        else:
            print(f"Target word '{target_word}' not present in the Word2Vec model for row {index}.")

    # Save all word similarities to a JSON file
    with open('word2vec/word_similarities.json', 'w') as f:
        json.dump(all_word_similarities, f)


if __name__ == "__main__":
    input_csv = 'word2vec/data/keyword.csv'  # Replace with your input CSV file path
    target_word = 'Northwestern'  # Replace with your target word
    main(input_csv, target_word)
