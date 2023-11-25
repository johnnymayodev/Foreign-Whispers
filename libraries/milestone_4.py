import os
import time
import pickle

from pydub import AudioSegment 
from TTS.api import TTS

def main(video_id, language):
    start = time.time()

    if not os.path.exists(f"Milestone2/{video_id}/audio.mp3"):
        return ["Failed", time.time() - start, "Original audio file does not exist"]

    if not os.path.exists(f"Milestone2/{video_id}/audio.wav"):
        # convert the mp3 to wav
        try: 
            mp3 = AudioSegment.from_mp3(f"Milestone2/{video_id}/audio.mp3")
        except Exception as e:
            return ["Failed", time.time() - start, f"Failed to load mp3: {e}"]
        
        try:
            mp3.export(f"Milestone2/{video_id}/audio.wav", format="wav")
        except Exception as e:
            return ["Failed", time.time() - start, f"Failed to convert mp3 to wav: {e}"]

    save_dir = f"Milestone4/{video_id}/{language}/audio/"

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

    # if save_dir is empty, then we need to generate the audio
    if len(os.listdir(save_dir)) == 0:
        pass
    else:
        print("Audio already generated.")
        return ["Success", time.time() - start, save_dir]

    try:
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
    except Exception as e:
        return ["Failed", time.time() - start, f"Failed to load TTS model: {e}"]

    # this is already a dictionary
    translations = pickle.load(open(f"Milestone3/{video_id}/{language}/translated_subtitles.pickle", "rb"))

    translations_as_list = []

    for i in range(len(translations)):
        translations_as_list.append(translations[i]['text']) # list

    counter = 0
    for sentence in translations_as_list:
        counter += 1
        save_file_path = f"{save_dir}/sentence_{counter}.wav"
        try:
            tts.tts_to_file(text=sentence, file_path=save_file_path, speaker_wav=f"Milestone2/{video_id}/audio.wav", language=language)
        except Exception as e:
            return ["Failed", time.time() - start, f"Failed to generate audio for sentence {counter}: {e}"]

    # try:
    #     tts.tts_to_file(text=translations_as_str, file_path="output.wav", speaker_wav=f"Milestone2/{video_id}/audio.wav", language=language)
    # except Exception as e:
    #     return ["Failed", time.time() - start, f"Failed to generate audio: {e}"]

    return ["Success", time.time() - start, save_dir]
