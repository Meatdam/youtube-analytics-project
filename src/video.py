import os
from dotenv import load_dotenv
from googleapiclient.discovery import build


class Video:
    """
    Класс Video обрабатывает видео по его ID
    """
    load_dotenv()
    API = os.getenv('API_KEY')

    def __init__(self, video_id):
        """
        Инициализатор класса Vido
        """
        self.video_id = video_id
        self.video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                               id=video_id).execute()

        self.video_title: str = self.video_response['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/{self.video_id}"
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        """
        Метод str отдает строковое значение класса
        """
        return self.video_title

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

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_video = self.get_service().playlistItems().list(playlistId=playlist_id, part='contentDetails',
                                                                      maxResults=50, ).execute()


