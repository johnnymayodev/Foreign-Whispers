import os
import time
import pickle
import argostranslate.package
import argostranslate.translate
from libraries.common import Common_Methods as cm
from libraries.common import Common_Variables as cv
from copy import deepcopy


def main(video_id, subtitles_in_english, language):
    start = time.time()

    from_code = cv.POPULAR_LANGUAGES["english"]

    translations = deepcopy(subtitles_in_english)

    cm.create_directory(cv.M3)

    video_id_path = os.path.join(cv.M3, video_id)
    cm.create_directory(video_id_path)

    language_path = os.path.join(video_id_path, language)
    cm.create_directory(language_path)

    pickle_path = os.path.join(language_path, cv.TRANSLATED_PICKLE_FILE)

    if os.path.exists(pickle_path):
        print(f"Video {video_id} already has translated subtitles")
        with open(pickle_path, "rb") as f:
            translations = pickle.load(f)
        return ["Success", time.time() - start, translations]

    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == language,
            available_packages,
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())

    # make the translator
    try:
        translator = argostranslate.translate
    except Exception as e:
        return [
            "Failed",
            time.time() - start,
            f"Error: Failed to make translator: {e}.",
        ]

    print(f"Translating subtitles to {language}...")
    for subtitle in translations:
        for key, value in translations[subtitle].items():
            if key == "text":
                try:
                    translations[subtitle]["text"] = translator.translate(
                        value, from_code, language
                    )
                except Exception as e:
                    return [
                        "Failed",
                        time.time() - start,
                        f"Error: Failed to translate: {e}.",
                    ]

    # save the translated subtitles to a file
    try:
        with open(pickle_path, "wb") as f:
            pickle.dump(translations, f)
    except Exception as e:
        return [
            "Failed",
            time.time() - start,
            f"Error: Failed to save translated subtitles to file: {e}.",
        ]

    return ["Success", time.time() - start, translations]
