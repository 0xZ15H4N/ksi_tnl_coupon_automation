from googleapiclient.discovery import build
from PIL import Image
import requests
import time
import re
import subprocess
import os
import ocr
from dotenv import load_dotenv
load_dotenv()
# Your YouTube API key
API_KEY = os.getenv("API_KEY")
# Channel ID
CHANNEL_ID = os.getenv("CHANNEL_ID") 
# Keyword (if you want to filter by title) - otherwise keep empty
KEYWORD = ""

# YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

# Function to download image from URL
def download_image(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

# Function to check if thumbnail text contains money pattern
def contains_money(text):
    # Look for $ or € followed by 100-1000
    match = re.search(r'[\$\€]\s*\d{3,4}', text)
    return bool(match)

# Function to check for new videos
def check_for_new_videos():
    request = youtube.search().list(
        part="snippet",
        channelId=CHANNEL_ID,
        order="date",
        maxResults=5
    )
    response = request.execute()

    for item in response["items"]:
        video_title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        thumbnail_url = item["snippet"]["thumbnails"]["high"]["url"]

        print(f"Checking video: {video_title}")

    download_image(thumbnail_url, "./temp_youtube_download/thumbnail.jpg")

#####################################################################
####### WE WILL USE EASYOCR FOR SCANNING TEXT FROM THE IMAGE ########
#####################################################################
    text = ocr.init('thumbnail.jpg')
    print(f"Extracted text: {text}")
    if contains_money(text):
        print(f"🟢 New video found related to money!")
        print(f"Title: {video_title}")
        print(f"Link: {video_url}")
        return [True,video_title,video_url]

    return [False,"",""]

# Main loop
while True:
    print("Checking for new videos...")
    metadata = check_for_new_videos()
    if metadata[0]:
        print("Monitoring stopped after finding a relevant video.")
        subprocess.run(["python3","./main.py","--link",f"{metadata[2]}"])
        time.sleep(15)
        subprocess.run(["python3","./main.py","--link",f"{metadata[2]}"])
