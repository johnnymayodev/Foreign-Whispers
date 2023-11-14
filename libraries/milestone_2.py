import os

""" This code may be needed to run on MacOS
ffmpeg_path = "/opt/homebrew/bin/ffmpeg"
os.environ["PATH"] += f":{os.path.dirname(ffmpeg_path)}"
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path
""" 

import whisper
import moviepy.editor as mp


def main(video_id):
    try:
        os.mkdir("Milestone2")
        os.mkdir(f"Milestone2/{video_id}")
    except FileExistsError:
        pass

    all_subtitles = []

    save_path = f"Milestone2/{video_id}/"
    video_path = f"Milestone1/{video_id}/"

    # if the video already has generated subtitles, skip it
    if os.path.exists(save_path + "generated_subtitles.txt"):
        print(f"Video {video_id} already has generated subtitles")
        all_subtitles.append(open(save_path + "generated_subtitles.txt", "r").read())
        return ["Success", all_subtitles]

    if os.path.exists(save_path + "audio.mp3"):
        print(f"Video {video_id} already has audio")
    else:
        # get the audio from the video
        try:
            audio = mp.VideoFileClip(video_path + "video.mp4").audio
        except Exception as e:
            return ["Failed", f"Error creating audio from video: {e}"]

        # save the audio to a file
        try:
            audio.write_audiofile(save_path + "audio.mp3")
        except Exception as e:
            return ["Failed", f"Error saving audio to file: {e}"]

    # load model
    try:
        model = whisper.load_model("base")
    except Exception as e:
        return ["Failed", f"Error loading model: {e}"]

    # generate subtitles from the audio
    try:
        generated_subtitles = model.transcribe(save_path + "audio.mp3")
    except Exception as e:
        return ["Failed", f"Error creating subtitles from audio: {e}"]

    # save the subtitles to a file
    try:
        with open(save_path + "generated_subtitles.txt", "w") as f:
            f.write(dict_to_string(generated_subtitles))
    except Exception as e:
        return ["Failed", f"Error saving subtitles to file: {e}"]

    all_subtitles.append(dict_to_string(generated_subtitles))

    return ["Success", all_subtitles]


def dict_to_string(dict):
    string = ""
    for key, value in dict.items():
        if key == "text":
            string += f"{value}\n"  # string += f"{key}: {value}\n"
    return string
