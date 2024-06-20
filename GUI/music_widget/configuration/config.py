import yaml

class Config:
    def __init__(self):
        self.__data = self.open()
        self.__layout = self.__data['layout']
        self.__opacity = self.__data['opacity']
        self.__color = self.__data['color']
        self.__last_link = self.__data['last_link']
        self.__always_on_top = self.__data['always_on_top']
        self.__current_song = self.__data['current_song']
        self.__last_playlist_url = self.__data['last_playlist_url']
        self.__last_artist = self.__data['last_artist']
        self.__last_song_title = self.__data['last_song_title']
        self.__last_thumbnail = self.__data['last_thumbnail']

    @property
    def layout(self):
        return self.__layout

    @layout.setter
    def layout(self, value):
        if value in ['default_layout','vertical_layout','music_island']:
            self.__layout = value
            self.__data['layout'] = value
            self.save(self.__data)
            print("SAVED")
    @property
    def opacity(self):
        return self.__opacity

    @opacity.setter
    def opacity(self, value):
        if 0.0 <= value <= 1.0:
            self.__opacity = value
            self.__data['opacity'] = value
            self.save(self.__data)
    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value
        self.__data['color'] = value
        self.save(self.__data)

    @property
    def last_link(self):
        return self.__last_link

    @last_link.setter
    def last_link(self, value):
        self.__last_link = value
        self.__data['last_link'] = value
        self.save(self.__data)
    @property
    def always_on_top(self):
        return self.__always_on_top

    @always_on_top.setter
    def always_on_top(self, value):
        self.__always_on_top = value
        self.__data['always_on_top'] = value
        self.save(self.__data)

    @property
    def current_song(self):
        return self.__current_song

    @current_song.setter
    def current_song(self, value):
        self.__current_song = value
        self.__data['current_song'] = value
        self.save(self.__data)

    @property
    def last_playlist_url(self):
        return self.__last_playlist_url

    @last_playlist_url.setter
    def last_playlist_url(self, value):
        self.__last_playlist_url = value
        self.__data['last_playlist_url'] = value
        self.save(self.__data)
    @property
    def last_artist(self):
        return self.__last_artist

    @last_artist.setter
    def last_artist(self, value):
        self.__last_artist = value
        self.__data['last_artist'] = value
        self.save(self.__data)

    @property
    def last_song_title(self):
        return self.__last_song_title

    @last_song_title.setter
    def last_song_title(self, value):
        self.__last_song_title = value
        self.__data['last_song_title'] = value
        self.save(self.__data)
    @property
    def last_thumbnail(self):
        return self.__last_thumbnail

    @last_thumbnail.setter
    def last_thumbnail(self, value):
        self.__last_thumbnail = value
        self.__data['last_thumbnail'] = value
        self.save(self.__data)


    def open(self):
        with open('GUI/music_widget/configuration/conf.yaml','r') as file:
            conf = yaml.safe_load(file)
        return conf

    def save(self, data):
        with open('GUI/music_widget/configuration/conf.yaml', 'w') as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True)

