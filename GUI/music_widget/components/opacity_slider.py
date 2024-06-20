import flet as ft


class OpacitySlider(ft.Container):
    def __init__(self, __props, __opacity_value):
        super().__init__()
        self.__queue = __props
        self.__opacity_value = __opacity_value
        self.expand = True
        self.t = ft.Text(f"{round(self.__opacity_value * 100)}%",size=20,color=ft.colors.BLACK)
        self.content = ft.Row(
            expand=True,
            spacing=0,
            controls=[
                ft.Slider(
                    min=10,
                    max=100,
                    divisions=18,
                    value=self.__opacity_value * 100,
                    width=350,
                    active_color=ft.colors.LIGHT_BLUE_900,
                    on_change=self.slider_changed
                ),
                self.t
            ]
        )

    def slider_changed(self, e):
        self.__queue.put(("change_opacity",e.control.value,))
        self.t.value = f"{round(e.control.value)}%"
        self.update()
