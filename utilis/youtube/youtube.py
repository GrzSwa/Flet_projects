from pytube import Playlist, YouTube
from .utilis.song import Song
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
class Youtube:
    def __init__(self, last_playlist_url, current_song):
        if last_playlist_url is not None:
            self.load_playlist(last_playlist_url)
        else:
            self.playlist = None
        self.current_song = current_song

    def load_playlist(self, playlist_url):
        self.playlist = self.__get_playlist(playlist_url)
        print(f"LOADED YOUTUBE PLAYLIST: {playlist_url}, len playlist = {len(self.playlist)}")

    def next(self):
        self.current_song += 1 if self.current_song < len(self.playlist) - 1 else 0
        return self.playlist[self.current_song]

    def previous(self):
        self.current_song -= 1 if self.current_song > 0 else 0
        return self.playlist[self.current_song]

    def __get_playlist(self, playlist_url):
        try:
            playlist = Playlist(playlist_url)
            songs = []
            lock = threading.Lock()

            def fetch_song(video_url):
                yt = YouTube(video_url)
                audio_stream = yt.streams.filter(only_audio=True).first()
                return {
                    'title': yt.title,
                    'artist': yt.author,
                    'thumbnail': yt.thumbnail_url,
                    'music_url': audio_stream.url if audio_stream else None
                }

            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = [executor.submit(fetch_song, video_url) for video_url in playlist.video_urls]
                for future in as_completed(futures):
                    try:
                        song = future.result()
                        with lock:
                            songs.append(Song
                                (
                                title=song["title"],
                                artist=song["artist"],
                                thumbnail=song["thumbnail"],
                                music_url=song["music_url"] if song["music_url"] else None
                                )
                            )
                    except Exception as e:
                        print(f"Error fetching song: {e}")

            return songs
        except Exception as e:
            print(str(e))
            return []



