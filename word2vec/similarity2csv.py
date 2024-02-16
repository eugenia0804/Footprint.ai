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
    row_data.update(value)  # Add word scores to the row data
    rows.append(row_data)

# Create DataFrame from the list of rows
df = pd.DataFrame(rows)

# Fill missing values with 0
df.fillna(0, inplace=True)

# Reverse the order of all rows
df_reversed = df[::-1]

# Save reversed DataFrame to CSV
df_reversed.to_csv("word2vec/word_similarities.csv", index=False)
