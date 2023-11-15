import pickle
import os

MILESTONE2_PATH = "Milestone2/"
MILESTONE3_PATH = "Milestone3/"
GENERATED_SUBTITLE_FILE_NAME = "generated_subtitles.pickle"
TRANSLATED_SUBTITLE_FILE_NAME = "translated_subtitles.pickle"


if __name__ == "__main__":
    print(
        "What would you like to unpickle?\n[1] Generated subtitles\n[2] Translated subtitles"
    )
    choice = input()
    if choice == "1":
        print("What video ID would you like to unpickle?")
        count = 0
        for video_id in os.listdir(MILESTONE2_PATH):
            count += 1
            print(f"[{count}] {video_id}")

        choice = input()
        if int(choice) > len(os.listdir(MILESTONE2_PATH)):
            print("Invalid choice")
            exit(1)

        video_id = os.listdir(MILESTONE2_PATH)[int(choice) - 1]

        with open(
            f"{MILESTONE2_PATH}{video_id}/{GENERATED_SUBTITLE_FILE_NAME}", "rb"
        ) as generated_subtitles_file:
            generated_subtitles = pickle.load(generated_subtitles_file)

        print(generated_subtitles)

    elif choice == "2":
        print("What video ID would you like to unpickle?")
        count = 0
        for video_id in os.listdir(MILESTONE3_PATH):
            count += 1
            print(f"[{count}] {video_id}")

        choice = input()
        if int(choice) > len(os.listdir(MILESTONE3_PATH)):
            print("Invalid choice")
            exit(1)

        video_id = os.listdir(MILESTONE3_PATH)[int(choice) - 1]

        print("What language would you like to unpickle?")
        count = 0
        for language in os.listdir(f"{MILESTONE3_PATH}{video_id}/"):
            count += 1
            print(f"[{count}] {language}")

        choice = input()
        if int(choice) > len(os.listdir(f"{MILESTONE3_PATH}{video_id}/")):
            print("Invalid choice")
            exit(1)

        language = os.listdir(f"{MILESTONE3_PATH}{video_id}/")[int(choice) - 1]

        with open(
            f"{MILESTONE3_PATH}{video_id}/{language}/{TRANSLATED_SUBTITLE_FILE_NAME}",
            "rb",
        ) as translated_subtitles_file:
            translated_subtitles = pickle.load(translated_subtitles_file)

        print(translated_subtitles)

    else:
        print("Invalid choice")
        exit(1)

    exit(0)
