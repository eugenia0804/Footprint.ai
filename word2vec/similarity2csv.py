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
    # Multiply each value by 100
    row_data.update({k: v * 100 for k, v in value.items()})
    rows.append(row_data)

# Create DataFrame from the list of rows
df = pd.DataFrame(rows)

# Fill missing values with 0
#df.fillna(0, inplace=True)

# Reverse the order of all rows
df_reversed = df[::-1]

# Transpose the DataFrame
df_transposed = df_reversed.transpose()

print(df_transposed.columns.tolist())
print(len(df_transposed.columns.tolist()) == len(set(df_transposed.columns.tolist())))

# Save transposed DataFrame to CSV
df_transposed.to_csv("word2vec/word_similarities_transposed.csv", index=True)
