import streamlit as st 
import requests
from bs4 import BeautifulSoup
import re
import google.auth
from googleapiclient.discovery import build
from datetime import datetime

def get_channel_id_from_url(youtube_url):
    try:
        # Fetch the HTML content of the YouTube channel page
        response = requests.get(youtube_url)
        response.raise_for_status()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the channel ID in the parsed HTML using a regular expression
        channel_id_pattern = re.compile(r'"channelId":"([^"]+)"')
        match = channel_id_pattern.search(str(soup))

        if match:
            return match.group(1)
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def extract_links(text):
    # Use a regular expression to find URLs in the text
    url_pattern = re.compile(r'https?://\S+')
    return url_pattern.findall(text)

@st.cache_data
def get_video_data(api_key, channel_id, start_date, end_date, max_results = 1000):
    youtube = build("youtube", "v3", developerKey=api_key, http=http)

    # Get the uploads playlist ID for the channel
    playlist_response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()
    playlist_id = playlist_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # Retrieve videos from the uploads playlist
    playlist_items_snippets = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=max_results
    ).execute()

    video_info = []
    #st.write(playlist_items_snippets)
    for item in playlist_items_snippets["items"]:
        video_id = item["snippet"]["resourceId"]["videoId"]
        video_title = item["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_pub_time = item["snippet"]["publishedAt"]

        upload_date = datetime.strptime(video_pub_time, "%Y-%m-%dT%H:%M:%SZ")

        # Check if the video is within the specified date range
        if start_date <= upload_date <= end_date:
            # Get the video description
            video_response = youtube.videos().list(
                part="snippet",
                id=video_id
            ).execute()

            video_description = video_response["items"][0]["snippet"]["description"]

            # Extract links from the video description
            links = extract_links(video_description)
            if links:
                video_info.append({"title": video_title, "url": video_url, "links": links})

    return video_info