import os
import time
import pickle

import argostranslate.package
import argostranslate.translate


def main(video_id, subtitles_in_english, language):
    start = time.time()

    from_code = "en"

    # translation = ""
    translations = subtitles_in_english

    try:
        os.mkdir("Milestone3/")
    except FileExistsError:
        pass
    
    try:
        os.mkdir(f"Milestone3/{video_id}/")
    except FileExistsError:
        pass

    try:
        os.mkdir(f"Milestone3/{video_id}/{language}/")
    except FileExistsError:
        pass

    if os.path.exists(f"Milestone3/{video_id}/{language}/translated_subtitles.pickle"):
        print(f"Video {video_id} already has translated subtitles")
        with open(f"Milestone3/{video_id}/{language}/translated_subtitles.pickle", "rb") as f:
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
        return ["Failed", time.time() - start, f"Error: Failed to make translator: {e}."]

    print(f"Translating subtitles to {language}...")
    for subtitle in translations:
        for key, value in translations[subtitle].items():
            if key == "text":
                try:
                    translations.update({subtitle: {
                        "start": translations[subtitle]["start"],
                        "end": translations[subtitle]["end"],
                        "text": translator.translate(value, from_code, language)
                    }})
                except Exception as e:
                    return ["Failed", time.time() - start, f"Error: Failed to translate: {e}."]                

    # save the translated subtitles to a file
    try:
        with open(f"Milestone3/{video_id}/{language}/translated_subtitles.pickle", "wb") as f:
            pickle.dump(translations, f)
    except Exception as e:
        return ["Failed", time.time() - start, f"Error: Failed to save translated subtitles to file: {e}."]
    
    return ["Success", time.time() - start, translations]
