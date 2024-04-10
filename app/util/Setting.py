from config.setting import setting


class Setting:
    @staticmethod
    def config(key):
        return setting.get(key)

    @staticmethod
    def update(key, new_value):
        setting.update({key: new_value})
