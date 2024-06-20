import flet as ft
import multiprocessing
import threading
from .multiprocessing import window_settings
from components.audio_controler import AudioControler, AudioControler2
from .settings import open_settings
from configuration.config import Config
from utilis.youtube.youtube import Youtube

class MusicIslandWidget(ft.Container):
    def __init__(self, **kwargs):
        super().__init__()
        self.options = kwargs
        self.config = kwargs.get('config')
        self.audio = kwargs.get('audio_controller')[0]
        self.yt = kwargs.get('yt_controller')

        self.bgcolor = self.config.color
        self.expand = True
        self.border_radius = ft.border_radius.all(10)

        self.linear_gradient = ft.Container(
            height=40,
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_right,
                end=ft.alignment.center_left,
                colors=[self.bgcolor, ft.colors.BLACK],
            ),
        )

        self.play_button = ft.Icon(
            name=ft.icons.PLAY_CIRCLE_FILL if self.audio.on_state_changed != 'playing' else ft.icons.PAUSE_CIRCLE_FILLED,
            size=16,
            color=ft.colors.WHITE
        )

        self.content = ft.Stack(
            expand=True,
            controls=[
                self.audio.widget,
                self.linear_gradient,
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(horizontal=5),
                    height=40,
                    bgcolor=ft.colors.TRANSPARENT,
                    content=ft.Row(
                        expand=True,
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            ft.Container(
                                content=ft.Icon(
                                    name=ft.icons.SETTINGS,
                                    size=12,
                                    color=ft.colors.WHITE54
                                ),
                                on_click=lambda _: self.options["settings"].start_new_process(self.options["page"],
                                                                                              self.options["queue"],
                                                                                              self.options["settings"])
                            ),

                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Icon(
                                                name=ft.icons.SKIP_PREVIOUS,
                                                size=16,
                                                color=ft.colors.WHITE
                                            ),
                                            on_click=lambda _: self.previous_song()
                                        ),
                                        ft.Container(
                                            content=self.play_button,
                                            on_click=lambda e: self.change_play_button(e)
                                        ),
                                        ft.Container(
                                            content=ft.Icon(
                                                name=ft.icons.SKIP_NEXT,
                                                size=16,
                                                color=ft.colors.WHITE
                                            ),
                                            on_click=lambda _: self.next_song()
                                        ),
                                    ]
                                )
                            ),
                            ft.Container(
                                content=ft.Icon(
                                    name=ft.icons.LINK,
                                    size=12,
                                    color=ft.colors.WHITE54
                                ),
                                on_click=lambda _: self.paste_link(self.options["page"].get_clipboard())
                            ),
                        ]
                    )
                ),
            ]
        )

    def change_color(self, color):
        self.linear_gradient.gradient.colors = [color, ft.colors.BLACK]
        self.linear_gradient.update()

    def change_play_button(self,e):
        if e.control.content.name == ft.icons.PLAY_CIRCLE_FILL and self.audio.get_current_position() > 0:
            e.control.content.name = ft.icons.PAUSE_CIRCLE_FILLED
            self.audio.resume()

        elif e.control.content.name == ft.icons.PLAY_CIRCLE_FILL:
            e.control.content.name = ft.icons.PAUSE_CIRCLE_FILLED
            self.audio.play()
        else:
            e.control.content.name = ft.icons.PLAY_CIRCLE_FILL
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

        self.update()

        self.audio.autoplay = True
        self.audio.update()
        # self.audio.play()

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
        "audio_controller": (audio_controller, audio_controller2,),
        "yt_controller": yt_controller
    }
    page.window_center()
    page.window_always_on_top = conf.always_on_top
    page.window_frameless = True
    page.window_bgcolor = ft.colors.TRANSPARENT
    page.window_width = 100
    page.window_height = 5
    page.spacing = 0
    page.padding = 0
    page.window_minimizable = False
    page.window_maximizable = False
    page.window_opacity = conf.opacity
    page.overlay.append(audio_controller)
    page.overlay.append(audio_controller2)
    widget = MusicIslandWidget(**args)
    page.bgcolor = ft.colors.TRANSPARENT
    page.add(
        ft.Container(
            expand=True,
            content=ft.WindowDragArea(widget)
        )
    )
    page.update()

    threading.Thread(target=p.handle_queue, args=(page, args, queue), daemon=True).start()