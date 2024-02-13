import os
import time
import pickle

from libraries.common import Common_Methods as cm
from libraries.common import Common_Variables as cv

import whisper
import moviepy.editor as mp


def main(video_id):
    start = time.time()

    cm.create_directory(cv.M2)

    m2_video_path = os.path.join(cv.M2, video_id)
    cm.create_directory(m2_video_path)

    save_path = os.path.join(m2_video_path, cv.AUDIO)
    pickle_path = os.path.join(m2_video_path, cv.GENERATED_PICKLE_FILE)
    video_path = os.path.join(cv.M1, video_id, cv.VIDEO)

    # check if the video already has generated subtitles
    if os.path.exists(pickle_path):
        print(f"Video {video_id} already has generated subtitles")
        with open(pickle_path, "rb") as f:
            generated_subtitles = pickle.load(f)
        return ["Success", time.time() - start, generated_subtitles]

    if os.path.exists(save_path):
        print(f"Video {video_id} already has audio")
    else:
        # get the audio from the video
        try:
            audio = mp.VideoFileClip(video_path).audio
        except Exception as e:
            return [
                "Failed",
                time.time() - start,
                f"Error: Failed to get audio from video: {e}.",
            ]

        # save the audio to a file
        try:
            audio.write_audiofile(save_path)
        except Exception as e:
            return [
                "Failed",
                time.time() - start,
                f"Error: Failed to save audio to file: {e}.",
            ]

    # load model
    print("Loading whisper...")
    try:
        model = whisper.load_model("base")
    except Exception as e:
        return ["Failed", time.time() - start, f"Error: Failed to load model: {e}."]

    # generate subtitles from the audio
    print(f"Generating subtitles for video {video_id}...")
    try:
        print("save_path:", os.path.join(cv.FILE_PATH, save_path))
        generated_subtitles = model.transcribe(os.path.join(cv.FILE_PATH, save_path))
    except Exception as e:
        return [
            "Failed",
            time.time() - start,
            f"Error: Failed to generate subtitles: {e}.",
        ]

    try:
        generated_subtitles = cm.subtitles_to_dict(generated_subtitles)
    except Exception as e:
        return [
            "Failed",
            time.time() - start,
            f"Error: Failed to clean generated subtitles: {e}.",
        ]

    # save the generated subtitles to a file
    try:
        with open(pickle_path, "wb") as f:
            pickle.dump(generated_subtitles, f)
    except Exception as e:
        return [
            "Failed",
            time.time() - start,
            f"Error: Failed to save generated subtitles to file: {e}.",
        ]

    return ["Success", time.time() - start, generated_subtitles]