
import streamlit as st
import googleapiclient.discovery
import re

def extract_links_from_description(description):
    return re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', description)

@st.cache_data
def get_video_details(_youtube, video_ids):
    request = _youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    )

    response = request.execute()

    videos = []
    for item in response["items"]:
        video = {
            "title": item["snippet"]["title"],
            "video_id": item["id"],
            "url": f"https://www.youtube.com/watch?v={item['id']}",
            "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
            "views": item["statistics"]["viewCount"],
            "description": item["snippet"]["description"],   
        }
        video["links"]= extract_links_from_description(video['description'])
        videos.append(video)

    return videos

@st.cache_data
def search_youtube_videos(api_key, search_term, return_by, max_results):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    request = youtube.search().list(
        q=search_term,
        type="video",
        part="id,snippet",
        maxResults = max_results,
        order = return_by
    )

    response = request.execute()

    video_ids = []
    for item in response["items"]:
        video_ids.append(item["id"]["videoId"])

    videos = get_video_details(youtube, video_ids)

    return videos
