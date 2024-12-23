import os
import re
import random
import shutil
import subprocess
from urllib.parse import urlparse, parse_qs


from yt_dlp import YoutubeDL
import glob


def get_youtube_video_id(url):
    try:
        # Parse the URL
        parsed_url = urlparse(url)
        # Extract query parameters
        query_params = parse_qs(parsed_url.query)
        # Return the video ID
        return query_params.get("v", [None])[0]
    except Exception as e:
        print(f"Error extracting video ID: {e}")
        return None


def sanitize_filename(name):

    # Remove invalid characters and replace spaces with underscores
    sanitized = re.sub(r'[<>:"/\\|?*]', '', name).strip().replace(' ', '_')
    # Remove single and double quotes
    sanitized = sanitized.replace("'", '').replace('"', '')
    return sanitized


def get_video_info(video_url):
    ydl_opts = {
        'skip_download': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
    return info

def download_video(video_url, download_dir):
    try:
        os.makedirs(download_dir, exist_ok=True)

        # Get video info first
        info = get_video_info(video_url)
        video_title = info.get('title')  # Extract the title

        # Sanitize the video title
        sanitized_title = sanitize_filename(video_title)
        output_path = os.path.join(download_dir, f"{sanitized_title}.%(ext)s")

        # Download the video with the sanitized title
        ydl_opts = {
            'outtmpl': output_path,  # Use the sanitized title for the output file
            'format': 'bv',  # Download video with 480p height
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return sanitized_title
    except Exception as e:
        print(e)