import os
import json
from googleapiclient.discovery import build

API_KEY = os.getenv('API_KEY')


class Channel:
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, channel_id):
        """Инициализация класса Channel"""
        self.__channel_id = channel_id
        channel = self.json_loads()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{channel["items"][0]["id"]}'
        self.subscriber = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

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
