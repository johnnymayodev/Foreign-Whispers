# from translate import Translator
import os
import argostranslate.package
import argostranslate.translate


def main(video_id, subtitles_en, language):
    from_code = "en"

    translation = ""
    translations = []

    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == language,
            available_packages,
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())

    try:
        os.mkdir("Milestone3")
        os.mkdir(f"Milestone3/{video_id}")
        os.mkdir(f"Milestone3/{video_id}/{language}/")
    except FileExistsError:
        pass

    if os.path.exists(f"Milestone3/{video_id}/{language}/translated_subtitles.txt"):
        print(f"Video {video_id} already has translated subtitles")
        translations.append(
            open(
                f"Milestone3/{video_id}/{language}/translated_subtitles.txt", "r"
            ).read()
        )
        return ["Success", translations]

    for i in range(len(subtitles_en)):
        save_path = f"Milestone3/{video_id}/{language}/"

        try:
            translator = argostranslate.translate
        except Exception as e:
            return ["Failed", f"Error creating translator: {e}"]

        try:
            translation = translator.translate(subtitles_en[i], from_code, language)
        except Exception as e:
            return ["Failed", f"Error translating subtitles: {e}"]

        try:
            with open(save_path + "translated_subtitles.txt", "w") as f:
                f.write(translation)
        except Exception as e:
            return ["Failed", f"Error saving subtitles to file: {e}"]

        translations.append(translation)
    return ["Success", translations]
