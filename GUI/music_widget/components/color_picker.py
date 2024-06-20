import flet as ft

class ColorPicker(ft.Container):
    def __init__(self, __props):
        super().__init__()
        self.__queue = __props
        self.expand = True
        self.default_color = "#000000"

        self.color_preview = ft.Icon(ft.icons.SQUARE, color=f"{self.default_color}")
        self.t = ft.TextField(
            label="",
            hint_text="Please enter your color in hex",
            height=40,
            width=260,
            text_size=12,
            max_lines=1,
            on_change=self.change_color
        )
        self.set_button = ft.ElevatedButton(text="Set color", on_click=self.set_color)

        self.content = ft.Row(
            expand=True,
            controls=[self.color_preview, self.t, self.set_button]
        )

    def change_color(self, e):
        self.default_color = e.control.value
        if len(self.default_color) < 7:
            self.default_color = "#000000"
        elif self.default_color[0] != "#":
            self.default_color = "#000000"
        else:
            self.color_preview.color = e.control.value
            self.color_preview.update()
            self.update()

    def set_color(self, _):
        self.__queue.put(("change_color",  self.default_color))