import os
import json
import time
import shutil
import pickle
import pytube

from flask import Flask, render_template

from libraries.common import Common_Variables as cv
import libraries.milestone_1 as m1
import libraries.milestone_2 as m2
import libraries.milestone_3 as m3
import libraries.milestone_4 as m4
import libraries.milestone_5 as m5

MILESTONE1_PATH = "milestone1/"
MILESTONE2_PATH = "milestone2/"
MILESTONE3_PATH = "milestone3/"
MILESTONE4_PATH = "milestone4/"
MILESTONE5_PATH = "milestone5/"

PORT = 37000

video_id = None

app = Flask(__name__, template_folder="web", static_folder="web")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/init", methods=["GET"])
def init():
    try:
        get_videos()
        return "OK"
    except Exception as e:
        return str(e)


@app.route("/select_video/<video_index>/<language>", methods=["POST"])
def select_video(video_index, language):
    try:
        get_subtitles(video_index, language)
        return "OK"
    except Exception as e:
        return str(e)


@app.route("/link_entered/<video_id>/<language_to_translate_to>", methods=["POST"])
def link_entered(video_id, language_to_translate_to):
    try:
        start = time.time()
        print("\nStarting...")

        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # Milestone 1
        video_id = milestone_1(video_url=video_url)

        # Milestone 2
        subtitles_en = milestone_2(video_id=video_id)

        # Milestone 3
        translated_subtitles = milestone_3(
            video_id=video_id,
            subtitles_en=subtitles_en,
            language_to_translate_to=language_to_translate_to,
        )

        # Milestone 4
        voice_over_path = milestone_4(video_id, language_to_translate_to)

        # Milestone 5
        translated_video = milestone_5(
            video_id=video_id,
            subtitles=translated_subtitles,
            voice_over_path=voice_over_path,
            language=language_to_translate_to,
        )

        print(f"Done.\nTotal time elapsed: {round((time.time() - start), 4)} seconds")

        return "OK"

    except Exception as e:
        return str(e)


def main():
    app.run(debug=True, port=PORT)


def get_videos():
    video_ids = os.listdir(MILESTONE1_PATH)
    video_titles = []
    for video_id in video_ids:
        title = pytube.YouTube(f"https://www.youtube.com/watch?v={video_id}").title
        video_titles.append(title)

    # CHECK IF ALL MILESTONES WERE COMPLETED FOR EACH VIDEO (for now assume yes)

    if not os.path.exists("web/static"):
        os.makedirs("web/static")

    if os.path.exists("web/static/videos.json"):
        os.remove("web/static/videos.json")

    languages = []

    for i in range(len(video_ids)):
        video_id = video_ids[i]
        video_title = video_titles[i]
        video_languages = os.listdir(f"{MILESTONE3_PATH}{video_id}")
        for language in video_languages:
            if language not in languages:
                languages.append(language)

    dict = {}

    for i in range(len(video_ids)):
        video_id = video_ids[i]
        video_title = video_titles[i]
        languages = os.listdir(f"{MILESTONE3_PATH}{video_id}")
        dict[str(i)] = {"id": video_id, "title": video_title, "languages": languages}

    json.dump(dict, open("web/static/videos.json", "w"))


def get_subtitles(video_index, language):
    video_id = os.listdir(MILESTONE2_PATH)[int(video_index)]

    if not os.path.exists("web/static"):
        os.makedirs("web/static")

    if os.path.exists("web/static/subtitles.json"):
        os.remove("web/static/subtitles.json")

    POPULAR_LANGUAGES = {
        "polish": "pl",
        "german": "de",
        "english": "en",
        "spanish": "es",
        "french": "fr",
        "italian": "it",
        "portuguese": "pt",
        "russian": "ru",
        # "chinese": "zh",
    }

    if language.lower() in POPULAR_LANGUAGES:
        language = POPULAR_LANGUAGES[language.lower()]

    get_subtitles = {}

    with open(
        f"{MILESTONE2_PATH}{video_id}/generated_subtitles.pickle", "rb"
    ) as generated_subtitles_file:
        generated_subtitles = pickle.load(generated_subtitles_file)

    with open(
        f"{MILESTONE3_PATH}{video_id}/{language}/translated_subtitles.pickle", "rb"
    ) as translated_subtitles_file:
        translated_subtitles = pickle.load(translated_subtitles_file)

    for i in range(len(generated_subtitles)):
        subtitle = generated_subtitles[i]
        translated_subtitle = translated_subtitles[i]
        get_subtitles[str(i)] = {
            "timestamp": subtitle["start"],
            "text": subtitle["text"],
            "translated_text": translated_subtitle["text"],
        }

    json.dump(get_subtitles, open("web/static/subtitles.json", "w"))

    if not os.path.exists(f"web/static/{language}"):
        os.makedirs(f"web/static/{language}")

    video_title = pytube.YouTube(f"https://www.youtube.com/watch?v={video_id}").title

    if not os.path.exists(f"web/static/{language}/{video_title}.mp4"):
        shutil.copy2(
            f"{MILESTONE5_PATH}{video_id}/{language}/translated_video.mp4",
            f"web/static/{language}/{video_title}.mp4",
        )


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


def milestone_1(video_url, attempts=0):
    m1_response = m1.main(video_url)
    print(
        f"Attempt {attempts+1}: Milestone 1 completed in {round(m1_response[1], 4)} seconds\n"
    )

    if attempts >= cv.MAX_ATTEMPTS or m1_response[0] == "Error":
        print(m1_response[2])
        exit(1)

    if m1_response[0] == "Failed":
        print(f"Failed retrying: {m1_response[2]}")
        shutil.rmtree(cv.M1)
        attempts += 1
        return milestone_1(video_url, attempts)

    return m1_response[2]


def milestone_2(video_id, attempts=0):
    m2_response = m2.main(video_id)
    print(
        f"Attempt {attempts+1}: Milestone 2 completed in {round(m2_response[1], 4)} seconds\n"
    )

    if attempts >= cv.MAX_ATTEMPTS:
        print(m2_response[2])
        exit(1)

    if m2_response[0] == "Failed":
        print(f"Failed retrying: {m2_response[2]}")
        shutil.rmtree(cv.M2)
        attempts += 1
        return milestone_2(video_id, attempts)

    return m2_response[2]


def milestone_3(video_id, subtitles_en, language_to_translate_to, attempts=0):
    m3_response = m3.main(video_id, subtitles_en, language_to_translate_to)
    print(
        f"Attempt {attempts+1}: Milestone 3 completed in {round(m3_response[1], 4)} seconds\n"
    )

    if attempts >= cv.MAX_ATTEMPTS:
        print(m3_response[2])
        exit(1)

    if m3_response[0] == "Failed":
        print(f"Failed retrying: {m3_response[2]}")
        shutil.rmtree(cv.M3)
        attempts += 1
        return milestone_3(video_id, subtitles_en, language_to_translate_to, attempts)

    return m3_response[2]


def milestone_4(video_id, language_to_translate_to, attempts=0):
    m4_response = m4.main(video_id, language_to_translate_to)
    print(
        f"Attempt {attempts+1}: Milestone 4 completed in {round(m4_response[1], 4)} seconds\n"
    )

    if attempts >= cv.MAX_ATTEMPTS:
        print(m4_response[2])
        exit(1)

    if m4_response[0] == "Failed":
        print(f"Failed retrying: {m4_response[2]}")
        shutil.rmtree(cv.M4)
        attempts += 1
        return milestone_4(video_id, language_to_translate_to, attempts)

    return m4_response[2]


def milestone_5(video_id, subtitles, voice_over_path, language, attempts=0):
    m5_response = m5.main(video_id, subtitles, voice_over_path, language)
    print(
        f"Attempt {attempts+1}: Milestone 5 completed in {round(m5_response[1], 4)} seconds\n"
    )

    if attempts >= cv.MAX_ATTEMPTS:
        print(m5_response[2])
        exit(1)

    if m5_response[0] == "Failed":
        print(f"Failed retrying: {m5_response[2]}")
        shutil.rmtree(cv.M5)
        attempts += 1
        return milestone_5(video_id, subtitles, voice_over_path, language, attempts)

    return m5_response[2]


if __name__ == "__main__":
    main()
