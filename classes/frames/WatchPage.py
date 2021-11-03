try:
    from tkinter import *
    from tkinter import messagebox
except ImportError:
    from Tkinter import *
    from Tkinter import messagebox
except Exception as e:
    print(e)
    quit()


class WatchPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        "scalper info display"
        self.info_container = Frame(self, bg=self.controller.bg_color)
        self.info_container.pack(side=TOP, pady=(150, 0))

        "time updated display"
        self.container = Frame(self, bg=self.controller.bg_color)
        Label(
            self.container,
            text="Checking if item is available...",
            font=self.controller.body_font,
            bg=self.controller.bg_color,
            fg=self.controller.fg_color,
        ).pack()
        self.container.pack(pady=(20, 0))
        Label(
            self,
            text="Closing this application will stop scalper from watching/buying product",
            font=self.controller.body_font,
            bg=self.controller.bg_color,
            fg=self.controller.fg_color
        ).pack(pady=(20, 0))

    def draw_info(self):
        url = self.controller.user_settings["url"]
        url_label = Label(self.info_container, text="Watching: " + url,
                          font=self.controller.body_font, bg=self.controller.bg_color, fg="blue", cursor="hand2")
        url_label.bind("<Button-1>", lambda e: self.controller.open_page(url))
        url_label.pack()

        num_products = self.controller.user_settings["num_products"]
        num_label = Label(self.info_container, text="Number of products trying to buy: " + str(num_products),
                          font=self.controller.body_font, bg=self.controller.bg_color, fg=self.controller.fg_color)
        num_label.pack(pady=(20, 0))

    def redraw(self, instock):
        for child in self.container.winfo_children():
            child.destroy()
        if not instock:
            text = "Item still not in stock, last checked at " + self.controller.get_curr_time()
        else:
            text = "Item in stock at " + self.controller.get_curr_time() + ". Buying now!"
        Label(
            self.container,
            text=text,
            font=self.controller.body_font,
            bg=self.controller.bg_color,
            fg=self.controller.fg_color,
        ).pack()
