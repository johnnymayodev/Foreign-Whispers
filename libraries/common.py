import os
import math

class Common_Variables:
    M1 = "Milestone1"
    M2 = "Milestone2"
    M3 = "Milestone3"
    M4 = "Milestone4"
    M5 = "Milestone5"
    M6 = "Milestone6"
    SUBTITLES = "subtitles.txt"
    VIDEO = "video.mp4"
    TRANSLATED_VIDEO = 'translated_video.mp4'
    AUDIO = "audio.mp3"
    AUDIO_WAV = "audio.wav"
    GENERATED_PICKLE_FILE = "generated_subtitles.pickle"
    TRANSLATED_PICKLE_FILE = "translated_subtitles.pickle"
    AUDIO_FOLDER = "audio"
    MULTI_LANG_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"
    MAX_ATTEMPTS = 9 # What ever this number is plus 1 is the actual max attempts
    FILE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # gets the script directory to Milestones
    BG_COLOR = (0,0,0)
    FONT_SIZE = 24
    SUBTITLES_POS = ('center', 'bottom')

    POPULAR_LANGUAGES = {
    "polish": "pl",
    "german": "de",
    "english": "en",
    "spanish": "es",
    "french": "fr",
    "italian": "it",
    "portuguese": "pt",
    "russian": "ru",
    # "chinese": "zh"
}
    
class Common_Methods:
    @staticmethod
    def create_directory(directory):
        try:
            os.mkdir(directory)
        except FileExistsError:
            pass

    @staticmethod
    def dict_to_string(dict):
        string = ""
        for key, value in dict.items():
            if key == "text":
                string += f"{value}\n"  # string += f"{key}: {value}\n"
        return string
    
    @staticmethod
    def subtitles_to_dict(input_dict):
        important_keys = [
            "start",
            "end",
            "text",
        ]
        """
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
        """
        new_dict = {}
        for segment in input_dict["segments"]:
            new_dict[segment["id"]] = {
                key: math.ceil(segment[key]) if key in ["start", "end"] else segment[key]
                for key in important_keys
            }
        return new_dict