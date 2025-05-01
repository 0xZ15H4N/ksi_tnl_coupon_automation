import os
import requests
import subprocess
import json
from time import sleep
from tqdm import tqdm
from dotenv import load_dotenv
from google.cloud import storage
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures import ThreadPoolExecutor, as_completed


load_dotenv()

# === CONFIG ===
KEY_PATH = os.getenv("AUTH_KEY")
VIDEO_PATH =  os.getenv("VIDEO_PATH") #'/home/theanonymouse/ksi_tnl/temp_youtube_download/video.mp4.webm'
CHUNK_DURATION = 60  # seconds
CHUNK_DIR = 'videoChunks'
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")


# Create reusable credentials and authed session

# === AUTH SETUP ===
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
credentials = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
authed_session = AuthorizedSession(credentials)

# === Ensure chunk directory exists ===
os.makedirs(CHUNK_DIR, exist_ok=True)

    # === Video Splitting ===
def split_video():
    print("[+] Splitting video into chunks...")
    cmd = [
        'ffmpeg',
        "-hide_banner",
        "-loglevel", "error",
        '-i', VIDEO_PATH,
        '-c', 'copy',
        '-map', '0',
        '-f', 'segment',
        '-segment_time', str(CHUNK_DURATION),
        os.path.join(CHUNK_DIR, 'chunk_%02d.mp4')
    ]
    subprocess.run(cmd, check=True)

# === Upload to Google Cloud Storage ===
def upload_to_gcs(local_file, bucket_name):
    print(f"[+] Uploading {local_file} to GCS...")
    client = storage.Client(credentials=credentials, project=credentials.project_id)
    bucket = client.bucket(bucket_name)
    blob_name = os.path.basename(local_file)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_file)
    return f"gs://{bucket_name}/{blob_name}"

# === Call Video Intelligence API ===
def analyze_video(uri):
    payload = {
        "inputUri": uri,
        "features": ["TEXT_DETECTION"]
    }
    response = authed_session.post(
        "https://videointelligence.googleapis.com/v1/videos:annotate",
        headers={'Content-Type': 'application/json'},
        data=json.dumps(payload)
    )

    if response.status_code != 200:
        print(f"[❌] API error: {response.status_code} - {response.text}")
        return None

    data = response.json()
    return data.get("name")

# === Wait for Operation Completion ===
def wait_for_operation(operation_name):
    if not operation_name:
        return None

    print(f"[~] Waiting for operation {operation_name} to complete...")
    while True:
        response = authed_session.get(
            f"https://videointelligence.googleapis.com/v1/operations/{operation_name}"
        )
        try:
            result = response.json()
        except json.JSONDecodeError:
            print("[❌] Invalid JSON response from API.")
            return None

        if result.get("done"):
            return result
        sleep(10)

# === Parse Duration String ===
def parse_duration(dur_str):
    if dur_str.endswith('s'):
        return float(dur_str[:-1])
    return 0.0

# === Parse Annotation Results ===
def parse_result(result, chunk_index):
    annotations = result['response']['annotationResults'][0].get('textAnnotations', [])
    offset = chunk_index * CHUNK_DURATION
    parsed = []

    for ann in annotations:
        desc = ann['text']
        for segment in ann['segments']:
            start = segment['segment']['startTimeOffset']
            start_sec = offset + parse_duration(start)
            parsed.append((round(start_sec, 2), desc))
    return parsed

# === Optional: Clean GCS after results ===
def clean_gcs_bucket(bucket_name, prefix='chunk_'):
    print("[🧹] Cleaning up GCS bucket...")
    client = storage.Client(credentials=credentials, project=credentials.project_id)
    bucket = client.bucket(bucket_name)
    for blob in bucket.list_blobs():
        if blob.name.startswith(prefix):
            print(f"  ⤷ Deleting {blob.name}")
            blob.delete()
    print("[✅] GCS cleanup complete.")

def process_chunk(idx, file):
    local_path = os.path.join(CHUNK_DIR, file)
    try:
        gcs_uri = upload_to_gcs(local_path, GCS_BUCKET_NAME)
        op_name = analyze_video(gcs_uri)
        result = wait_for_operation(op_name)
        if result:
            return parse_result(result, idx)
        else:
            print(f"[!] Skipping chunk {file} due to API error.")
            return []
    except Exception as e:
        print(f"[!] Error processing chunk {file}: {e}")
        return []

def main():
    split_video()
    chunk_files = sorted(os.listdir(CHUNK_DIR))
    all_results = []

    # Use max_workers=4 or more depending on your bandwidth and system
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(process_chunk, idx, file): (idx, file)
            for idx, file in enumerate(chunk_files)
        }

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing chunks"):
            result = future.result()
            if result:
                all_results.extend(result)

    # Write results
    print("\n[✅] Final Detected Coupon Codes and Timestamps:")
    with open("results.txt", "w") as f:
        for time_sec, text in sorted(all_results):
            f.write(f"[{time_sec:.2f}s] {text}\n")




