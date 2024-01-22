import os
import json
from googleapiclient.discovery import build

API_KEY = os.getenv('API_KEY')


class Channel:
    """Класс для ютуб-канала"""
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        result = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(result, indent=4))
