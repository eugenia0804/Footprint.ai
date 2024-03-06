import pandas as pd
import json

# Load JSON data
with open("word2vec/word_similarities.json", "r") as json_file:
    data = json.load(json_file)

# Initialize an empty list to hold rows
rows = []

# Iterate over the JSON data and populate the list
for key, value in data.items():
    end_time = key.split(" - ")[1]  # Extract end time from key
    row_data = {'end_time': end_time}
    # Find top 10 words with highest similarity score
    top_words = sorted(value.items(), key=lambda x: x[1], reverse=True)[:20]
    for word, score in top_words:
        row_data[word] = score * 100  # Multiply each value by 100
    rows.append(row_data)

# Create DataFrame from the list of rows
df = pd.DataFrame(rows)

# Reverse the order of all rows
df_reversed = df[::-1]

# Transpose the DataFrame
df_transposed = df_reversed.transpose()

#df_transposed.ffill(axis=1, inplace=True)

print(df_transposed.columns.tolist())
print(len(df_transposed.columns.tolist()) == len(set(df_transposed.columns.tolist())))

# Save transposed DataFrame to CSV
df_transposed.to_csv("word2vec/word_similarities_transposed.csv", index=True)
