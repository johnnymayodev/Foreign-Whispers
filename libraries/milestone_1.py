import os
from pytube import YouTube, Playlist
from youtube_transcript_api import YouTubeTranscriptApi

MAX_VIDEOS = 10


def main(app):
    print("milestone 1")
    PLAYLIST = Playlist(app.config["YT_URL"])
    playlist_id = app.config["YT_URL"].split("list=")[1].split("&")[0]

    # create a directory for the playlist
    try:
        os.mkdir(f"playlist_{playlist_id}")
    except FileExistsError:
        pass

    # loop through the playlist and make a list of the videos
    videos = []
    for video in PLAYLIST.videos:
        if video.age_restricted:
            print(f"skipping {video.video_id} because it is age restricted")
            continue

        if video.length > 1200:
            print(f"skipping {video.video_id} because it is longer than 20 minutes")
            continue

        if not YouTubeTranscriptApi.list_transcripts(video.video_id).find_transcript(
            ["en"]
        ):
            print(f"skipping {video.video_id} because it has no english subtitles")
            continue

        print(f"adding {video.title}")
        videos.append(video)

        if len(videos) >= MAX_VIDEOS:
            break

    print(f"found {len(videos)} videos")

    # loop through the videos and make subdirectories for each video (the name of the subdirectory is the video id)
    for video in videos:
        try:
            os.mkdir(f"playlist_{playlist_id}/{video.video_id}")
            os.mkdir(f"playlist_{playlist_id}/{video.video_id}/video")
            os.mkdir(f"playlist_{playlist_id}/{video.video_id}/subtitles")
        except FileExistsError:
            pass

    print("subdirectories created")

    # loop through the videos and download the video and subtitles
    for video in videos:
        # check if the video has already been downloaded
        if os.path.isfile(f"playlist_{playlist_id}/{video.video_id}/video/video.mp4"):
            continue

        # download the video
        video.streams.get_highest_resolution().download(
            output_path=f"playlist_{playlist_id}/{video.video_id}/video"
        )

        # check if the subtitles have already been downloaded
        if os.path.isfile(
            f"playlist_{playlist_id}/{video.video_id}/subtitles/subtitles.txt"
        ):
            continue

        # download the subtitles
        transcript = YouTubeTranscriptApi.get_transcript(
            video.video_id, languages=["en"]
        )
        with open(
            f"playlist_{playlist_id}/{video.video_id}/subtitles/subtitles.txt", "w"
        ) as f:
            for line in transcript:
                f.write(line["text"] + "\n")

    print("videos and subtitles downloaded")
    return {"Milestone 1": "Done"}
