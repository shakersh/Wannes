import json
import random

import requests


class Translate:
    @staticmethod
    def __(key, placeholders=None, lang='ar'):
        with open('trans/' + lang + '.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        translation = data.get(key, data.get('default_msg'))
        if isinstance(translation, list):
            translation = random.choice(translation)
        if placeholders is not None:
            for key, value in placeholders.items():
                translation = translation.replace(':' + key, str(value))

        return translation

    @staticmethod
    def google_translate(text, lang='ar'):
        api_key = "AIzaSyD-7uWTjTodZba7ky7mgfSgnVxAX_opoh8"
        translate_url = "https://translation.googleapis.com/language/translate/v2"

        params = {
            "q": text,
            "target": lang,
            "key": api_key
        }

        response = requests.post(translate_url, data=params)
        data = response.json()

        if "data" in data and "translations" in data["data"]:
            return data["data"]["translations"][0]["translatedText"]
