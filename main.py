import os
import time

import libraries.milestone_1 as m1
import libraries.milestone_2 as m2
import libraries.milestone_3 as m3

video_url = "https://www.youtube.com/watch?v=bNKdlnoAqIs"  # Bill Gates: The 2021 60 Minutes interview
language_to_translate_to = "el"  # Greek

if not __name__ == "__main__":
    print("This file should be run as a script.")
    exit(1)

if __name__ == "__main__":
    print("Are you running on a Mac? (y/n)")
    if input() == "y":
        ffmpeg_path = "/opt/homebrew/bin/ffmpeg"
        os.environ["PATH"] += f":{os.path.dirname(ffmpeg_path)}"
        os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path

    print("\nEnter a YouTube video URL (leave blank for a pre-set URL):")
    if input() != "":
        video_url = input()

    print("Enter a language to translate to (leave blank for a pre-set language):")
    if input() != "":
        language_to_translate_to = input()

    start = time.time()
    print("\nStarting...")

    # Milestone 1
    m1_response = m1.main(video_url)
    print(f"Milestone 1 completed in {round(m1_response[1], 4)} seconds\n")

    if m1_response[0] == "Failed":
        print(m1_response[2])
        exit(1)

    video_id = m1_response[2]

    # Milestone 2
    m2_response = m2.main(video_id)
    print(f"Milestone 2 completed in {round(m2_response[1], 4)} seconds\n")

    if m2_response[0] == "Failed":
        print(m2_response[2])
        exit(1)

    subtitles_en = m2_response[2]

    # Milestone 3
    m3_response = m3.main(video_id, subtitles_en, language_to_translate_to)
    print(f"Milestone 3 completed in {round(m3_response[1], 4)} seconds\n")

    if m3_response[0] == "Failed":
        print(m3_response[2])
        exit(1)

    translated_subtitles = m3_response[2]

    print(f"Done.\nTotal time elapsed: {round((time.time() - start), 4)} seconds")
    exit(0)
