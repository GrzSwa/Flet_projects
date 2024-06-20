import flet as ft


class AlwaysTop(ft.Container):
    def __init__(self, __props, __always_on_top):
        super().__init__()
        self.__queue = __props
        self.__always_on_top = __always_on_top
        self.expand = True
        self.content = ft.Switch(
            value=self.__always_on_top,
            active_color=ft.colors.LIGHT_BLUE_900,
            on_change=self.switch_changed
        )

    def switch_changed(self, e):
        self.__queue.put(("change_always_on_top",e.control.value,))
        self.update()
