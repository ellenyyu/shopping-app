import streamlit as st
from googleapiclient.discovery import build
import requests
from io import BytesIO
import base64
import zipfile

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


def zip_images(image_urls):
    
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for url in image_urls:
            file_name = url.split("/")[-1]
            response = requests.get(url)

            if response.status_code == 200:
                zip_file.writestr(f"{file_name}.jpg", response.content)
            else:
                st.warning(f"Failed to download image {file_name} (Status code: {response.status_code})")

    zip_data = zip_buffer.getvalue()
    zip_b64 = base64.b64encode(zip_data).decode()
    href = f'data:application/zip;base64,{zip_b64}'
    
    return href
