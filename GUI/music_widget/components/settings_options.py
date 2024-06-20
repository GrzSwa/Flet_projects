import flet as ft


class SettingsOptions(ft.Container):
    def __init__(self, title, widget: object, describe=None):
        super().__init__()

        self.title = title
        self.describe = describe
        self.widget = widget

        self.expand = True
        self.padding = ft.padding.all(15)
        self.content = ft.Column(
            expand=True,
            spacing=0,
            controls=[
                ft.Text(self.title, size=20, weight=ft.FontWeight.W_600),
                ft.Text(self.describe, size=12, color=ft.colors.BLACK54),
                self.widget
            ]
        )