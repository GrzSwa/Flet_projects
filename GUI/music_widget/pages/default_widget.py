import time

import flet as ft
import multiprocessing
import threading
from .multiprocessing import window_settings
from components.audio_controler import AudioControler, AudioControler2
from components.song_info import SongInfo
from .settings import open_settings
from configuration.config import Config
from utilis.youtube.youtube import Youtube

class DefaultWidget(ft.Container):
    def __init__(self, **kwargs):
        super().__init__()
        self.options = kwargs
        self.config = kwargs.get('config')
        self.audio = kwargs.get('audio_controller')[0]
        self.yt = kwargs.get('yt_controller')

        self.bgcolor = self.config.color #'#453256'
        self.expand = True
        self.border_radius = ft.border_radius.all(10)
        self.song_info = SongInfo(self.config.last_artist, self.config.last_song_title)

        self.linear_gradient = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_right,
                end=ft.alignment.center_left,
                colors=[self.bgcolor, ft.colors.with_opacity(0.8,self.bgcolor), ft.colors.TRANSPARENT],
                stops=[0.55,0.6,1]
            ),
        )

        self.thumbnail = ft.Container(
            expand=2,
            alignment=ft.alignment.center_left,
            image_src=self.config.last_thumbnail,
            image_fit=ft.ImageFit.COVER
        )

        self.play_button = ft.IconButton(
            icon=ft.icons.PLAY_CIRCLE_FILL if self.audio.on_state_changed != 'playing' else ft.icons.PAUSE_CIRCLE_FILLED,
            icon_size=32,
            icon_color=ft.colors.WHITE,
            on_click=lambda e: self.change_play_button(e)
        )

        self.content = ft.Stack(
            controls=[
                ft.Row(
                    expand=True,
                    spacing=0,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        self.thumbnail,
                        ft.Container(
                            expand=2
                        ),
                    ]
                ),
                self.linear_gradient,
                ft.IconButton(
                    icon=ft.icons.SETTINGS,
                    icon_color=ft.colors.BLACK54,
                    icon_size=16,
                    bottom=0,
                    padding=ft.padding.all(1),
                    splash_radius=1,
                    on_click=lambda _: self.options["settings"].start_new_process(self.options["page"], self.options["queue"], self.options["settings"])
                ),
                ft.Container(
                    width=200,
                    right=0,
                    content=self.song_info
                ),
                ft.Container(
                    width=200,
                    right=0,
                    bottom=5,
                    content=ft.Container(
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.START,
                            spacing=1,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=3,
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.icons.SKIP_PREVIOUS,
                                            icon_size=22,
                                            icon_color=ft.colors.WHITE,
                                            on_click=lambda _: self.previous_song()
                                        ),
                                        self.play_button,
                                        ft.IconButton(
                                            icon=ft.icons.SKIP_NEXT,
                                            icon_size=22,
                                            icon_color=ft.colors.WHITE,
                                            on_click=lambda _: self.next_song()
                                        ),
                                    ]
                                ),
                                self.audio.widget
                            ]
                        )
                    )
                ),
                ft.IconButton(
                    icon=ft.icons.LINK,
                    icon_color=ft.colors.BLACK54,
                    icon_size=16,
                    right=0,
                    top=0,
                    padding=ft.padding.all(1),
                    splash_radius=1,
                    on_click=lambda _: self.paste_link(self.options["page"].get_clipboard())
                ),

            ]
        )

    def change_color(self, color):
        self.linear_gradient.gradient.colors = [color, ft.colors.with_opacity(0.8, color), ft.colors.TRANSPARENT]
        self.linear_gradient.update()

    def change_play_button(self,e):
        if e.control.icon == ft.icons.PLAY_CIRCLE_FILL and self.audio.get_current_position() > 0:
            e.control.icon = ft.icons.PAUSE_CIRCLE_FILLED
            self.audio.resume()

        elif e.control.icon == ft.icons.PLAY_CIRCLE_FILL:
            e.control.icon = ft.icons.PAUSE_CIRCLE_FILLED
            self.audio.play()
            self.audio.autoplay = True
        else:
            e.control.icon = ft.icons.PLAY_CIRCLE_FILL
            self.audio.pause()
        self.update()

    def paste_link(self, link):
        self.yt.current_song = -1
        self.yt.load_playlist(link)
        song = self.yt.next()
        self.audio.src = song.url
        self.audio.autoplay = True
        self.audio.play()
        self.play_button.icon = ft.icons.PAUSE_CIRCLE_FILLED
        self.audio.update()
        self.play_button.update()
        self.config.last_link = song.url
        self.config.last_artist = song.artist
        self.config.last_song_title = song.title
        self.config.last_thumbnail = song.thumbnail
        self.config.last_playlist_url = link
        self.config.current_song = self.yt.current_song

        self.thumbnail.image_src = song.thumbnail
        self.song_info.artist.value = song.artist
        self.song_info.title.value = song.title
        self.song_info.update()

        self.update()

    def next_song(self):
        self.audio.pause()
        self.play_button.icon = ft.icons.PLAY_CIRCLE_FILL
        self.play_button.update()
        song = self.yt.next()
        self.audio.src = song.url
        self.play_button.icon = ft.icons.PAUSE_CIRCLE_FILLED
        self.audio.update()
        self.play_button.update()
        self.config.last_link = song.url
        self.config.last_artist = song.artist
        self.config.last_song_title = song.title
        self.config.last_thumbnail = song.thumbnail
        self.config.current_song = self.yt.current_song

        self.thumbnail.image_src = song.thumbnail
        self.song_info.artist.value = song.artist
        self.song_info.title.value = song.title
        self.song_info.update()
        self.update()

        self.audio.autoplay = True
        self.audio.update()
        # self.audio.play()

    def previous_song(self):
        self.audio.pause()
        self.play_button.icon = ft.icons.PLAY_CIRCLE_FILL
        self.play_button.update()
        song = self.yt.previous()
        self.audio.src = song.url
        self.play_button.icon = ft.icons.PAUSE_CIRCLE_FILLED
        self.audio.update()
        self.play_button.update()
        self.config.last_link = song.url
        self.config.last_artist = song.artist
        self.config.last_song_title = song.title
        self.config.last_thumbnail = song.thumbnail
        self.config.current_song = self.yt.current_song

        self.thumbnail.image_src = song.thumbnail
        self.song_info.artist.value = song.artist
        self.song_info.title.value = song.title
        self.song_info.update()
        self.update()

        self.audio.autoplay = True
        self.audio.update()
        #self.audio.play()

def widget(page: ft.Page):
    queue = multiprocessing.Queue()
    conf = Config()
    audio_controller = AudioControler(conf.last_link)
    audio_controller2 = AudioControler2(conf.last_link)
    yt_controller = Youtube(conf.last_playlist_url, conf.current_song)
    p = window_settings(target=open_settings, target_args=(queue,conf,))
    args = {
        "page": page,
        "queue": queue,
        "settings": p,
        "config": conf,
        "audio_controller": (audio_controller,audio_controller2,),
        "yt_controller": yt_controller
    }
    page.window_center()
    page.window_always_on_top = conf.always_on_top
    page.window_frameless = True
    page.window_bgcolor = ft.colors.TRANSPARENT
    page.window_width = 350
    page.window_height = 125
    page.spacing = 0
    page.padding = 0
    page.window_minimizable = False
    page.window_maximizable = False
    page.window_opacity = conf.opacity
    page.overlay.append(audio_controller)
    page.overlay.append(audio_controller2)
    widget = DefaultWidget(**args)
    page.bgcolor = ft.colors.TRANSPARENT
    page.add(
        ft.Container(
            expand=True,
            content=ft.WindowDragArea(widget)
        )
    )
    page.update()

    threading.Thread(target=p.handle_queue, args=(page, args, queue), daemon=True).start()