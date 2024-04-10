from time import sleep
from app.core.Emoji import Emoji
from app.core.Player import Player
from app.core.Services.Service import Service
from app.util.Dump import Dump
from app.util.Helper import Helper
from app.util.Scrapper import Scrapper
from app.util.Translate import Translate
from app.core import Constants
import pafy


class PlayVideo(Service):
    keywords = ['شغل اغنية', 'شغل فيديو', 'افتح اغنية', 'افتح فيديو', 'اطربني', 'فيديو', 'سمعني', 'اغنية', 'اغنيه',
                'افتح اغنيه', 'شغل اغنيه']

    def handle(self, request):
        if not Helper.is_raspberry():
            Dump.dd('Platform not supported')
            Constants.audio.speak(Translate.__('not_supported'))
            return

        request = Helper.get_raw_request(request, self.keywords)
        Dump.dd(request)
        video_id = Scrapper.youtube_search(request)
        Dump.dd(video_id)

        if video_id:
            video_url = "https://www.youtube.com/watch?v=" + video_id

            video = pafy.new(video_url)
            best = video.getbest(preftype="mp4")

            player = Player(best.url)
            player.play_video()
            Emoji.change_emoji('listen')
            sleep(5)
            while player.is_playing():
                sleep(1)

            player.release()

        else:
            Translate.__('video_not_found')

    @staticmethod
    def is_background_job():
        return False
