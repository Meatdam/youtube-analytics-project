import os
import json
from googleapiclient.discovery import build

API_KEY = os.getenv('API_KEY')


class Channel:
    """Класс для ютуб-канала"""
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, channel_id) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.title = self.title_youtube()
        self.id = self.id_channel()
        self.description = self.descriptions()
        self.url = self.url_channel()
        self.subscriber = self.subscriber_count()
        self.video_count = self.video_counts()
        self.view_count = self.view_counts()

    @property
    def channel_id(self):
        """getter __channel_id"""
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, user_input):
        """Запрещает назначять новое название __channel_id"""
        if user_input:
            print("AttributeError: property 'channel_id' of 'Channel' object has no setter")
        else:
            self.__channel_id = user_input

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        result = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(result, indent=4))

    def json_loads(self):
        """Сохраняет данные о канале в виде словаря в dict_youtube"""
        json_yotube = json.dumps(
            self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute(),
            indent=4)
        return json.loads(json_yotube)

    def title_youtube(self):
        """Возвращает название канала"""
        for item in self.json_loads()['items']:
            return item['snippet']['title']

    def id_channel(self):
        """возвращяет id канала"""
        for item in self.json_loads()['items']:
            return item['id']

    def descriptions(self):
        """Возвращает описание канала"""
        for item in self.json_loads()['items']:
            return item['snippet']['description']

    def url_channel(self):
        """Возвращает ссылку(URL:адрес) на канал"""
        return f"https://www.youtube.com/channel/{self.id}"

    def subscriber_count(self):
        """Возвращает количество подписчиков"""
        for item in self.json_loads()['items']:
            return item['statistics']['subscriberCount']

    def video_counts(self):
        """Возвращает количество видео"""
        for item in self.json_loads()['items']:
            return item['statistics']['videoCount']

    def view_counts(self):
        """Возвращает общее количество просмотрв"""
        for item in self.json_loads()['items']:
            return item['statistics']['viewCount']

    @classmethod
    def get_service(cls):
        """Получает объект для работы с API вне класса"""
        return build('youtube', 'v3', developerKey=API_KEY)

    def to_json(self, filename):
        """Создает json файл с данными о канале"""
        result = {
            'id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(filename, "w", encoding='utf-8') as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
