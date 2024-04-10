from app.util.Dump import Dump
from app.core.Services.Chat import Chat
from app.util.Resources import Resources
import sys


class Classification:
    @staticmethod
    def classify(request):
        # should check the request here and return type
        # if nothing, then return Chat
        try:
            for item in Resources.modules:
                modul = sys.modules[item[0]]  # item[0] is module name
                service = getattr(modul, item[1])  # item[1] is class name
                if any(map(request.__contains__, service().keywords)):
                    Dump.dd(service)
                    return service()

        except Exception as e:
            Dump.dd(e)
            Dump.dd(Chat)
            return Chat()

        Dump.dd(Chat)
        return Chat()
