import os
from yt_dlp import YoutubeDL
import ffmpeg

def download_youtube_video(url):
    """Download a YouTube video in the best available quality using yt-dlp.

    The function saves the file into a local "videos" folder and returns the final
    filepath or None if an error occurred.
    """

    # Ensure output directory exists
    os.makedirs("videos", exist_ok=True)

    ydl_opts = {
        "format": "bestvideo*+bestaudio/best",  # separate video+audio then merge
        "merge_output_format": "mp4",            # final container
        "outtmpl": os.path.join("videos", "%(title)s.%(ext)s"),
        "quiet": False,                           # show progress
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            output_file = ydl.prepare_filename(info)

        print(f"Downloaded: {info.get('title')} to 'videos' folder")
        print(f"File path: {output_file}")
        return output_file

    except Exception as e:
        print(f"An error occurred while downloading: {e}")
        print("Assurez-vous que yt-dlp est à jour :  pip install -U yt-dlp")
        return None

if __name__ == "__main__":
    youtube_url = input("Enter YouTube video URL: ")
    download_youtube_video(youtube_url)
