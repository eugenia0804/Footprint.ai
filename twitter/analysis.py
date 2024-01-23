import json

def count_entries(json_file_path):
    # Read the JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Count the number of entries
    num_entries = len(data)

    return num_entries

if __name__ == "__main__":
    # Replace 'twitter_results.json' with the actual path to your JSON file
    json_file_path = 'twitter_results.json'

    # Call the function to count entries
    num_entries = count_entries(json_file_path)

    # Print the result
    print(f"Number of entries in the JSON file: {num_entries}")