from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips, CompositeVideoClip, TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.audio.AudioClip import CompositeAudioClip
from libraries.common import Common_Variables as cv
from libraries.common import Common_Methods as cm
import json
import time
import os

def main(video_id, subtitles, _voice_over_path, language):
    start = time.time()
    path_to_video = os.path.join(cv.M1, video_id, cv.VIDEO)
    voice_over_dir = _voice_over_path
    translated_video_path = os.path.join(cv.M5, video_id, language, cv.TRANSLATED_VIDEO)
    translated_audio_path = os.path.join(cv.M5, video_id, language, cv.AUDIO_WAV)
    
    # check if M5 has already been completed
    if os.path.exists(translated_video_path):
        print("Video already translated.")
        return success(time.time() - start, translated_video_path)

    cm.create_directory(cv.M5)
    cm.create_directory(os.path.join(cv.M5, video_id))
    cm.create_directory(os.path.join(cv.M5, video_id, language))

    # Combines audio clips together
    try:
        audio_clip = combine_audio_clips(voice_over_dir)
        audio_clip.write_audiofile(translated_audio_path, codec='pcm_s16le', bitrate='16k', fps=44100)
    except Exception as e:
        return failed(time.time()-start, f"Failed to combine audios: {e}")

    # Creates a VideoFileClip with new audio and generates the translation stub
    try:
        translated_video_with_subtitles = create_video_audio_subtitles_clips(path_to_video, translated_audio_path, subtitles)
    except Exception as e:
        return failed(time.time()-start, f"Failed to create clips: {e}")

    # Writes the new video file down to the translated_video_path
    try:
        translated_video_with_subtitles.write_videofile(translated_video_path)
    except Exception as e:
        return failed(time.time()-start, f"Failed to write translated video file: {e}")

    return success(time.time() - start, translated_video_path)

# Creates the VideoFileClip and SubtitleClip
def create_video_audio_subtitles_clips(video_path, audio_path, subtitles_data):
    audio_clip = AudioFileClip(audio_path)

    video_clip = VideoFileClip(filename=video_path, audio=False)
    
    subtitle_gen = subtitle_data_generator(subtitles_data)

    subtitles = []
    for subtitle in subtitle_gen:
        start_time, end_time, text = subtitle
        duration = end_time - start_time
        
        text_clip = TextClip(text, fontsize=16, color='white', font='Arial', bg_color='black')
        text_clip = text_clip.set_pos('bottom').set_duration(duration).set_start(start_time)
        
        subtitles.append(text_clip)
        
    result = CompositeVideoClip([video_clip.set_audio(audio_clip), *subtitles])

    return result

# Combines .wav files together
def combine_audio_clips(audio_dir):
    audio_clips = []
    
    audio_files = os.listdir(audio_dir)
    
    for i in range(len(audio_files)):
        for j in range(len(audio_files)-1):
            if int(audio_files[j].split("_")[1].split(".")[0]) > int(audio_files[j+1].split("_")[1].split(".")[0]):
                audio_files[j], audio_files[j+1] = audio_files[j+1], audio_files[j]
    
    for filename in audio_files:
        if filename.endswith(".wav"):
            audio_path = os.path.join(audio_dir, filename)
            audio_clip = AudioFileClip(audio_path)
            audio_clips.append(audio_clip)
    return concatenate_audioclips(audio_clips)

# Creates a tuple of the translated subtitles data
def subtitle_data_generator(subtitles_data):
    for subtitle in subtitles_data:
        yield subtitles_data[subtitle]['start'], subtitles_data[subtitle]['end'], subtitles_data[subtitle]['text']

# Failed Process
def failed(_time, message):
    return ["Failed", _time, message]

def success(_time, message):
    return ["Success", _time, message]