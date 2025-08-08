import os

from Components.YoutubeDownloader import download_youtube_video
from Components.Edit import extractAudio, crop_video
from Components.Transcription import transcribeAudio
from Components.LanguageTasks import GetHighlight
from Components.FaceCrop import crop_to_vertical, combine_videos

url = input("Enter YouTube video URL: ")
Vid= download_youtube_video(url)
if Vid:
    Vid = Vid.replace(".webm", ".mp4")
    print(f"Downloaded video and audio files successfully! at {Vid}")

    Audio = extractAudio(Vid)
    if Audio:

        transcriptions = transcribeAudio(Audio)
        if len(transcriptions) > 0:
            TransText = ""
            for text, start, end in transcriptions:
                TransText += (f"{start} - {end}: {text}\n")

            segments = GetHighlight(TransText)  # list of (start, end)
            if len(segments) > 0:
                print(f"Segments trouvés : {segments}")
                for idx, (start, stop) in enumerate(segments, start=1):
                    print(f"Processing segment {idx}: {start}-{stop}s")
                    base = f"{idx}"
                    out_raw = f"Out_{base}.mp4"
                    out_crop = f"croped_{base}.mp4"
                    final_file = f"Final_{base}.mp4"

                    crop_video(Vid, out_raw, start, stop)
                    crop_to_vertical(out_raw, out_crop)
                    combine_videos(out_raw, out_crop, final_file)
            else:
                print("Error in getting highlight")
        else:
            print("No transcriptions found")
    else:
        print("No audio file found")
else:
    print("Unable to Download the video")