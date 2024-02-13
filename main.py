import time
import shutil

from libraries.common import Common_Variables as cv
import libraries.milestone_1 as m1
import libraries.milestone_2 as m2
import libraries.milestone_3 as m3
import libraries.milestone_4 as m4
import libraries.milestone_5 as m5

def main():
    video_url = get_youtube_video_url(default = "https://www.youtube.com/watch?v=bNKdlnoAqIs")
    language_to_translate_to = get_language(default = cv.POPULAR_LANGUAGES["polish"])
    start = time.time()
    print("\nStarting...")

    # Milestone 1
    video_id = milestone_1(video_url = video_url)

    # Milestone 2
    subtitles_en = milestone_2(video_id = video_id)

    # Milestone 3
    translated_subtitles = milestone_3(video_id = video_id, subtitles_en = subtitles_en, language_to_translate_to = language_to_translate_to)

    # Milestone 4
    voice_over_path = milestone_4(video_id = video_id, language_to_translate_to = language_to_translate_to)

    #Milestone 5
    translated_video = milestone_5(video_id = video_id, subtitles = translated_subtitles, voice_over_path = voice_over_path, language = language_to_translate_to)

    print(f"Done.\nTotal time elapsed: {round((time.time() - start), 4)} seconds")
    exit(0)

def get_youtube_video_url(default):
    print("\nEnter a YouTube video URL (leave blank for a pre-set URL):")
    new_video_url = input()
    if new_video_url != "":

        if "https://www.youtube.com/watch?v=" not in new_video_url:
            print("\nInvalid URL. Please try again.")
            print("Example: https://www.youtube.com/watch?v=bNKdlnoAqIs")
            return get_youtube_video_url(default)
        return new_video_url
    return default

def get_language(default):
    print("Enter a language to translate to (leave blank for a pre-set language):")
    new_language_to_translate_to = input().lower()
    
    if new_language_to_translate_to != "":
        if len(new_language_to_translate_to) != 2:
            if new_language_to_translate_to not in cv.POPULAR_LANGUAGES.keys():
                print("\nLanguage not found. Please try again.\n")
                return get_language(default)
            else:
                return cv.POPULAR_LANGUAGES[new_language_to_translate_to]
        else:
            return new_language_to_translate_to
    return default

def milestone_1(video_url, attempts = 0):
    m1_response = m1.main(video_url)
    print(f"Attempt {attempts+1}: Milestone 1 completed in {round(m1_response[1], 4)} seconds\n")

    if attempts >= cv.MAX_ATTEMPTS or m1_response[0] == "Error":
        print(m1_response[2])
        exit(1)

    if m1_response[0] == "Failed":
        print(f"Failed retrying: {m1_response[2]}")
        shutil.rmtree(cv.M1)
        attempts += 1
        return milestone_1(video_url, attempts)

    return m1_response[2]

def milestone_2(video_id, attempts = 0):
    m2_response = m2.main(video_id)
    print(f"Attempt {attempts+1}: Milestone 2 completed in {round(m2_response[1], 4)} seconds\n")

    if attempts >= cv.MAX_ATTEMPTS:
        print(m2_response[2])
        exit(1)

    if m2_response[0] == "Failed":
        print(f"Failed retrying: {m2_response[2]}")
        shutil.rmtree(cv.M2)
        attempts += 1
        return milestone_2(video_id, attempts)

    return m2_response[2]

def milestone_3(video_id, subtitles_en, language_to_translate_to, attempts = 0):
    m3_response = m3.main(video_id, subtitles_en, language_to_translate_to)
    print(f"Attempt {attempts+1}: Milestone 3 completed in {round(m3_response[1], 4)} seconds\n")

    if attempts >= cv.MAX_ATTEMPTS:
        print(m3_response[2])
        exit(1)

    if m3_response[0] == "Failed":
        print(f"Failed retrying: {m3_response[2]}")
        shutil.rmtree(cv.M3)
        attempts += 1
        return milestone_3(video_id, subtitles_en, language_to_translate_to, attempts)

    return m3_response[2]

def milestone_4(video_id, language_to_translate_to, attempts = 0):
    m4_response = m4.main(video_id, language_to_translate_to)
    print(f"Attempt {attempts+1}: Milestone 4 completed in {round(m4_response[1], 4)} seconds\n")

    if attempts >= cv.MAX_ATTEMPTS:
        print(m4_response[2])
        exit(1)

    if m4_response[0] == "Failed":
        print(f"Failed retrying: {m4_response[2]}")
        shutil.rmtree(cv.M4)
        attempts += 1
        return milestone_4(video_id, language_to_translate_to, attempts)

    return m4_response[2]

def milestone_5(video_id, subtitles, voice_over_path, language, attempts = 0):
    m5_response = m5.main(video_id, subtitles, voice_over_path, language)
    print(f"Attempt {attempts+1}: Milestone 5 completed in {round(m5_response[1], 4)} seconds\n")

    if attempts >= cv.MAX_ATTEMPTS:
        print(m5_response[2])
        exit(1)

    if m5_response[0] == "Failed":
        print(f"Failed retrying: {m5_response[2]}")
        shutil.rmtree(cv.M5)
        attempts += 1
        return milestone_5(video_id, subtitles, voice_over_path, language, attempts)

    return m5_response[2]    


if not __name__ == "__main__":
    print("This file should be run as a script.")
    exit(1)

if __name__ == "__main__":
    main()