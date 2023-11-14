import os
import math
import time
import pickle

import pandas as pd

""" This code may be needed to run on MacOS
ffmpeg_path = "/opt/homebrew/bin/ffmpeg"
os.environ["PATH"] += f":{os.path.dirname(ffmpeg_path)}"
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path
""" 

import whisper
import moviepy.editor as mp


def main(video_id):
    start = time.time()

    try:
        os.mkdir("Milestone2/")
    except FileExistsError:
        pass

    try:
        os.mkdir(f"Milestone2/{video_id}")
    except FileExistsError:
        pass

    save_path = f"Milestone2/{video_id}/"
    video_path = f"Milestone1/{video_id}/"

    # check if the video already has generated subtitles
    if os.path.exists(save_path + "generated_subtitles.pickle"):
        print(f"Video {video_id} already has generated subtitles")
        with open(save_path + "generated_subtitles.pickle", "rb") as f:
            # generated_subtitles = pickle.load(f)
            generated_subtitles = pd.read_pickle(f)
        return ["Success", time.time() - start, generated_subtitles]

    if os.path.exists(save_path + "audio.mp3"):
        print(f"Video {video_id} already has audio")
    else:
        # get the audio from the video
        try:
            audio = mp.VideoFileClip(video_path + "video.mp4").audio
        except Exception as e:
            return ["Failed", time.time() - start, f"Error: Failed to get audio from video: {e}."]

        # save the audio to a file
        try:
            audio.write_audiofile(save_path + "audio.mp3")
        except Exception as e:
            return ["Failed", time.time() - start, f"Error: Failed to save audio to file: {e}."]

    # load model
    try:
        model = whisper.load_model("base")
    except Exception as e:
        return ["Failed", time.time() - start, f"Error: Failed to load model: {e}."]

    # generate subtitles from the audio
    try:
        generated_subtitles = model.transcribe(save_path + "audio.mp3")
    except Exception as e:
        return ["Failed", time.time() - start, f"Error: Failed to generate subtitles: {e}."]

    generated_subtitles = dict_to_dict(generated_subtitles)

    # save the generated subtitles to a file
    try:
        with open(f"Milestone2/{video_id}/generated_subtitles.pickle", "wb") as f:
            pickle.dump(generated_subtitles, f)
    except Exception as e:
        return ["Failed", time.time() - start, f"Error: Failed to save generated subtitles to file: {e}."] 

    return ["Success", time.time() - start, generated_subtitles]


def dict_to_string(dict):
    string = ""
    for key, value in dict.items():
        if key == "text":
            string += f"{value}\n"  # string += f"{key}: {value}\n"
    return string

def dict_to_dict(dict):
    important_keys = [
        "start",
        "end",
        "text",
    ]

    '''
    new_dict = {
        "0": { # segment id
            "start": 0.0,
            "end": 2.0,
            "text": "Hello"
        },
        "1": {
            "start": 2.0,
            "end": 4.0,
            "text": "World"
        }
    }
    '''

    new_dict = {}

    for dict in dict['segments']:
        new_dict[dict['id']] = {key: math.ceil(dict[key]) if key in ["start", "end"] else dict[key] for key in important_keys}

    return new_dict
