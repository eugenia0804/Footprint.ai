import pandas as pd
import json
import os
import re
import matplotlib.pyplot as plt


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
    print(inside)

    return inside, keyword

inside, keyword = get_data()

def check_cocurrent(text, center_keyword, comparison_keyword):
    if isinstance(text, str):
        return bool(re.search(r'\b{}\b'.format(center_keyword), text, re.IGNORECASE)) and bool(re.search(r'\b{}\b'.format(comparison_keyword), text, re.IGNORECASE))
    else:
        return False


def calculate_weekly_percentage_df(df, center_keyword, comparison_keywords):
    weekly_percentages = {}
    for comparison_keyword in comparison_keywords:
        df['cocurrent'] = df['Content'].apply(lambda x: check_cocurrent(x, center_keyword, comparison_keyword))
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['week'] = df['Timestamp'].dt.strftime('%Y-%U')
        weekly_counts = df.groupby('week')['cocurrent'].sum()  # Count occurrences where both keywords appear together
        total_entries = df.groupby('week').size()  # Total number of entries per week
        weekly_percentage = (weekly_counts / total_entries) * 100  # Calculate percentage
        weekly_percentages[comparison_keyword] = weekly_percentage

    # Create a DataFrame from the weekly_percentages dictionary
    df_weekly_percentage = pd.DataFrame(weekly_percentages)
    
    # Save the DataFrame to a CSV file
    df_weekly_percentage.to_csv(f'co/weekly_percentage_with_{center_keyword}.csv', index=True)  # Change 'weekly_percentage_data.csv' to desired filename
    return df_weekly_percentage

def calculate_weekly_percentage_df_7days(df, center_keyword, comparison_keywords):
    weekly_percentages = {}
    for comparison_keyword in comparison_keywords:
        df['cocurrent'] = df['Content'].apply(lambda x: check_cocurrent(x, center_keyword, comparison_keyword))
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['interval'] = df['Timestamp'].dt.floor('7D')  # Round down to the nearest 7-day interval
        weekly_counts = df.groupby('interval')['cocurrent'].sum()  # Count occurrences where both keywords appear together
        total_entries = df.groupby('interval').size()  # Total number of entries per interval
        weekly_percentage = (weekly_counts / total_entries) * 100  # Calculate percentage
        weekly_percentages[comparison_keyword] = weekly_percentage

    # Create a DataFrame from the weekly_percentages dictionary
    df_weekly_percentage = pd.DataFrame(weekly_percentages)
    
    summed_data = {}
    words = ["Scandal", "Misconduct", "Haz", "Fir", "Alleg", "Lawsuit", "Su"]
    for word in words:
        variations = [col for col in df_weekly_percentage.columns if word in col]
        summed_data[word] = df_weekly_percentage[variations].sum(axis=1)

    # Creating a new DataFrame with summed data
    summed_df = pd.DataFrame(summed_data)

    print(summed_df)
    
    # Save the DataFrame to a CSV file
    summed_df.to_csv(f'co/weekly_percentage_with_{center_keyword}_7days_sum.csv', index=True)  # Change 'weekly_percentage_data.csv' to desired filename
    return df_weekly_percentage



'''
def plot_weekly_percentage(weekly_percentages, center_keyword, comparison_keywords):
    plt.figure(figsize=(10, 6))
    for comparison_keyword in comparison_keywords:
        plt.plot(weekly_percentages[comparison_keyword].index, weekly_percentages[comparison_keyword].values, marker='o', label=f'{center_keyword} and {comparison_keyword}')
    plt.title(f'Percentage of Cocurrency of {center_keyword} and {", ".join(comparison_keywords)} by Week')
    plt.xlabel('Week')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show
    plt.savefig("co/image.png")
'''

df = keyword
center_keyword = "baseball"
comparison_keywords = ["Scandal", "Scandals", "Misconduct", "Misconducts", "Hazing", "Hazed", "Hazes", "Haze", "Firing", "Fired", "Fire", "Fires", "Allegations", "Allegation", "Allege", "Alleges", "Alleged", "Alleging", "Lawsuit", "Lawsuits", "Sue", "Sues", "Sued", "Suing"]

calculate_weekly_percentage_df_7days(df, center_keyword, comparison_keywords)

#plot_weekly_percentage(weekly_percentages, center_keyword, comparison_keywords)
