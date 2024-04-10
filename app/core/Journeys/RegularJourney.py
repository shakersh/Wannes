from app.core import Constants
from app.util.Setting import Setting
from app.util.Translate import Translate
from app.core.Classification import Classification
from app.core.Mode import Mode


class RegularJourney:
    @staticmethod
    def welcome():
        Constants.audio.speak(Translate.__('welcome_msg'))

    @staticmethod
    def classify_request(request):

        # First check if there is a response or not, if not, then sleep
        # Need to determine if robot should sleep forever (till say "ونيس" again)
        if request is None:
            Mode.sleepy()
            return

        # We should classify the response type first
        # this should return a service obj
        return Classification.classify(request)

    @staticmethod
    def handle_request(service, request, feeling):
        Constants.feeling = feeling
        service.handle(request)

    @staticmethod
    def sleep_listening():
        # listen while sleeping to wake up
        request = Constants.audio.listen(with_emoji=False)
        # If user call me "ونيس", then have to wake up
        if request and (any(map(request.__contains__, [Setting.config('name'), 'وليد', 'ولا']))):
            Mode.wakeup()
            Constants.audio.speak(Translate.__('force_wakeup_msg'))
