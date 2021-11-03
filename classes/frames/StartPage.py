try:
    from tkinter import *
except ImportError:
    from Tkinter import *
except Exception as e:
    print(e)
    quit()

from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import NoSuchElementException

from classes.Driver import Driver


class StartPage(Frame):
    """The first frame of the application that will be shown on start"""

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        "use _var_.get() to get value of object"
        self.url = StringVar()
        self.num_products = IntVar()

        Label(
            self,
            text="-Make sure you have read the help text before using for the first time-",
            font=controller.italic_font,
            bg=controller.bg_color,
            fg=controller.fg_color,
        ).pack(pady=(150, 0))

        "user input: link"
        Label(
            self,
            text="Enter the Best Buy url you would like watched:",
            font=controller.body_font,
            bg=controller.bg_color,
            fg=controller.fg_color,
        ).pack(pady=(20, 0))
        Entry(
            self,
            font=controller.body_font,
            width=60,
            textvariable=self.url,
            bg=controller.bg_color,
            fg=controller.fg_color,
        ).pack()

        "user input: number of items"
        Label(
            self,
            text="How many items do you want to try to buy?",
            font=controller.body_font,
            bg=controller.bg_color,
            fg=controller.fg_color,
        ).pack(pady=(20, 0))
        Spinbox(
            self,
            font=controller.body_font,
            from_=1,
            to=20,
            width=3,
            textvariable=self.num_products,
            bg=controller.bg_color,
            fg=controller.fg_color,
        ).pack()

        "continue button"
        self.continue_btn = Button(
            self,
            text="Continue",
            command=lambda: self.controller.start_thread(
                "start_page_check_thread"),
            font=controller.button_font,
            width=controller.button_width,
            bg=controller.accent_color,
            fg=controller.accent_fg_color,
        )
        self.continue_btn.bind(
            "<Return>", lambda e: self.controller.start_thread("start_page_check_thread"))
        self.continue_btn.pack_configure(
            side=RIGHT, pady=(0, 100), padx=(0, 250))

    def check_input(self):
        """check that all user's input is valid"""
        self.continue_btn.config(state=DISABLED)
        url = None
        num_products = None
        valid = False
        try:
            url = self.url.get()
            num_products = self.num_products.get()

            if num_products < 1:
                raise TclError("Number less than zero.")

            if self.controller.user_settings["url"] != url:
                raise KeyError("Url is not the same")

            valid = True

        except TclError:
            self.controller.print_error(
                "Number of products must be a valid number over zero."
            )
        except InvalidArgumentException:
            self.controller.print_error(
                "Invalid url, try again.  (Make sure the url starts with 'https://bestbuy.com')"
            )

        except KeyError:
            try:
                if url == "" or "bestbuy.com" not in url:
                    raise InvalidArgumentException("Invalid url")

                driver = Driver()
                self.controller.test_drivers.append(driver)
                driver.get(url)
                driver.check_stock()
                valid = True

            except NoSuchElementException:
                self.controller.print_error("Invalid bestbuy url.")
            except InvalidArgumentException:
                self.controller.print_error(
                    "Invalid url, try again.  (Make sure the url starts with 'https://bestbuy.com')"
                )
            except Exception as e:
                print(e)
                self.controller.print_error(
                    "Something went wrong, check all fields and try again. " +
                    "If you keep getting this error, it is possible that this application is out of date."
                )
        finally:
            "close open driver"
            drivers = self.controller.test_drivers
            for driver in drivers:
                driver.quit()
                self.controller.test_drivers.remove(driver)

            self.continue_btn.config(state=NORMAL)
            if valid:
                "add url and num_products to App's settings"
                for x in [{"url": url}, {"num_products": num_products}]:
                    for k, v in x.items():
                        if v is not None:
                            self.controller.add_user_setting(k, v)
                "redraw and show next frame"
                self.controller.frame_func("LoginPage", "redraw")
                self.controller.show_frame("LoginPage")
