from googleapiclient.discovery import build
import requests
import time
import re
import subprocess
import os
import ocr
import time
import alert_me 
from dotenv import load_dotenv
from datetime import datetime,time as tm
import time
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
        maxResults=1
    )
    response = request.execute()

    for item in response["items"]:
        video_title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        thumbnail_url = item["snippet"]["thumbnails"]["high"]["url"]
        

    download_image(thumbnail_url, "./temp_youtube_download/thumbnail.jpg")

#####################################################################
##################### GOOGLE VISION AI ##############################
#####################################################################

    text = ocr.init('./temp_youtube_download/thumbnail.jpg')
    if contains_money(text[0]):
        print(f"🟢 New video found related to money!")
        print(f"Title: {video_title}")
        print(f"Link: {video_url}")
        return [True,video_title,video_url,text]

    return [False,"","",""]


print("Scanning in Every 2.4hr")
print("Scanning starting in 3....2....1...")
# Main loop
while True:
    print("Scaning for new video")
    alert_me.send_email(os.getenv("EMAIL_"),os.getenv("APP_PASS"),os.getenv("CLIENT"),"HITTING THE Youtube_data_V3/?search api","Finding the latest video??")
    metadata = check_for_new_videos()
    if metadata[0]:
        print("EMAIL SENDED")
        alert_me.send_email(sender= os.getenv("EMAIL_"),password = os.getenv("APP_PASS"),recipient =os.getenv("CLIENT"),subject="KSI NEW VIDEO",body=f"WAKE UP! KSI DROPPED NEW VIDEO {metadata[2]} {metadata[3]}")
        print("Monitoring stopped after finding a relevant video.")
        subprocess.run(["python3","./main.py","--link",f"{metadata[2]}"])
    time.sleep(8640) # scan in every 2.4 hrs 
