import requests
import bs4
from app.util.Dump import Dump
from youtubesearchpython import VideosSearch


class Scrapper:
    @staticmethod
    def google_search(request):
        url = 'https://google.com/search?q=' + request
        request_result = requests.get(url)
        soup = bs4.BeautifulSoup(request_result.text, "html.parser")

        filtered = soup.findAll('h3')
        result = None
        if len(filtered):
            result = filtered[0]
            Dump.dd(result, result.get_text())
            result = result.get_text()

        return result

    @staticmethod
    def youtube_search(request):
        search = VideosSearch(request, limit=1)
        results = search.result()
        if len(results['result']) > 0:
            video_id = results['result'][0]['id']
            return video_id
