import subprocess
import re
import argparse
import amazon_bot
import cleaner
import ocr
import video_dectection

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

    with open("./results.txt") as f:
        a=f.read()

    coupons = re.findall(r"[A-Z0-9]{4}-[A-Z0-9]{6}-[A-Z0-9]{4}",a)
    amazon_bot.init(coupons)
    print("Temporary directory cleaned up after execution.")
    cleaner.removeAll()

    
