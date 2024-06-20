import time

import flet as ft

class AudioControler(ft.Audio):
    def __init__(self, src, pb_width=125):
        super().__init__()
        self.src = src
        self.autoplay = False
        self.volume = 0.7
        self.balance = 0
        self.on_duration_changed = lambda e: self.__set_duration(e)
        self.on_position_changed = lambda e: self.__change_value(e)
        self.on_state_changed = lambda e: print("State changed:", e.data)
        self.on_seek_complete = lambda _: print("Seek complete")
        self.duration = ft.Text("0:00", size=10, color=ft.colors.WHITE54)
        self.pb = ft.ProgressBar(
            width=pb_width,
            value=0.0,
            color=ft.colors.WHITE,
            bgcolor=ft.colors.WHITE38,
            border_radius=ft.border_radius.all(2),
        )

        self.widget = ft.Container(
            content=ft.Row(
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[self.pb, self.duration]
            )
        )

    def __set_duration(self,e):
        sec = int(e.data) / 1000
        min = int(sec//60)
        remaining_seconds = sec % 60

        self.duration.value = f"{min}:{round(remaining_seconds)}"
        self.duration.update()
        self.update()

    def __change_value(self,e):
        scale_factor = self.get_duration()/ 1.0
        converted_value = int(e.data) / scale_factor
        self.pb.value = converted_value
        self.pb.update()

class AudioControler2(ft.Audio):
    def __init__(self, src):
        super().__init__()
        self.src = src
        self.autoplay = False
        self.volume = 0.7
        self.balance = 0



