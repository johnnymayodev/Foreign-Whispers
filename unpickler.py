import pickle
import os

if __name__ == "__main__":
    print(
        "What would you like to unpickle?\n[1] Generated subtitles\n[2] Translated subtitles"
    )
    choice = input()
    if choice == "1":
        print("What video ID would you like to unpickle?")
        count = 0
        for video_id in os.listdir("Milestone2/"):
            count += 1
            print(f"[{count}] {video_id}")

        choice = input()
        if int(choice) > len(os.listdir("Milestone2/")):
            print("Invalid choice")
            exit(1)

        video_id = os.listdir("Milestone2/")[int(choice) - 1]

        with open(
            f"Milestone2/{video_id}/generated_subtitles.pickle", "rb"
        ) as generated_subtitles_file:
            generated_subtitles = pickle.load(generated_subtitles_file)

        print(generated_subtitles)

    elif choice == "2":
        print("What video ID would you like to unpickle?")
        count = 0
        for video_id in os.listdir("Milestone3/"):
            count += 1
            print(f"[{count}] {video_id}")

        choice = input()
        if int(choice) > len(os.listdir("Milestone3/")):
            print("Invalid choice")
            exit(1)

        video_id = os.listdir("Milestone3/")[int(choice) - 1]

        print("What language would you like to unpickle?")
        count = 0
        for language in os.listdir(f"Milestone3/{video_id}/"):
            count += 1
            print(f"[{count}] {language}")

        choice = input()
        if int(choice) > len(os.listdir(f"Milestone3/{video_id}/")):
            print("Invalid choice")
            exit(1)

        language = os.listdir(f"Milestone3/{video_id}/")[int(choice) - 1]

        with open(
            f"Milestone3/{video_id}/{language}/translated_subtitles.pickle", "rb"
        ) as translated_subtitles_file:
            translated_subtitles = pickle.load(translated_subtitles_file)

        print(translated_subtitles)

    else:
        print("Invalid choice")
        exit(1)

    exit(0)
