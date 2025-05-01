import subprocess
import re
import argparse
import amazon_bot
import cleaner
import ocr
import video_detection
import alert_me
import os

# Step 1: Download video and subtitles
def download_video_and_subs(url,temp_dir):
    # Download the vide
    subprocess.run(["yt-dlp", "--cookies", "cookie.txt", "-f", "bestvideo+bestaudio", "-o", os.path.join(temp_dir, "video.mp4"), url])

# ------------ Main Execution --------------

if __name__ == "__main__":
    # Enter the YouTube video URL
    parser = argparse.ArgumentParser(description="Process a video link.")
# Optional argument --link
    parser.add_argument("--link", required=True, help="The URL of the video")
    args = parser.parse_args()
    temp_dir = os.path.expanduser("~/ksi_tnl/temp_youtube_download")
    video_url = args.link        
    # Download video and subtitles
    download_video_and_subs(video_url,temp_dir)
    
    video_detection.main()

    with open("results.txt", "r", encoding="utf-8") as f:
        text = f.read()

# Match exactly: 4-part - 6-part - 4-part, optionally spaced, no timestamp/no prefix
    pattern = r'\b(?:[\w@#$%^&*]{1,2}\s*){4}-\s*(?:[\w@#$%^&*]{1,2}\s*){6}-\s*(?:[\w@#$%^&*]{1,2}\s*){4}\b'

# Find all matches
    matches = re.findall(pattern, text)

# Clean spaces within each match
    cleaned = [''.join(m.split()) for m in matches]

# Optional: remove duplicates
    unique = sorted(set(cleaned))
    alert_me.send_email(os.getenv("EMAIL_"),os.getenv("APP_PASS"),os.getenv("CLIENT"),"ALL THE COUPON CODES",F"{unique}")
    #amazon_bot.init(unique)
    print("Temporary directory cleaned up after execution.")
    cleaner.removeAll()

    
