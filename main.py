import libraries.milestone_1 as m1
import libraries.milestone_2 as m2
import libraries.milestone_3 as m3

video_url = "https://www.youtube.com/watch?v=bNKdlnoAqIs"  # Bill Gates: The 2021 60 Minutes interview
language_to_translate_to = "el"  # Greek

if not __name__ == "__main__":
    print("This file should be run as a script.")
    exit(1)

if __name__ == "__main__":
    print("\nEnter a YouTube video URL (leave blank for a pre-set URL):")
    if input() != "":
        video_url = input()

    print("Enter a language to translate to (leave blank for a pre-set language):")
    if input() != "":
        language_to_translate_to = input()

    print("\nStarting...")

    # Milestone 1
    m1_response = m1.main(video_url)
    if m1_response[0] == "Failed":
        print(f"Failed to download video {m1_response[1][0]}\n{m1_response[1][1]}")
        exit(1)
    video_id = m1_response[1][0]

    # Milestone 2
    m2_response = m2.main(video_id)
    if m2_response[0] == "Failed":
        print(f"Failed to generate subtitles for video {video_id}\n{m2_response[1]}")
        exit(1)
    subtitles_en = m2_response[1]

    # Milestone 3
    m3_response = m3.main(video_id, subtitles_en, language_to_translate_to)
    if m3_response[0] == "Failed":
        print(f"Failed to translate subtitles for video {video_id}\n{m3_response[1]}")
        exit(1)

    print("Done.")
    exit(0)
