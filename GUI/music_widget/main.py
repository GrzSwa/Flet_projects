import flet as ft
import pages.default_widget as dw
import pages.vertical_widget as vw
import pages.music_island as mi
from configuration.config import Config

if __name__ == "__main__":
    layout = Config().layout
    if layout == 'default_layout':
        del layout
        ft.app(target=dw.widget)
    elif layout == 'vertical_layout':
        del layout
        ft.app(target=vw.widget)
    else:
        del layout
        ft.app(target=mi.widget)

