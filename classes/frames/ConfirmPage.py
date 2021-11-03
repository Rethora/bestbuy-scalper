try:
    from tkinter import *
except ImportError:
    from Tkinter import *
except Exception as e:
    print(e)
    quit()


class ConfirmPage(Frame):
    """the frame that will be shown when prompting the user if they are ready to continue"""

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.container = Frame(self, bg=controller.bg_color)
        self.container.pack(pady=(150, 0))

        "back and continue buttons"
        continue_btn = Button(
            self,
            text="Continue",
            font=controller.button_font,
            bg=controller.accent_color,
            fg=controller.accent_fg_color,
            command=self.confirm,
            width=controller.button_width,
        )
        continue_btn.bind("<Return>", self.confirm)
        continue_btn.pack_configure(
            side=RIGHT,
            padx=controller.button_padding
        )

        back_btn = Button(
            self,
            text="Back",
            font=controller.button_font,
            bg=controller.accent_color,
            fg=controller.accent_fg_color,
            command=self.page_back_func,
            width=controller.button_width,
        )
        back_btn.bind("<Return>", self.page_back_func)
        back_btn.pack_configure(
            side=RIGHT, padx=controller.button_padding)

    def draw_info(self):
        Label(self.container, text="Make sure this is the correct url.",
              font=self.controller.body_font,
              bg=self.controller.bg_color,
              fg=self.controller.fg_color, ).pack()

        url = self.controller.get_user_setting("url")
        url = (url[:100] + "...") if len(url) > 100 else url

        url_label = Label(
            self.container, text=url,
            font=self.controller.body_font,
            fg="blue",
            bg=self.controller.bg_color,
            cursor="hand2", )
        url_label.bind(
            "<Button-1>",
            lambda e: self.controller.open_page(url)
        )
        url_label.pack(pady=(0, 10))

        with open("assets/confirm.txt") as f:
            file_text = f.read()
            Label(
                self.container,
                font=self.controller.body_font,
                bg=self.controller.bg_color,
                fg=self.controller.fg_color,
                text=str(file_text),
                justify=CENTER,
                wraplength=650,
            ).pack()

    def confirm(self, event=None):
        self.controller.start_thread("scalper_thread")
        self.controller.frame_func("WatchPage", "draw_info")
        self.controller.show_frame("WatchPage")

    def page_back_func(self, event=None):
        """on back button click: close each driver, and empty app's drivers"""
        self.controller.close_all_drivers()
        self.controller.show_frame("LoginPage")
