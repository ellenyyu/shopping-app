import streamlit as st
from googleapiclient.discovery import build
import requests
import os

@st.cache_data
def get_image_urls(api_key, cx, search_term, num_results):
    results_per_request = 10
    num_requests = -(-num_results // results_per_request)  # Equivalent to math.ceil(num_results / results_per_request)
    image_urls = []


    service = build("customsearch", "v1", developerKey=api_key)

    for i in range(num_requests):
        start_index = i * results_per_request + 1
        result = service.cse().list(q=search_term, cx=cx, searchType='image', num=results_per_request, start=start_index).execute()

        # Extract image URLs from the API response
        image_urls.extend(item['link'] for item in result.get('items', []))

    return image_urls[:num_results]

def download_file(url, save_directory):
    # Create the save directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)

    # Extract the file name from the URL
    file_name = os.path.join(save_directory, url.split("/")[-1])

    # Download the file
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Save the file to the specified directory
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f"File downloaded successfully: {file_name}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")