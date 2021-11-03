try:
    from tkinter import *
except ImportError:
    from Tkinter import *
except Exception as e:
    print(e)
    quit()

import os
from markdown2 import Markdown
from tkhtmlview import HTMLLabel

from classes.myWidgets.Scrollable import Scrollable


class PurchasedPage(Frame):
    """The first frame of the application that will be shown on start"""

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        container = Frame(self)
        self.scrollable = Scrollable(
            container,
            canvas_color=controller.bg_color,
        )
        self.scrollable.pack()
        container.pack(pady=(50, 0))

        Button(
            self,
            text="Back",
            font=controller.button_font,
            bg=controller.accent_color,
            fg=controller.accent_fg_color,
            width=controller.button_width,
            command=lambda: controller.show_frame("FinishPage"),
        ).pack_configure(side="right", pady=40)

    def draw_info(self, tmp_dir):

        with open(os.path.join(tmp_dir, "purchased.md")) as f:
            file_text = f.read()
            md = HTMLLabel(
                self.scrollable.scrollable_frame,
                html=Markdown().convert(file_text),
                background=self.controller.bg_color,
                fg=self.controller.fg_color,
                font=self.controller.md_font,
                borderwidth=0,
                selectborderwidth=0,
                height=500,
                width=950,
            )
            md.pack(fill=BOTH, expand=1)
