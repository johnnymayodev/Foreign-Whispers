import time

import libraries.milestone_1 as m1
import libraries.milestone_2 as m2
import libraries.milestone_3 as m3

video_url = "https://www.youtube.com/watch?v=bNKdlnoAqIs"  # Bill Gates: The 2021 60 Minutes interview
language_to_translate_to = "el"  # Greek

popular_languages = {
    "greek": "el",
    "hindi": "hi",
    "german": "de",
    "english": "en",
    "spanish": "es",
    "french": "fr",
    "italian": "it",
    "japanese": "ja",
    "korean": "ko",
    "portuguese": "pt",
    "russian": "ru",
    "chinese": "zh"
}

if not __name__ == "__main__":
    print("This file should be run as a script.")
    exit(1)

if __name__ == "__main__":
    print("\nEnter a YouTube video URL (leave blank for a pre-set URL):")
    new_video_url = input()
    if new_video_url != "":
        video_url = new_video_url

    print("Enter a language to translate to (leave blank for a pre-set language):")
    new_language_to_translate_to = input().lower()
    
    if new_language_to_translate_to != "":
        
        if len(new_language_to_translate_to) != 2:
            language_to_translate_to = new_language_to_translate_to
            if new_language_to_translate_to not in popular_languages.keys():
                print("Language not found. Please try again.")
                exit(1)
            else:
                language_to_translate_to = popular_languages[new_language_to_translate_to]
        else:
            language_to_translate_to = new_language_to_translate_to

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
