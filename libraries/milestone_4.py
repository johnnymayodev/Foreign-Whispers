import os
import time
import pickle

from libraries.common import Common_Variables as cv
from libraries.common import Common_Methods as cm
from pydub import AudioSegment 
from TTS.api import TTS

def main(video_id, language):
    start = time.time()
    audio_mp3_path = os.path.join(cv.M2, video_id, cv.AUDIO)
    audio_wav_path = os.path.join(cv.M2, video_id, cv.AUDIO_WAV)

    if not os.path.exists(audio_mp3_path):
        return ["Failed", time.time() - start, "Original audio file does not exist"]

    if not os.path.exists(audio_wav_path):
        # convert the mp3 to wav
        try: 
            mp3 = AudioSegment.from_mp3(audio_mp3_path)
        except Exception as e:
            return ["Failed", time.time() - start, f"Failed to load mp3: {e}"]
        
        try:
            mp3.export(audio_wav_path, format="wav")
        except Exception as e:
            return ["Failed", time.time() - start, f"Failed to convert mp3 to wav: {e}"]
        
    cm.create_directory(cv.M4)
    video_id_path = os.path.join(cv.M4, video_id)
    cm.create_directory(video_id_path)
    language_path = os.path.join(video_id_path, language)
    cm.create_directory(language_path)
    audio_path = os.path.join(language_path, cv.AUDIO_FOLDER)
    cm.create_directory(audio_path)

    save_dir = os.path.join(cv.M4, video_id, language, cv.AUDIO_FOLDER)

    # if save_dir is empty, then we need to generate the audio
    if len(os.listdir(save_dir)) == 0:
        pass
    else:
        print("Audio already generated.")
        return ["Success", time.time() - start, save_dir]

    try:
        tts = TTS(cv.MULTI_LANG_MODEL, gpu=False)
    except Exception as e:
        return ["Failed", time.time() - start, f"Failed to load TTS model: {e}"]

    # this is already a dictionary
    translated_path = os.path.join(cv.M3, video_id, language, cv.TRANSLATED_PICKLE_FILE)
    with open(translated_path, 'rb') as f:
        translations = pickle.load(f)

    translations_as_list = []

    for i in range(len(translations)):
        translations_as_list.append(translations[i]['text']) # list

    for counter, sentence in enumerate(translations_as_list):
        save_file_path = os.path.join(save_dir, f"sentence_{counter}.wav")
        try:
            tts.tts_to_file(text=sentence, file_path=save_file_path, speaker_wav=audio_wav_path, language=language, speed=2.0)
        except Exception as e:
            return ["Failed", time.time() - start, f"Failed to generate audio for sentence {counter}: {e}"]

    return ["Success", time.time() - start, save_dir]
