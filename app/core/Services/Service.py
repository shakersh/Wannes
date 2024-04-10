from app.util.Dump import Dump


class Service:
    keywords = []

    def handle(self, request):
        Dump.dd('Not allowed to run a generic service')

    @staticmethod
    def post_action():
        pass

    @staticmethod
    def pre_action():
        pass

    @staticmethod
    def is_background_job():
        return False
