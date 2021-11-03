try:
    from tkinter import *
except ImportError:
    from Tkinter import *
except Exception as e:
    print(e)
    quit()

from markdown2 import Markdown
from tkhtmlview import HTMLLabel

from classes.myWidgets.Scrollable import Scrollable


class HelpPage(Frame):
    """the frame that will be shown when the user clicks 'help'"""

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        Label(
            self,
            text="Help",
            bg=controller.bg_color,
            fg=controller.fg_color,
            font=controller.title_font,
            pady=40,
        ).pack()

        frame = Frame(self)
        self.scrollable = Scrollable(
            frame,
            canvas_color=controller.bg_color,
        )
        self.scrollable.pack()
        frame.pack()

        with open("assets/help.md") as f:
            file_text = f.read()
            HTMLLabel(
                self.scrollable.scrollable_frame,
                html=Markdown().convert(file_text),
                background=controller.bg_color,
                fg=controller.fg_color,
                font=controller.body_font,
                borderwidth=0,
                selectborderwidth=0,
                height=500,
                width=950,
            ).pack(fill=BOTH, expand=1)

            # self.scrollable.update()

        Button(
            self,
            text="Back",
            font=controller.button_font,
            bg=controller.accent_color,
            fg=controller.accent_fg_color,
            width=controller.button_width,
            command=lambda: controller.show_frame(prev_option=True),
        ).pack_configure(side="right", pady=40)
