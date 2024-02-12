import os
import isodate
from dotenv import load_dotenv
from googleapiclient.discovery import build
import datetime
from src.channel import Channel
from src.video import Video, PLVideo


class PlayList:
    """
    Парсит плейлисты канала на Ютуб
    """
    load_dotenv()
    API = os.getenv('API_KEY')

    def __init__(self, id_playlist):
        self.id_playlist = id_playlist
        self.playlist_info = self.get_service().playlists().list(id=id_playlist,
                                                                 part='contentDetails, snippet', ).execute()
        self.video_response = self.get_service().playlistItems().list(playlistId=id_playlist,
                                                                      part='contentDetails',
                                                                      maxResults=50, ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.video_response['items']]

        self.video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                               id=self.video_ids).execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.id_playlist}"

    @property
    def total_duration(self):
        """
        Обьект класса Playlist
        return: суммарную длительность плейлиста
        """
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += datetime.timedelta(seconds=duration.total_seconds())
        return total_duration

    def show_best_video(self):
        """
        Метод класса Playlist
        return: Ссылку на самое популярное видео из плейлиста
        """
        max_like = 0
        max_video = ''
        for video in self.video_response['items']:
            count_like = video['statistics']['likeCount']
            count_video = video['id']
            if int(count_like) > int(max_like):
                max_video = count_video
        return f"https://youtu.be/{max_video}"

    @classmethod
    def get_service(cls):
        """
        Класс метод Playlist
        """
        youtube = build('youtube', 'v3', developerKey=cls.API)
        return youtube
