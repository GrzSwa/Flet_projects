import flet as ft
import pages
import multiprocessing

def _s_(sub_page_class, queue, props):
    import flet

    def APP(page: flet.Page):
        if sub_page_class.controls is not None:
            for con in sub_page_class.controls:
                page.add(con)
        if sub_page_class.page_props is not None:
            for P in sub_page_class.page_props:
                if hasattr(page, P):
                    setattr(page, P, sub_page_class.page_props[P])
                    page.update()
        page.update()
        if sub_page_class.target is not None:
            sub_page_class.target(page, queue, props)
        page.update()

    def monitor_process_lifetime():
        flet.app(target=APP, view=sub_page_class.view)
        queue.put("process_closed")

    monitor_process_lifetime()


class window_settings(object):
    def __init__(self, controls=None, page_props=None, target=None, target_args=None, view=ft.FLET_APP):
        self.controls = controls
        self.page_props = page_props
        self.target = target
        self.target_args = target_args if target_args else ()
        self.view = view
        self.__PROCESS_STARTED = False

    def start(self):
        queue = multiprocessing.Queue()
        multiprocessing.Process(target=_s_, args=(self, *self.target_args)).start()

    def handle_queue(self, page, args, queue):
        while True:
            message = queue.get()
            if type(message) is tuple:
                if message[0] == "change_opacity":
                    page.window_opacity = message[1]*0.01
                    page.update()
                    args['config'].opacity = message[1]*0.01
                elif message[0] == "change_color":
                    page.controls[0].content.content.change_color(message[1])
                    page.update()
                    args['config'].color = message[1]
                elif message[0] == "change_always_on_top":
                    page.window_always_on_top = message[1]
                    page.update()
                    args['config'].always_on_top = message[1]
            else:
                if message == "save":
                    print("Saved")
                elif message == "default_layout":
                    page.window_width = 350
                    page.window_height = 125
                    page.remove_at(0)
                    page.add(ft.Container(expand=True, content=ft.WindowDragArea(pages.default_widget.DefaultWidget(**args))))
                    page.update()
                    args['config'].layout = "default_layout"
                elif message == "vertical_layout":
                    page.window_width = 165
                    page.window_height = 300
                    page.remove_at(0)
                    page.add(ft.Container(expand=True, content=ft.WindowDragArea(pages.vertical_widget.VerticalWidget(**args))))
                    page.update()
                    args['config'].layout = "vertical_layout"
                elif message == "music_island":
                    page.window_width = 80
                    page.window_height = 15
                    page.remove_at(0)
                    page.add(ft.Container(expand=True, content=ft.WindowDragArea(pages.music_island.MusicIslandWidget(**args))))
                    page.update()
                    args['config'].layout = "music_island"
                elif message == "process_closed":
                    self.__PROCESS_STARTED = False

    def start_new_process(self, page, queue, p):
        if not self.__PROCESS_STARTED:
            p.start()
            self.__PROCESS_STARTED = True
        else:
            print("Process already running")
            page.update()

