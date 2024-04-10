from datetime import datetime
from io import BytesIO
import pygame
import wikipediaapi
from gtts import gTTS
from app.core import Constants
from app.core.Emoji import Emoji
from app.util.Dump import Dump
from app.util.Scrapper import Scrapper
from app.util.Setting import Setting
from app.util.Translate import Translate
from app.core.Services.Service import Service
import openai
from nltk.chat.util import Chat as NormalChat, reflections
from resources.chatting.Chatting import pairs


class Chat(Service):

    def handle(self, request):
        # First, need to check if we have a saved answer
        # If not then go with below flow:
        chat = NormalChat(pairs, reflections)
        reply = chat.respond(request)

        # We have to check if this user is able to use AI Model or not
        # If not, go with normal speach
        # Will assume now it's okay to use Normal Chat
        # reply = self.gpt(request)

        Dump.dd(reply)
        if reply is None:
            # reply = self.normal_chat(request)
            reply = self.stream_gpt(request)
            if reply:
                Dump.dd('gpt: ' + reply)
            return

        if reply is None:
            reply = Translate.__('no_response_found')

        Constants.audio.speak(reply)

    @staticmethod
    def gpt(request):
        # openai.api_key = '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'
        openai.api_key = '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'

        try:
            Dump.dd("sending request")
            reply = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    # {
                    #     "role": "system",
                    #     "content": "انت شخص سعودي وتتكلم بالعامية\nتم صناعتك من خلال شركة بدائع التقنية للتجارة الالكترونية\nهدفك تسلية الناس ومساعدتهم في بعض الاعمال البسيطة\nانت شخص سعودي ومسلم ومحب للناس\n\nاسم المالك لك هو شاكر شاهين\nعمره 32 سنة، ما بيحب الكلام كتير، ويحب الاجابات المختصرة\nبيحب التقنية، كرة القدم\nوبيحب التواصل باللغة العامية"
                    # },
                    {
                        "role": "system",
                        "content": "انت شخص سعودي وتتكلم بالعامية\nتم صناعتك من خلال شركة بدائع التقنية للتجارة الالكترونية\nهدفك تسلية الناس ومساعدتهم في بعض الاعمال البسيطة\nانت شخص سعودي ومسلم ومحب للناس، بتحب الاجابات المختصرة وقليل الكلام"
                    },
                    {
                        "role": "user",
                        "content": request,
                    },
                    # {
                    #     "role": "assistant",
                    #     "content": "الهلال، نادي كبير جِدًّا في المملكة العَرَبِيّة السُّعُودِيّة وواحِدٌ مِنْ أشهَر الأندية في الشرق الأوسط. تأسَّسَ فِي عام 1957 ومَقَرُّهُ في الرِّيَاض. ألوان الهلال هي الزُّرْقَاء، وملعبهُم الرَّئِيسِيّ هو مَلْعَب الملك فهد الدولي، وهو مِنْ أكبَر المَلاعِب في العالَم. النادي حَقَّقَ العديد مِنْ البطولات المحليَّة والقاريَّة، وهو مَشهُورٌ بِجُمُوحِ جَماهيرِهِ الولائيَّة والحَمَّاسيَّة. فاز بِبَطُولَة دوري أبطال آسيا مَرَّات عدَّة، ولَدَيهُ سِجلٌ حافل بِالإنجازات. إن الهلال لَيس فَقَط ناديًا لكُرَة القَدَم، بَل هو رُمُزٌّ للنَّجَاح والشُّغَف في عالَم الرِّيَاضَة ويحمِل مَكَانَةً خاصَّةً في قُلُوب مَشجِّعَيهِ."
                    # }
                ],
                temperature=0.3,
                max_tokens=300,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                , stream=True)
            Dump.dd("requests received")

            # reply = chat.choices[0].message.content
        except Exception as e:
            Dump.dd(e)
            reply = Translate.__('error_connection_ai')

        return reply

    def stream_gpt(self, request):
        reply = ""
        sounds_list = []
        pygame.mixer.pre_init(30000, -16, 2, 2048)
        pygame.mixer.init()
        sound = pygame.mixer.music

        for response in self.gpt(request):
            content = response.choices[0].delta.get('content', '')

            if not content:
                continue

            if any(map(content.__contains__, ['.', ',', '،'])):
                Dump.dd(reply)
                mp3_fp = BytesIO()
                obj = gTTS(text=reply, lang='ar')
                obj.write_to_fp(mp3_fp)
                mp3_fp.seek(0)
                sounds_list.append(mp3_fp)

                Dump.dd('start playing at: ' + datetime.now().strftime("%H:%M:%S.%f")[:-3])

                if not sound.get_busy():
                    Emoji.change_emoji('speak')
                    sound.load(sounds_list.pop(0))
                    sound.play()
                    Dump.dd('Still loading, then play the second part')

                reply = ""
                continue

            reply += content

        Constants.audio.play_back(sound, sounds_list)

        pygame.mixer.quit()

    def normal_chat(self, request):
        reply = None
        try:
            key = 'ويكيبيديا' if Setting.config('lang') == 'ar' else 'wikipedia'
            result = Scrapper.google_search(request + ' ' + key)
            if result:
                reply = self.wikipedia(result)

        except:
            return None

        return reply

    @staticmethod
    def wikipedia(result):
        reply = None
        # remove wikipedia from the result first
        result = result.replace(' - ويكيبيديا', '')
        result = result.replace(' - Wikipedia', '')

        # now search in wikipedia about the result
        wiki_wiki = wikipediaapi.Wikipedia(
            'User-Agent: CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org) generic-library/0.0',
            'ar')
        page_py = wiki_wiki.page(result)
        Dump.dd(page_py, page_py.exists(), page_py.summary)

        if page_py.exists():
            reply = page_py.summary

        return reply

    @staticmethod
    def post_action():
        Setting.update('has_welcome', False)

    @staticmethod
    def is_background_job():
        return False
