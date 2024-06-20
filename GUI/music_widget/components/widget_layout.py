import flet as ft
import math

class WidgetLayout(ft.Container):
    def __init__(self, __props):
        super().__init__()
        self.__queue = __props
        self.expand = True

        self.content = ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            spacing=2,
            controls=[
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.bottom_center,
                    content=ft.Column(
                        spacing=0,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.RECTANGLE,
                                on_click=lambda _: self.__queue.put("default_layout")
                            ),
                            ft.Text("Default")
                        ]
                    )
                ),
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        spacing=0,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.RECTANGLE_ROUNDED,
                                on_click=lambda _: self.__queue.put("vertical_layout"),
                                rotate=ft.Rotate(angle=0.50 * math.pi, alignment=ft.alignment.center)
                            ),
                            ft.Text("Vertical")
                        ]
                    )
                ),
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        spacing=0,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.RECTANGLE,
                                on_click=lambda _: self.__queue.put("music_island")
                            ),
                            ft.Text("Island")
                        ]
                    )
                ),
            ]
        )