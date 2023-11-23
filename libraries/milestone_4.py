import os
import time
import pickle


def main(video_id, language):
    start = time.time()

    save_path = f"Milestone4/{video_id}/{language}/audio/voice_over.mp3"

    try:
        os.mkdir("Milestone4/")
    except FileExistsError:
        pass

    try:
        os.mkdir(f"Milestone4/{video_id}/")
    except FileExistsError:
        pass

    try:
        os.mkdir(f"Milestone4/{video_id}/{language}/")
    except FileExistsError:
        pass

    try:
        os.mkdir(f"Milestone4/{video_id}/{language}/audio/")
    except FileExistsError:
        pass

    if os.path.exists(save_path):
        print("Voice over already exists, skipping...")
        return

    try:
        pass 
        # Pick TTS model
    except Exception as e:
        return ["Failed", time.time() - start, f"Failed to load TTS model: {e}"]

    # this is already a dictionary
    translations = pickle.load(open(f"Milestone3/{video_id}/{language}/translated_subtitles.pickle", "rb"))

    # not sure if a list or str is better for this part
    # ---- LIST ----
    translations_as_list = []

    for i in range(len(translations)):
        translations_as_list.append(translations[i]['text'])

    # ---- STRING ----
    translations_as_str = ""

    for i in range(len(translations)):
        translations_as_str += translations[i]['text'] + " "

    try:
        pass
        # use the TTS model to generate audio
    except Exception as e:
        return ["Failed", time.time() - start, f"Failed to generate audio: {e}"]

    try:
        pass
        # save the audio file 
        # save_path -> (Milestone4/{video_id}/{language}/audio/voice_over.mp3)
    except Exception as e:
        return ["Failed", time.time() - start, f"Failed to save audio: {e}"]

    return ["Success", time.time() - start, save_path]
