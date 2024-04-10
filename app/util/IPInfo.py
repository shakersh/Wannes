import requests


class IPInfo:

    @staticmethod
    def city():
        response = requests.get('https://ipinfo.io')
        data = response.json()
        city = data.get('city')
        if city:
            return city
