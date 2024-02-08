from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud(dict):
    # Create a WordCloud object
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict)

    # Display the generated word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Example usage
data_dict = {"python": 30, "programming": 25, "data": 20, "wordcloud": 15, "example": 10}
generate_wordcloud(data_dict)