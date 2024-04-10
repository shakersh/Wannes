import os
import nltk

from app.util.Dump import Dump


class Resources:
    modules = []

    def load(self):
        # essential entity models downloads
        nltk.downloader.download('maxent_ne_chunker')
        nltk.downloader.download('words')
        nltk.downloader.download('treebank')
        nltk.downloader.download('maxent_treebank_pos_tagger')
        nltk.downloader.download('punkt')
        nltk.download('averaged_perceptron_tagger')

        dir_list = os.listdir('app/core/Services')

        for file in dir_list:
            if not file.endswith('.py'):
                continue
            service_name = file.replace('.py', '')
            module_name = "app.core.Services." + service_name
            __import__(module_name)
            self.modules.append([module_name, service_name])
