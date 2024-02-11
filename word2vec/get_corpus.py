import pandas as pd
import json
import os

import re

def remove_links(text):
    return re.sub(r'http\S+', '', text)

def get_data():
    df_inside = pd.DataFrame() 
    df_keyword = pd.DataFrame()
    metadata_file = "twitter/tweets/metadata.json"
    
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as file:
            metadata = json.load(file) 
            for entry in metadata:
                query = entry.get("query", "")
                tweet_id = entry.get("id", "")
                tweet_count = entry.get("count", "")
                filename = f"twitter/tweets/{tweet_id}_tweets_{tweet_count}.csv"
                if os.path.exists(filename):
                    df = pd.read_csv(filename)
                    if query.startswith("from:insidenu"):
                        df_inside = pd.concat([df_inside, df], ignore_index=True)
                    elif query.startswith("Northwestern"):
                        df_keyword = pd.concat([df_keyword, df], ignore_index=True)
                        
        print(f"All insideNU tweets has been combined, with total record of {len(df_inside)}")
        print(f"All insideNU tweets has been combined, with total record of {len(df_keyword)}")
                      
    inside = df_inside.drop_duplicates(subset=["Tweet ID"])
    keyword = df_keyword.drop_duplicates(subset=["Tweet ID"])
    
    print(f"After deduplication, number of tweets from insidenu = {len(inside)}")
    print(f"After deduplication, number of tweets from keyword search = {len(keyword)}")

    return inside, keyword

def get_text_by_week(df, output_file):
    # Convert 'Timestamp' column to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%dT%H:%M:%S.%fZ')
    
    # Handle NaN values in 'Content' column
    df['Content'] = df['Content'].fillna('')  # Replace NaN with empty string
    
    # Group by week and concatenate text data, then remove links
    text_by_week = df.groupby(df['Timestamp'].dt.strftime('%U')).agg(
        text=('Content', ' '.join),
        count=('Content', 'count'),
        start_timestamp=('Timestamp', 'min'),
        end_timestamp=('Timestamp', 'max')
    )
    text_by_week['text'] = text_by_week['text'].apply(remove_links)
    
    # Reset index to make 'Timestamp' a column again
    text_by_week.reset_index(inplace=True)
    
    # Save DataFrame to CSV
    text_by_week.to_csv(output_file, index=False)



df_inside, df_keyword = get_data()
get_text_by_week(df_inside,'word2vec/inside.csv')
get_text_by_week(df_keyword,'word2vec/keyword.csv')
