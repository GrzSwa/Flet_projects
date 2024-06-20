import flet as ft


class SongInfo(ft.Container):
    def __init__(self, artist, title):
        super().__init__()
        self.expand = True
        self.padding = ft.padding.only(left=15,right=15,top=20)
        self.alignment = ft.alignment.center

        self.artist = ft.Text(
            value=artist,
            color=ft.colors.WHITE,
            size=16,
            weight=ft.FontWeight.W_600,
            text_align=ft.TextAlign.CENTER,
            overflow=ft.TextOverflow.ELLIPSIS,
            max_lines=1
        )

        self.title = ft.Text(
            value=title,
            color=ft.colors.WHITE54,
            overflow=ft.TextOverflow.ELLIPSIS,
            max_lines=1,
            size=8
        )

        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=1,
            controls=[
                ft.Container(
                    content=self.artist
                ),
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=10),
                    content=self.title
                )

            ]
        )