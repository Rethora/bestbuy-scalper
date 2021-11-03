try:
    from tkinter import *
except ImportError:
    from Tkinter import *
except Exception as e:
    print(e)
    quit()


class FinishPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.container = Frame(
            self, bg=self.controller.bg_color)
        self.container.pack(pady=(150, 0))

        purchased_btn = Button(self,
                               text="Purchased",
                               font=controller.button_font,
                               width=controller.button_width,
                               bg=controller.accent_color,
                               fg=controller.accent_fg_color,
                               command=lambda: self.controller.show_frame("PurchasedPage"))
        purchased_btn.bind(
            "<Return>",
            lambda e: self.controller.show_frame("PurchasedPage")
        )
        purchased_btn.pack(side=RIGHT, padx=(10, 0))

        err_btn = Button(self, text="Errors",
                         font=controller.button_font,
                         width=controller.button_width,
                         bg=controller.accent_color,
                         fg=controller.accent_fg_color,
                         command=lambda: self.controller.show_frame("ErrorsPage"))
        err_btn.bind(
            "<Return>", lambda e: self.controller.show_frame("ErrorsPage"))
        err_btn.pack(side=RIGHT, padx=(0, 10))

    def draw_info(self):
        """draw labels with info about scalp"""

        "this is where we will either show the info about bought products or tell the user that no items were bought"
        url = self.controller.get_user_setting("url")
        time = self.controller.get_curr_time()
        drivers = self.controller.drivers
        num_drivers_left = len(drivers)

        Label(
            self.container,
            text="Scalper finished at:",
            bg=self.controller.bg_color,
            fg=self.controller.fg_color,
            font=self.controller.body_font
        ).pack()
        Label(
            self.container,
            text=time,
            bg=self.controller.bg_color,
            fg=self.controller.accent_color,
            font=self.controller.body_font
        ).pack()

        if num_drivers_left > 0:
            Label(
                self.container,
                text="This scalper was watching the product at url:",
                bg=self.controller.bg_color,
                fg=self.controller.fg_color,
                font=self.controller.body_font
            ).pack(pady=(20, 0))
            url_label = Label(
                self.container,
                text=url,
                bg=self.controller.bg_color,
                fg="blue",
                font=self.controller.body_font,
                cursor="hand2"
            )
            url_label.bind(
                "<Button-1>",
                lambda e: self.controller.open_page(url)
            )
            url_label.pack()

            if num_drivers_left == 1:
                text = "Bought " + str(num_drivers_left) + " product."
            else:
                text = "Bought " + str(num_drivers_left) + " products."

            Label(
                self.container,
                text=text,
                bg=self.controller.bg_color,
                fg=self.controller.fg_color,
                font=self.controller.body_font
            ).pack(pady=(20, 0))

            # for i, driver in enumerate(drivers):
            #     email = driver.get_user_prop("email")
            #     Label(self.container, text=email, font=self.controller.body_font,
            #           bg=self.controller.bg_color, fg=self.controller.accent_color).pack()
        else:
            Label(
                self.container,
                text="No products were bought. Check out 'Errors' to see where scalper encountered problems.",
                bg=self.controller.bg_color,
                fg=self.controller.fg_color,
                font=self.controller.body_font
            ).pack(pady=(20, 0))
