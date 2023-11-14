import os
import time

from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi


def main(video_url):
    start = time.time()

    try:
        os.mkdir("Milestone1/")
    except FileExistsError:
        pass

    try:
        os.mkdir(f"Milestone1/{YouTube(video_url).video_id}/")
    except FileExistsError:
        pass

    # if the url is a video, download it
    if "watch?v=" in video_url:
        youtube = YouTube(video_url)
    # if the url is a playlist, download it
    else:
        return ["Failed", time.time()-start , f"Error: {video_url} is a playlist. Please enter a video url."]

    if os.path.exists(f"Milestone1/{youtube.video_id}/video.mp4"):
        print(f"Video {youtube.video_id} already downloaded")
        return ["Success", time.time()-start , youtube.video_id]

    # if the video is age restricted, skip it
    if youtube.age_restricted:
        return ["Failed", time.time()-start , f"Error: {youtube.video_id} is age restricted."]

    # if the video doesn't have subtitles, skip it
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            youtube.video_id, languages=["en"]
        )
    except:
        return ["Failed", time.time()-start , f"Error: {youtube.video_id} doesn't have subtitles."]

    # if the video doesn't have english subtitles, skip it
    if not transcript:
        return ["Failed", time.time()-start , f"Error: {youtube.video_id} doesn't have english subtitles."]

    # download the video
    try:
        print(f"Downloading video {youtube.video_id}...")
        youtube.streams.filter(file_extension="mp4").first().download(
            output_path=f"Milestone1/{youtube.video_id}/", filename="video.mp4"
        )
    except Exception as e:
        return ["Failed", time.time()-start , f"Error: Failed to download video {youtube.video_id}.\n{e}"]

    # download the subtitles
    with open(f"Milestone1/{youtube.video_id}/subtitles.txt", "w") as f:
        f.write(str(transcript))

    return ["Success", time.time() - start, youtube.video_id]
