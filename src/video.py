import os
from dotenv import load_dotenv
from googleapiclient.discovery import build


class Video:
    """
    Класс Video обрабатывает видео по его ID
    """
    load_dotenv()
    API = os.getenv('API_KEY')

    def __init__(self, channel_id):
        """
        Инициализатор класса Vido
        """

        self.video_id = channel_id
        self.video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                               id=channel_id).execute()


        try:
            self.title: str = self.video_response['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/{self.video_id}"
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        """
        Метод str отдает строковое значение класса
        """
        return self.title

    @classmethod
    def get_service(cls):
        """
        Класс метод Video
        """
        youtube = build('youtube', 'v3', developerKey=cls.API)
        return youtube


class PLVideo(Video):
    """
    Класс PLVideo наследник класса Video
    return: id плейлиста, id видео
    """

    def __init__(self, video_id, channel_id):
        super().__init__(video_id)
        self.playlist_id = channel_id


