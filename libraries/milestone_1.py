import os
from pytube import YouTube, Playlist
from youtube_transcript_api import YouTubeTranscriptApi


def main(video_url):
    try:
        os.mkdir("Milestone1/")
        os.mkdir(f"Milestone1/{YouTube(video_url).video_id}/")
    except FileExistsError:
        pass

    # if the url is a video, download it
    if "watch?v=" in video_url:
        youtube = YouTube(video_url)
    # if the url is a playlist, download it
    else:
        print("This program is not designed to work with playlists.")

    if os.path.exists(f"Milestone1/{youtube.video_id}/video.mp4"):
        print(f"Video {youtube.video_id} already downloaded")
        return ["Success", [youtube.video_id]]

    # if the video is age restricted, skip it
    if youtube.age_restricted:
        print(f"Video {youtube.video_id} is age restricted")
        return ["Failed", [youtube.video_id]]

    # if the video doesn't have subtitles, skip it
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            youtube.video_id, languages=["en"]
        )
    except:
        print(f"Video {youtube.video_id} doesn't have subtitles")
        return ["Failed", [youtube.video_id]]

    # if the video doesn't have english subtitles, skip it
    if not transcript:
        print(f"Video {youtube.video_id} doesn't have english subtitles")
        return ["Failed", [youtube.video_id]]

    # download the video
    try:
        youtube.streams.filter(file_extension="mp4").first().download(
            output_path=f"Milestone1/{youtube.video_id}/", filename="video.mp4"
        )
    except:
        return ["Failed", [youtube.video_id]]

    # download the subtitles
    with open(f"Milestone1/{youtube.video_id}/subtitles.txt", "w") as f:
        f.write(str(transcript))

    return ["Success", [youtube.video_id]]
