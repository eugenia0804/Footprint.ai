import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = "AAAAAAAAAAAAAAAAAAAAAAYerwEAAAAAD4oZ%2BEFaIpI3SVTB3vkL8%2F5DxCQ%3D1UNjoxnSueJQjBj1hklce7PA3HtWAPMTi8jIE4IaAqobbcpPdo"

search_url = "https://api.twitter.com/2/tweets/search/recent"

# Include all tweet fields in 'tweet.fields'
query_params = {'query': 'Northwestern Football lang:en', 'tweet.fields': 'attachments,author_id,card_uri,context_annotations,conversation_id,created_at,edit_controls,edit_history_tweet_ids,entities,geo,id,in_reply_to_user_id,lang,note_tweet,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld', 'max_results': 10}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def main():
    # Initialize an empty list to store the results
    all_results = []

    # Loop until there is no more next token
    while True:
        # Make a request to get results
        json_response = connect_to_endpoint(search_url, query_params)

        # Append the results to the list
        all_results.extend(json_response['data'])

        # Check if there is a next token
        next_token = json_response.get('meta', {}).get('next_token')
        if not next_token:
            break

        # Update the next token for the next request
        query_params['next_token'] = next_token

    # Store all results into a JSON file
    with open('twitter_results.json', 'w') as json_file:
        json.dump(all_results, json_file, indent=4, sort_keys=True)

if __name__ == "__main__":
    main()
