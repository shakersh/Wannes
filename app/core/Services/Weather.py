from app.core import Constants
from app.core.Emoji import Emoji
from app.core.Services.Service import Service
import requests
from app.util.Dump import Dump
from app.util.IPInfo import IPInfo
from app.util.Setting import Setting
from app.util.Translate import Translate
import locationtagger


class Weather(Service):
    keywords = ['درجة الحرارة', 'حالة الطقس', 'حاله الطقس', 'درجه الحراره']

    def handle(self, request):
        lang = Setting.config('lang')

        if lang != 'en':
            request = Translate.google_translate(request, 'en')

        Dump.dd(request)
        # extracting entities.
        place_entity = locationtagger.find_locations(text=request)
        Dump.dd(place_entity.countries, place_entity.cities, place_entity.regions)
        if place_entity.countries:
            city = place_entity.countries[0]
        elif place_entity.regions:
            city = place_entity.regions[0]
        elif place_entity.cities:
            city = place_entity.cities[0]
        else:
            city = IPInfo.city()

        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        api_key = "b4c4c473183d57da250b411769243a6c"
        complete_url = f"{base_url}q={city}&appid={api_key}&lang={lang}&units=metric"

        response = requests.get(complete_url)
        data = response.json()

        if data["cod"] != "404":
            main_data = data["main"]
            weather_data = data["weather"][0]
            description = weather_data["description"]
            temp = int(main_data["temp"])
            wind = int(data["wind"]["speed"])

            # change emoji based on weather
            if temp < 12:
                feeling = 'cold'

            elif temp < 28:
                feeling = 'relax'

            else:
                feeling = 'hot'

            Emoji.change_emoji(feeling)

            Constants.audio.speak(
                Translate.__('weather_summary', {'city': city, 'description': description, 'temp': temp, 'wind': wind}),
                False)
        else:
            Constants.audio.speak(Translate.__('weather_not_found'))

    @staticmethod
    def post_action():
        Setting.update('has_welcome', False)
