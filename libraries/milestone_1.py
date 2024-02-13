import os
import time
from libraries.common import Common_Methods as cm
from libraries.common import Common_Variables as cv

from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi


def main(video_url):
    start = time.time()

    cm.create_directory(cv.M1)

    # if the url is a video, download it
    if "watch?v=" in video_url:
        youtube = YouTube(video_url)
        video_id = youtube.video_id
        video_id_path = os.path.join(cv.M1, video_id)
        subtitle_path = os.path.join(video_id_path, cv.SUBTITLES)
        cm.create_directory(video_id_path)

        save_path = os.path.join(video_id_path, cv.VIDEO)
    # if the url is a playlist, ask to be sent a video
    else:
        return [
            "Error",
            time.time() - start,
            f"Error: {video_url} is a playlist. Please enter a video url.",
        ]

    if os.path.exists(save_path):
        print(f"Video {video_id} already downloaded")
        return ["Success", time.time() - start, video_id]

    # if the video is age restricted, skip it
    if youtube.age_restricted:
        return [
            "Error",
            time.time() - start,
            f"Error: {video_id} is age restricted.",
        ]

    # if the video doesn't have subtitles, skip it
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=[cv.POPULAR_LANGUAGES["english"]]
        )
    except:
        return [
            "Error",
            time.time() - start,
            f"Error: {video_id} doesn't have subtitles.",
        ]

    # if the video doesn't have english subtitles, skip it
    if not transcript:
        return [
            "Error",
            time.time() - start,
            f"Error: {video_id} doesn't have english subtitles.",
        ]

    # download the video
    try:
        print(f"Downloading video {video_id}...")
        youtube.streams.filter(file_extension="mp4").first().download(
            output_path=video_id_path, filename=cv.VIDEO
        )
    except Exception as e:
        return [
            "Failed",
            time.time() - start,
            f"Error: Failed to download video {video_id}.\n{e}",
        ]

    # download the subtitles
    with open(subtitle_path, "w") as f:
        f.write(str(transcript))

    return ["Success", time.time() - start, video_id]