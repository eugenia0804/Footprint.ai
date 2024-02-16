import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# Load the CSV file
file_path = "word2vec/data/inside.csv"
df = pd.read_csv(file_path)

# Create the directory if it doesn't exist
output_dir = "word2vec/images/inside-freq"
os.makedirs(output_dir, exist_ok=True)

# Define words to exclude
exclude_words = [""]  # Add the words you want to exclude

# Iterate over each row
for index, row in df.iterrows():
    # Extract necessary information
    text = row['text']
    start_timestamp = row['start_timestamp']
    end_timestamp = row['end_timestamp']
    
    # Remove excluded words from the text
    if file_path == "word2vec/data/inside.csv":
        for word in exclude_words:
            text = text.replace(word, "")
    
    # Generate word cloud based on word frequency
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Plot the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f"{start_timestamp} - {end_timestamp}")
    plt.axis('off')
    
    # Save the word cloud image with a filename based on timestamps
    image_filename = os.path.join(output_dir, f"{start_timestamp}_{end_timestamp}.png")
    plt.savefig(image_filename)
    plt.close()  
