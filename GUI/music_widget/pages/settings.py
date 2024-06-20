import flet as ft
from components.settings_options import SettingsOptions
from components.widget_layout import WidgetLayout
from components.opacity_slider import OpacitySlider
from components.color_picker import ColorPicker
from components.always_top import AlwaysTop

def open_settings(page: ft.Page, queue,conf):
    page.title = "Settings"
    page.window_width = 450
    page.window_height = 620
    page.spacing = 0
    page.padding = 0
    page.window_minimizable = False
    page.window_maximizable = False
    page.add(Settings(queue,conf))
    page.update()


class Settings(ft.Container):
    def __init__(self, props, conf):
        super().__init__()
        self.__queue=props
        self.__conf=conf
        self.expand = True

        self.options = [
            SettingsOptions("Layout", WidgetLayout(self.__queue), "Choose from three available widget layout"),
            SettingsOptions("Opacity", OpacitySlider(self.__queue, conf.opacity), "Change the transparency of the widget"),
            SettingsOptions("Color", ColorPicker(self.__queue), "Set your own color"),
            SettingsOptions("Always on top", AlwaysTop(self.__queue, conf.always_on_top), "Set the widget to always display above other apps"),
        ]

        self.content = ft.Column(
            spacing=0,
            controls=self.options
        )